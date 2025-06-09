import os
import time
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
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException

def generate_random_string(length=8):
    """Generate a random string of fixed length"""
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(length))

class UserFlowLiveTest(StaticLiveServerTestCase):
    """Test the complete user flow from registration to collaboration using LiveServerTestCase"""
    
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        # Set up Chrome options for headless browser
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--window-size=1920,1080")
        
        # Create a driver
        cls.driver = webdriver.Chrome(options=chrome_options)
        cls.driver.implicitly_wait(10)
    
    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()
        super().tearDownClass()
    
    def setUp(self):
        # Generate unique test data
        self.timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        self.admin_user = {
            'username': f'admin{self.timestamp}',
            'email': f'admin{self.timestamp}@example.com',
            'password': 'AdminPass123!',
            'first_name': 'Admin',
            'last_name': 'User'
        }
        self.regular_user = {
            'username': f'user{self.timestamp}',
            'email': f'user{self.timestamp}@example.com',
            'password': 'UserPass123!',
            'first_name': 'Regular',
            'last_name': 'User'
        }
        self.invited_user = {
            'username': f'invited{self.timestamp}',
            'email': f'invited{self.timestamp}@example.com',
            'password': 'InvitedPass123!',
            'first_name': 'Invited',
            'last_name': 'User'
        }
        
        # Test data for workspace, project, team, etc.
        self.workspace_name = f'Live Workspace {self.timestamp}'
        self.project_name = f'Live Project {self.timestamp}'
        self.team_name = f'Live Team {self.timestamp}'
        self.task_name = f'Live Task {self.timestamp}'
        self.subtask_name = f'Live Subtask {self.timestamp}'
    
    def wait_for_element(self, by, value, timeout=10):
        """Wait for an element to be present"""
        try:
            element = WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located((by, value))
            )
            return element
        except TimeoutException:
            self.fail(f"Timed out waiting for element {value}")
    
    def wait_for_url_contains(self, text, timeout=10):
        """Wait for URL to contain specific text"""
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.url_contains(text)
            )
            return True
        except TimeoutException:
            self.fail(f"Timed out waiting for URL to contain {text}")
    
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
    
    def take_screenshot(self, name):
        """Take a screenshot for debugging"""
        self.driver.save_screenshot(f"screenshot_{name}_{self.timestamp}.png")
    
    @override_settings(EMAIL_BACKEND='django.core.mail.backends.locmem.EmailBackend')
    def test_complete_user_flow(self):
        """Test the complete user flow from registration to collaboration"""
        driver = self.driver
        
        # Step 1: Register admin user
        driver.get(f"{self.live_server_url}{reverse('accounts:signup')}")
        
        try:
            # Fill in the form
            self.wait_for_element(By.ID, "id_username").send_keys(self.admin_user['username'])
            self.wait_for_element(By.ID, "id_email").send_keys(self.admin_user['email'])
            self.wait_for_element(By.ID, "id_password1").send_keys(self.admin_user['password'])
            self.wait_for_element(By.ID, "id_password2").send_keys(self.admin_user['password'])
            
            # Submit the form
            self.wait_for_element(By.XPATH, "//button[@type='submit']").click()
            
            # Check for success message or redirect to login
            try:
                success_message = self.wait_for_element(By.CLASS_NAME, "alert-success")
                self.assertIn("account created", success_message.text.lower())
            except:
                # If no success message, check if redirected to login
                self.wait_for_url_contains("login")
        except Exception as e:
            self.take_screenshot("register_admin")
            raise e
        
        # Step 2: Login as admin
        driver.get(f"{self.live_server_url}{reverse('accounts:login')}")
        
        try:
            # Fill in the form
            self.wait_for_element(By.ID, "id_username").send_keys(self.admin_user['username'])
            self.wait_for_element(By.ID, "id_password").send_keys(self.admin_user['password'])
            
            # Submit the form
            self.wait_for_element(By.XPATH, "//button[@type='submit']").click()
            
            # Check that we're redirected to the dashboard or home
            try:
                self.wait_for_url_contains("dashboard")
            except:
                self.wait_for_url_contains("home")
        except Exception as e:
            self.take_screenshot("login_admin")
            raise e
        
        # Step 3: Create workspace
        driver.get(f"{self.live_server_url}{reverse('workspace:create')}")
        
        try:
            # Fill in the form
            self.wait_for_element(By.ID, "id_name").send_keys(self.workspace_name)
            self.wait_for_element(By.ID, "id_description").send_keys(f"Description for {self.workspace_name}")
            
            # Submit the form
            self.wait_for_element(By.XPATH, "//button[@type='submit']").click()
            
            # Check that we're redirected to the workspace detail page
            self.wait_for_url_contains("/workspaces/")
            
            # Extract workspace ID from URL for later use
            current_url = driver.current_url
            self.workspace_id = current_url.split('/')[-2]
        except Exception as e:
            self.take_screenshot("create_workspace")
            raise e
        
        # Step 4: Create team
        driver.get(f"{self.live_server_url}{reverse('teamflow:team-create')}")
        
        try:
            # Fill in the form
            self.wait_for_element(By.ID, "id_name").send_keys(self.team_name)
            
            # Check if URL field exists, if so fill it
            try:
                url_field = driver.find_element(By.ID, "id_url")
                url_field.send_keys(self.team_name.lower().replace(' ', '-'))
            except NoSuchElementException:
                # URL might be auto-generated
                pass
            
            self.wait_for_element(By.ID, "id_description").send_keys(f"Description for {self.team_name}")
            
            # Submit the form
            self.wait_for_element(By.XPATH, "//button[@type='submit']").click()
            
            # Check that we're redirected to the team detail page
            self.wait_for_url_contains("/teams/team/")
            
            # Extract team URL from URL for later use
            current_url = driver.current_url
            self.team_url = current_url.split('/')[-2]
        except Exception as e:
            self.take_screenshot("create_team")
            raise e
        
        # Step 5: Create project in workspace
        driver.get(f"{self.live_server_url}{reverse('projectflow:project-create')}")
        
        try:
            # Fill in the form
            self.wait_for_element(By.ID, "id_name").send_keys(self.project_name)
            self.wait_for_element(By.ID, "id_description").send_keys(f"Description for {self.project_name}")
            
            # Try to select workspace if field exists
            try:
                workspace_select = Select(self.wait_for_element(By.ID, "id_workspace"))
                # Find option containing workspace ID or name
                for i, option in enumerate(workspace_select.options):
                    if self.workspace_id in option.get_attribute("value") or self.workspace_name in option.text:
                        workspace_select.select_by_index(i)
                        break
            except:
                # Workspace selection might not be available
                pass
            
            # Try to select team if field exists
            try:
                team_select = Select(self.wait_for_element(By.ID, "id_team"))
                # Find option containing team URL or name
                for i, option in enumerate(team_select.options):
                    if self.team_url in option.get_attribute("value") or self.team_name in option.text:
                        team_select.select_by_index(i)
                        break
            except:
                # Team selection might not be available
                pass
            
            # Submit the form
            self.wait_for_element(By.XPATH, "//button[@type='submit']").click()
            
            # Check that we're redirected to the project detail page
            self.wait_for_url_contains("/projects/project/")
            
            # Extract project slug from URL for later use
            current_url = driver.current_url
            self.project_slug = current_url.split('/')[-2]
        except Exception as e:
            self.take_screenshot("create_project")
            raise e
        
        # Step 6: Create task in project
        try:
            # Try direct URL first
            driver.get(f"{self.live_server_url}/projects/task/create/?project={self.project_slug}")
        except:
            # Fallback to general task creation
            driver.get(f"{self.live_server_url}{reverse('projectflow:task-create')}")
        
        try:
            # Fill in the form
            self.wait_for_element(By.ID, "id_name").send_keys(self.task_name)
            self.wait_for_element(By.ID, "id_description").send_keys(f"Description for {self.task_name}")
            
            # Try to select project if not pre-selected
            try:
                project_select = Select(self.wait_for_element(By.ID, "id_project"))
                # Find option containing project name
                for i, option in enumerate(project_select.options):
                    if self.project_name in option.text:
                        project_select.select_by_index(i)
                        break
            except:
                # Project might be pre-selected or field might not be visible
                pass
            
            # Submit the form
            self.wait_for_element(By.XPATH, "//button[@type='submit']").click()
            
            # Check that we're redirected to the task detail page
            self.wait_for_url_contains("/projects/task/")
            
            # Extract task ID from URL for later use
            current_url = driver.current_url
            self.task_id = current_url.split('/')[-2]
        except Exception as e:
            self.take_screenshot("create_task")
            raise e
        
        # Step 7: Invite a new user
        try:
            # Navigate to invite page
            driver.get(f"{self.live_server_url}{reverse('accounts:invite_create')}")
            
            # Fill in the form
            self.wait_for_element(By.ID, "id_email").send_keys(self.invited_user['email'])
            
            # Submit the form
            self.wait_for_element(By.XPATH, "//button[@type='submit']").click()
            
            # Check for success message
            try:
                success_message = self.wait_for_element(By.CLASS_NAME, "alert-success")
                self.assertIn("invite", success_message.text.lower())
            except:
                # Success message might not appear, check if redirected to invite list
                self.wait_for_url_contains("invite")
            
            # Check if there are emails in the test outbox
            self.assertGreater(len(mail.outbox), 0, "No emails were sent")
            
            # Find the invite email
            invite_email = None
            for email_obj in mail.outbox:
                if self.invited_user['email'] in email_obj.to:
                    invite_email = email_obj
                    break
            
            self.assertIsNotNone(invite_email, f"No invite email found for {self.invited_user['email']}")
            
            # Extract invite link
            self.invite_link = self.extract_verification_link(invite_email.body)
            self.assertIsNotNone(self.invite_link, "Could not extract invite link")
        except Exception as e:
            self.take_screenshot("invite_user")
            raise e
        
        # Step 8: Logout admin user
        try:
            # Click on user dropdown
            user_dropdown = self.wait_for_element(By.CLASS_NAME, "dropdown-toggle")
            user_dropdown.click()
            
            # Click on logout
            logout_link = self.wait_for_element(By.XPATH, "//a[contains(@href, 'logout')]")
            logout_link.click()
            
            # Check that we're logged out
            self.wait_for_url_contains("login")
        except Exception as e:
            self.take_screenshot("logout_admin")
            # If dropdown navigation fails, try direct logout URL
            driver.get(f"{self.live_server_url}{reverse('accounts:logout')}")
        
        # Step 9: Accept invitation as invited user
        try:
            # Visit the invite link
            driver.get(self.invite_link)
            
            # Fill in the registration form
            try:
                self.wait_for_element(By.ID, "id_username").send_keys(self.invited_user['username'])
                self.wait_for_element(By.ID, "id_password1").send_keys(self.invited_user['password'])
                self.wait_for_element(By.ID, "id_password2").send_keys(self.invited_user['password'])
                
                # Submit the form
                self.wait_for_element(By.XPATH, "//button[@type='submit']").click()
                
                # Check for success or redirect to login
                try:
                    success_message = self.wait_for_element(By.CLASS_NAME, "alert-success")
                    self.assertIn("account created", success_message.text.lower())
                except:
                    # Might redirect directly to login
                    self.wait_for_url_contains("login")
            except:
                # If the above fails, the invite might lead directly to login
                self.wait_for_url_contains("login")
        except Exception as e:
            self.take_screenshot("accept_invitation")
            raise e
        
        # Step 10: Login as invited user
        driver.get(f"{self.live_server_url}{reverse('accounts:login')}")
        
        try:
            # Fill in the form
            self.wait_for_element(By.ID, "id_username").send_keys(self.invited_user['username'])
            self.wait_for_element(By.ID, "id_password").send_keys(self.invited_user['password'])
            
            # Submit the form
            self.wait_for_element(By.XPATH, "//button[@type='submit']").click()
            
            # Check that we're redirected to the dashboard or home
            try:
                self.wait_for_url_contains("dashboard")
            except:
                self.wait_for_url_contains("home")
        except Exception as e:
            self.take_screenshot("login_invited")
            raise e
        
        # Step 11: View project as invited user
        driver.get(f"{self.live_server_url}/projects/project/{self.project_slug}/")
        
        try:
            # Check that project name appears on the page
            project_heading = self.wait_for_element(By.XPATH, "//*[contains(text(), '" + self.project_name + "')]")
            self.assertIsNotNone(project_heading)
        except Exception as e:
            self.take_screenshot("view_project")
            raise e
        
        # Step 12: View task as invited user
        driver.get(f"{self.live_server_url}/projects/task/{self.task_id}/")
        
        try:
            # Check that task name appears on the page
            task_heading = self.wait_for_element(By.XPATH, "//*[contains(text(), '" + self.task_name + "')]")
            self.assertIsNotNone(task_heading)
        except Exception as e:
            self.take_screenshot("view_task")
            raise e
        
        # Test completed successfully
        print(f"User flow test completed successfully with timestamp {self.timestamp}")
        print(f"Created workspace: {self.workspace_name} (ID: {self.workspace_id})")
        print(f"Created team: {self.team_name} (URL: {self.team_url})")
        print(f"Created project: {self.project_name} (Slug: {self.project_slug})")
        print(f"Created task: {self.task_name} (ID: {self.task_id})")
