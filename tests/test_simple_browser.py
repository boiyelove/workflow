import os
import time
from django.test import LiveServerTestCase
from django.contrib.auth.models import User
from django.urls import reverse
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

class SimpleBrowserTest(LiveServerTestCase):
    """Simple browser tests that work on Mac M1"""
    
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        # Set up Chrome options for headless browser
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        
        # Create a Chrome driver
        cls.driver = webdriver.Chrome(options=chrome_options)
        cls.driver.implicitly_wait(10)
        
        # Create a test user
        cls.test_user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpassword123'
        )
        
        # Create a directory for screenshots
        os.makedirs('screenshots', exist_ok=True)
    
    @classmethod
    def tearDownClass(cls):
        if hasattr(cls, 'driver'):
            cls.driver.quit()
        super().tearDownClass()
    
    def wait_for_element(self, by, value, timeout=10):
        """Wait for an element to be present"""
        try:
            element = WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located((by, value))
            )
            return element
        except TimeoutException:
            # Take screenshot on timeout
            self.driver.save_screenshot(f'screenshots/timeout_{value}.png')
            self.fail(f"Timed out waiting for element {value}")
    
    def test_homepage_loads(self):
        """Test that the homepage loads"""
        self.driver.get(self.live_server_url)
        self.driver.save_screenshot('screenshots/homepage.png')
        
        # Check that we're either on the homepage or redirected to login
        current_url = self.driver.current_url
        self.assertTrue(
            self.live_server_url in current_url or 'login' in current_url,
            f"Expected homepage or login redirect, got: {current_url}"
        )
    
    def test_login_page_loads(self):
        """Test that the login page loads"""
        self.driver.get(f"{self.live_server_url}{reverse('accounts:login')}")
        self.driver.save_screenshot('screenshots/login_page.png')
        
        # Check for username field
        username_field = self.wait_for_element(By.NAME, "username")
        self.assertIsNotNone(username_field)
        
        # Check for password field
        password_field = self.wait_for_element(By.NAME, "password")
        self.assertIsNotNone(password_field)
        
        # Check for login button
        login_button = self.wait_for_element(By.XPATH, "//button[@type='submit']")
        self.assertIsNotNone(login_button)
    
    def test_login_works(self):
        """Test that login works"""
        self.driver.get(f"{self.live_server_url}{reverse('accounts:login')}")
        
        # Fill in the login form
        username_field = self.wait_for_element(By.NAME, "username")
        username_field.send_keys('testuser')
        
        password_field = self.wait_for_element(By.NAME, "password")
        password_field.send_keys('testpassword123')
        
        # Take screenshot before submitting
        self.driver.save_screenshot('screenshots/before_login.png')
        
        # Submit the form
        login_button = self.wait_for_element(By.XPATH, "//button[@type='submit']")
        login_button.click()
        
        # Wait a moment for the page to load
        time.sleep(2)
        
        # Take screenshot after login
        self.driver.save_screenshot('screenshots/after_login.png')
        
        # Check that we're logged in by looking for common elements
        page_source = self.driver.page_source.lower()
        self.assertTrue(
            'logout' in page_source or 
            'dashboard' in page_source or 
            'profile' in page_source or
            'welcome' in page_source,
            "Login seems to have failed"
        )
    
    def test_signup_page_loads(self):
        """Test that the signup page loads"""
        self.driver.get(f"{self.live_server_url}{reverse('accounts:signup')}")
        self.driver.save_screenshot('screenshots/signup_page.png')
        
        # Check for username field
        username_field = self.wait_for_element(By.NAME, "username")
        self.assertIsNotNone(username_field)
        
        # Check for email field
        email_field = self.wait_for_element(By.NAME, "email")
        self.assertIsNotNone(email_field)
        
        # Check for password fields
        password1_field = self.wait_for_element(By.NAME, "password1")
        self.assertIsNotNone(password1_field)
        
        password2_field = self.wait_for_element(By.NAME, "password2")
        self.assertIsNotNone(password2_field)
        
        # Check for signup button
        signup_button = self.wait_for_element(By.XPATH, "//button[@type='submit']")
        self.assertIsNotNone(signup_button)
