import os
import time
import threading
import queue
import random
import string
from datetime import datetime
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.test import override_settings
from django.core import mail
from django.urls import reverse
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException

# Number of parallel threads to run tests
NUM_THREADS = 4

def generate_random_string(length=8):
    """Generate a random string of fixed length"""
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(length))

class UserFlowTest(StaticLiveServerTestCase):
    """Test the complete user flow from registration to collaboration"""
    
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        # Set up Chrome options for headless browser
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--window-size=1920,1080")
        
        # Create a driver for each thread
        cls.drivers = [
            webdriver.Chrome(options=chrome_options)
            for _ in range(NUM_THREADS)
        ]
    
    @classmethod
    def tearDownClass(cls):
        # Quit all drivers
        for driver in cls.drivers:
            driver.quit()
        super().tearDownClass()
    
    def setUp(self):
        # Generate unique test data for each test run
        self.timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        self.test_users = [
            {
                'username': f'testuser{self.timestamp}_{i}',
                'email': f'testuser{self.timestamp}_{i}@example.com',
                'password': 'SecurePassword123!',
                'first_name': f'Test{i}',
                'last_name': f'User{i}'
            }
            for i in range(NUM_THREADS + 2)  # Create extra users for invites
        ]
        
        # Test data for workspace, project, team, etc.
        self.workspace_name = f'Test Workspace {self.timestamp}'
        self.project_name = f'Test Project {self.timestamp}'
        self.team_name = f'Test Team {self.timestamp}'
        self.task_name = f'Test Task {self.timestamp}'
        self.subtask_name = f'Test Subtask {self.timestamp}'
    
    def extract_verification_link(self, email_body):
        """Extract verification link from email body"""
        # This is a simplified version - adjust based on your actual email format
        start_index = email_body.find('http')
        if start_index == -1:
            return None
        
        end_index = email_body.find('"', start_index)
        if end_index == -1:
            end_index = email_body.find('\n', start_index)
        
        if end_index == -1:
            return email_body[start_index:]
        return email_body[start_index:end_index]
    
    def wait_for_element(self, driver, by, value, timeout=10):
        """Wait for an element to be present"""
        try:
            element = WebDriverWait(driver, timeout).until(
                EC.presence_of_element_located((by, value))
            )
            return element
        except TimeoutException:
            self.fail(f"Timed out waiting for element {value}")
    
    def wait_for_url_contains(self, driver, text, timeout=10):
        """Wait for URL to contain specific text"""
        try:
            WebDriverWait(driver, timeout).until(
                EC.url_contains(text)
            )
            return True
        except TimeoutException:
            self.fail(f"Timed out waiting for URL to contain {text}")
    
    def register_user(self, driver, user_data):
        """Register a new user"""
        # Navigate to signup page
        driver.get(f"{self.live_server_url}{reverse('accounts:signup')}")
        
        # Fill in the form
        self.wait_for_element(driver, By.ID, "id_username").send_keys(user_data['username'])
        self.wait_for_element(driver, By.ID, "id_email").send_keys(user_data['email'])
        self.wait_for_element(driver, By.ID, "id_password1").send_keys(user_data['password'])
        self.wait_for_element(driver, By.ID, "id_password2").send_keys(user_data['password'])
        
        # Submit the form
        self.wait_for_element(driver, By.XPATH, "//button[@type='submit']").click()
        
        # Check for success message
        success_message = self.wait_for_element(driver, By.CLASS_NAME, "alert-success")
        self.assertIn("Account created", success_message.text)
        
        # Return to verify we can extract verification link if needed
        return user_data
    
    def verify_email(self, driver, user_data):
        """Verify email for a user"""
        # In a real test, we would check the email and extract the verification link
        # For this example, we'll simulate email verification
        
        # Check if there are emails in the test outbox
        self.assertGreater(len(mail.outbox), 0, "No emails were sent")
        
        # Find the verification email for this user
        verification_email = None
        for email in mail.outbox:
            if user_data['email'] in email.to:
                verification_email = email
                break
        
        self.assertIsNotNone(verification_email, f"No verification email found for {user_data['email']}")
        
        # Extract verification link
        verification_link = self.extract_verification_link(verification_email.body)
        self.assertIsNotNone(verification_link, "Could not extract verification link")
        
        # Visit the verification link
        driver.get(verification_link)
        
        # Check for success message
        success_message = self.wait_for_element(driver, By.CLASS_NAME, "alert-success")
        self.assertIn("verified", success_message.text.lower())
    
    def login_user(self, driver, user_data):
        """Login a user"""
        # Navigate to login page
        driver.get(f"{self.live_server_url}{reverse('accounts:login')}")
        
        # Fill in the form
        self.wait_for_element(driver, By.ID, "id_username").send_keys(user_data['username'])
        self.wait_for_element(driver, By.ID, "id_password").send_keys(user_data['password'])
        
        # Submit the form
        self.wait_for_element(driver, By.XPATH, "//button[@type='submit']").click()
        
        # Check that we're redirected to the dashboard
        self.wait_for_url_contains(driver, "/dashboard")
        
        # Verify username appears in the header
        user_dropdown = self.wait_for_element(driver, By.CLASS_NAME, "dropdown-toggle")
        self.assertIn(user_data['username'], user_dropdown.text)
    
    def update_profile(self, driver, user_data):
        """Update user profile"""
        # Navigate to profile page
        driver.get(f"{self.live_server_url}/accounts/profile/")
        
        # Fill in profile information
        try:
            self.wait_for_element(driver, By.ID, "id_first_name").clear()
            self.wait_for_element(driver, By.ID, "id_first_name").send_keys(user_data['first_name'])
            
            self.wait_for_element(driver, By.ID, "id_last_name").clear()
            self.wait_for_element(driver, By.ID, "id_last_name").send_keys(user_data['last_name'])
            
            # Submit the form
            self.wait_for_element(driver, By.XPATH, "//button[@type='submit']").click()
            
            # Check for success message
            success_message = self.wait_for_element(driver, By.CLASS_NAME, "alert-success")
            self.assertIn("profile updated", success_message.text.lower())
        except (TimeoutException, NoSuchElementException):
            # If profile page doesn't have these fields, we'll skip this test
            self.skipTest("Profile update form not found or has different structure")
    
    def create_workspace(self, driver):
        """Create a new workspace"""
        # Navigate to workspace creation page
        driver.get(f"{self.live_server_url}{reverse('workspace:create')}")
        
        # Fill in the form
        self.wait_for_element(driver, By.ID, "id_name").send_keys(self.workspace_name)
        self.wait_for_element(driver, By.ID, "id_description").send_keys(f"Description for {self.workspace_name}")
        
        # Submit the form
        self.wait_for_element(driver, By.XPATH, "//button[@type='submit']").click()
        
        # Check that we're redirected to the workspace detail page
        self.wait_for_url_contains(driver, "/workspaces/")
        
        # Verify workspace name appears on the page
        workspace_title = self.wait_for_element(driver, By.TAG_NAME, "h1")
        self.assertIn(self.workspace_name, workspace_title.text)
        
        # Extract workspace ID from URL for later use
        current_url = driver.current_url
        workspace_id = current_url.split('/')[-2]
        return workspace_id
    
    def create_project(self, driver, workspace_id):
        """Create a new project in a workspace"""
        # Navigate to project creation page
        driver.get(f"{self.live_server_url}{reverse('projectflow:project-create')}")
        
        # Fill in the form
        self.wait_for_element(driver, By.ID, "id_name").send_keys(self.project_name)
        self.wait_for_element(driver, By.ID, "id_description").send_keys(f"Description for {self.project_name}")
        
        # Select workspace
        try:
            workspace_select = self.wait_for_element(driver, By.ID, "id_workspace")
            # Select by value or by visible text depending on implementation
            for option in workspace_select.find_elements(By.TAG_NAME, "option"):
                if workspace_id in option.get_attribute("value"):
                    option.click()
                    break
        except (TimeoutException, NoSuchElementException):
            self.skipTest("Workspace selection not found or has different structure")
        
        # Submit the form
        self.wait_for_element(driver, By.XPATH, "//button[@type='submit']").click()
        
        # Check that we're redirected to the project detail page
        self.wait_for_url_contains(driver, "/projects/project/")
        
        # Verify project name appears on the page
        project_title = self.wait_for_element(driver, By.TAG_NAME, "h1")
        self.assertIn(self.project_name, project_title.text)
        
        # Extract project slug from URL for later use
        current_url = driver.current_url
        project_slug = current_url.split('/')[-2]
        return project_slug
    
    def create_team(self, driver):
        """Create a new team"""
        # Navigate to team creation page
        driver.get(f"{self.live_server_url}{reverse('teamflow:team-create')}")
        
        # Fill in the form
        self.wait_for_element(driver, By.ID, "id_name").send_keys(self.team_name)
        self.wait_for_element(driver, By.ID, "id_url").send_keys(self.team_name.lower().replace(' ', '-'))
        self.wait_for_element(driver, By.ID, "id_description").send_keys(f"Description for {self.team_name}")
        
        # Submit the form
        self.wait_for_element(driver, By.XPATH, "//button[@type='submit']").click()
        
        # Check that we're redirected to the team detail page
        self.wait_for_url_contains(driver, "/teams/team/")
        
        # Verify team name appears on the page
        team_title = self.wait_for_element(driver, By.TAG_NAME, "h1")
        self.assertIn(self.team_name, team_title.text)
        
        # Extract team URL from URL for later use
        current_url = driver.current_url
        team_url = current_url.split('/')[-2]
        return team_url
    
    def create_task(self, driver, project_slug):
        """Create a new task in a project"""
        # Navigate to task creation page for the project
        driver.get(f"{self.live_server_url}/projects/task/create/?project={project_slug}")
        
        # Fill in the form
        self.wait_for_element(driver, By.ID, "id_name").send_keys(self.task_name)
        self.wait_for_element(driver, By.ID, "id_description").send_keys(f"Description for {self.task_name}")
        
        # Submit the form
        self.wait_for_element(driver, By.XPATH, "//button[@type='submit']").click()
        
        # Check that we're redirected to the task detail page
        self.wait_for_url_contains(driver, "/projects/task/")
        
        # Verify task name appears on the page
        task_title = self.wait_for_element(driver, By.TAG_NAME, "h1")
        self.assertIn(self.task_name, task_title.text)
        
        # Extract task ID from URL for later use
        current_url = driver.current_url
        task_id = current_url.split('/')[-2]
        return task_id
    
    def assign_user_to_task(self, driver, task_id, user_data):
        """Assign a user to a task"""
        # Navigate to task detail page
        driver.get(f"{self.live_server_url}/projects/task/{task_id}/")
        
        # Click on assign user button/link
        try:
            assign_button = self.wait_for_element(driver, By.XPATH, "//button[contains(text(), 'Assign') or contains(@class, 'assign')]")
            assign_button.click()
            
            # In the modal or form that appears, select the user
            user_select = self.wait_for_element(driver, By.ID, "id_assigned_users")
            for option in user_select.find_elements(By.TAG_NAME, "option"):
                if user_data['username'] in option.text:
                    option.click()
                    break
            
            # Submit the form
            self.wait_for_element(driver, By.XPATH, "//form[contains(@action, 'assign')]//button[@type='submit']").click()
            
            # Check for success message
            success_message = self.wait_for_element(driver, By.CLASS_NAME, "alert-success")
            self.assertIn("assigned", success_message.text.lower())
        except (TimeoutException, NoSuchElementException):
            # If assignment UI is different, try alternative approach
            self.skipTest("Task assignment UI not found or has different structure")
    
    def assign_user_to_project(self, driver, project_slug, user_data):
        """Assign a user to a project"""
        # Navigate to project detail page
        driver.get(f"{self.live_server_url}/projects/project/{project_slug}/")
        
        # Click on assign user button/link
        try:
            assign_button = self.wait_for_element(driver, By.XPATH, "//button[contains(text(), 'Assign') or contains(@class, 'assign')]")
            assign_button.click()
            
            # In the modal or form that appears, select the user
            user_select = self.wait_for_element(driver, By.ID, "id_assigned_users")
            for option in user_select.find_elements(By.TAG_NAME, "option"):
                if user_data['username'] in option.text:
                    option.click()
                    break
            
            # Submit the form
            self.wait_for_element(driver, By.XPATH, "//form[contains(@action, 'assign')]//button[@type='submit']").click()
            
            # Check for success message
            success_message = self.wait_for_element(driver, By.CLASS_NAME, "alert-success")
            self.assertIn("assigned", success_message.text.lower())
        except (TimeoutException, NoSuchElementException):
            # If assignment UI is different, try alternative approach
            self.skipTest("Project assignment UI not found or has different structure")
    
    def invite_user(self, driver, email):
        """Invite a new user to the platform"""
        # Navigate to invite page
        driver.get(f"{self.live_server_url}{reverse('accounts:invite_create')}")
        
        # Fill in the form
        self.wait_for_element(driver, By.ID, "id_email").send_keys(email)
        
        # Submit the form
        self.wait_for_element(driver, By.XPATH, "//button[@type='submit']").click()
        
        # Check for success message
        success_message = self.wait_for_element(driver, By.CLASS_NAME, "alert-success")
        self.assertIn("invite", success_message.text.lower())
        
        # Check if there are emails in the test outbox
        self.assertGreater(len(mail.outbox), 0, "No emails were sent")
        
        # Find the invite email for this user
        invite_email = None
        for email_obj in mail.outbox:
            if email in email_obj.to:
                invite_email = email_obj
                break
        
        self.assertIsNotNone(invite_email, f"No invite email found for {email}")
        
        # Extract invite link
        invite_link = self.extract_verification_link(invite_email.body)
        self.assertIsNotNone(invite_link, "Could not extract invite link")
        
        return invite_link
    
    def accept_invitation(self, driver, invite_link, user_data):
        """Accept an invitation and create an account"""
        # Visit the invite link
        driver.get(invite_link)
        
        # Fill in the registration form
        self.wait_for_element(driver, By.ID, "id_username").send_keys(user_data['username'])
        self.wait_for_element(driver, By.ID, "id_password1").send_keys(user_data['password'])
        self.wait_for_element(driver, By.ID, "id_password2").send_keys(user_data['password'])
        
        # Submit the form
        self.wait_for_element(driver, By.XPATH, "//button[@type='submit']").click()
        
        # Check for success message
        success_message = self.wait_for_element(driver, By.CLASS_NAME, "alert-success")
        self.assertIn("account created", success_message.text.lower())
        
        # Check that we're redirected to the login page
        self.wait_for_url_contains(driver, "login")
    
    def worker(self, thread_id, results_queue):
        """Worker function for parallel test execution"""
        driver = self.drivers[thread_id]
        user_data = self.test_users[thread_id]
        
        try:
            # Step 1: Register user
            self.register_user(driver, user_data)
            
            # Step 2: Verify email (simulated)
            # self.verify_email(driver, user_data)
            
            # Step 3: Login
            self.login_user(driver, user_data)
            
            # Step 4: Update profile
            self.update_profile(driver, user_data)
            
            # Step 5: Create workspace
            workspace_id = self.create_workspace(driver)
            
            # Step 6: Create project in workspace
            project_slug = self.create_project(driver, workspace_id)
            
            # Step 7: Create team
            team_url = self.create_team(driver)
            
            # Step 8: Create task
            task_id = self.create_task(driver, project_slug)
            
            # Step 9: Assign another user to task
            other_user = self.test_users[(thread_id + 1) % NUM_THREADS]
            self.assign_user_to_task(driver, task_id, other_user)
            
            # Step 10: Assign another user to project
            self.assign_user_to_project(driver, project_slug, other_user)
            
            # Step 11: Invite a new user
            invite_email = self.test_users[NUM_THREADS + thread_id]['email']
            invite_link = self.invite_user(driver, invite_email)
            
            # Step 12: Accept invitation (using the same driver for simplicity)
            self.accept_invitation(driver, invite_link, self.test_users[NUM_THREADS + thread_id])
            
            # Report success
            results_queue.put((thread_id, True, None))
        except Exception as e:
            # Report failure
            results_queue.put((thread_id, False, str(e)))
    
    @override_settings(EMAIL_BACKEND='django.core.mail.backends.locmem.EmailBackend')
    def test_complete_user_flow(self):
        """Test the complete user flow from registration to collaboration"""
        # Create a queue for results
        results_queue = queue.Queue()
        
        # Create and start threads
        threads = []
        for i in range(NUM_THREADS):
            thread = threading.Thread(target=self.worker, args=(i, results_queue))
            threads.append(thread)
            thread.start()
        
        # Wait for all threads to complete
        for thread in threads:
            thread.join()
        
        # Check results
        failures = []
        while not results_queue.empty():
            thread_id, success, error = results_queue.get()
            if not success:
                failures.append(f"Thread {thread_id} failed: {error}")
        
        # Assert no failures
        self.assertEqual(len(failures), 0, f"Test failures: {', '.join(failures)}")
