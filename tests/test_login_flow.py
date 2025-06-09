import os
import time
from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

class LoginFlowTest(StaticLiveServerTestCase):
    """Test the login flow with the fixed login view"""
    
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        # Set up Chrome options for headless browser
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--window-size=1920,1080")
        
        # Use webdriver_manager to get the correct ChromeDriver
        from webdriver_manager.chrome import ChromeDriverManager
        from selenium.webdriver.chrome.service import Service as ChromeService
        
        # Create a Chrome driver
        cls.driver = webdriver.Chrome(
            service=ChromeService(ChromeDriverManager().install()),
            options=chrome_options
        )
        cls.driver.implicitly_wait(10)
        
        # Create a directory for screenshots
        os.makedirs('login_test_screenshots', exist_ok=True)
    
    @classmethod
    def tearDownClass(cls):
        if hasattr(cls, 'driver'):
            cls.driver.quit()
        super().tearDownClass()
    
    def setUp(self):
        # Create test user
        self.user = User.objects.create_user(
            username='loginuser',
            email='login@example.com',
            password='loginpass123'
        )
    
    def wait_for_element(self, by, value, timeout=10):
        """Wait for an element to be present"""
        try:
            element = WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located((by, value))
            )
            return element
        except TimeoutException:
            # Take screenshot on timeout
            self.driver.save_screenshot(f'login_test_screenshots/timeout_{value}.png')
            self.fail(f"Timed out waiting for element {value}")
    
    def take_screenshot(self, name):
        """Take a screenshot with the given name"""
        timestamp = time.strftime("%Y%m%d-%H%M%S")
        filename = f"login_test_screenshots/{name}_{timestamp}.png"
        self.driver.save_screenshot(filename)
        print(f"Screenshot saved: {filename}")
    
    def test_login_flow(self):
        """Test the login flow with the fixed login view"""
        # Navigate to login page
        self.driver.get(f"{self.live_server_url}{reverse('accounts:login')}")
        self.take_screenshot("login_page")
        
        # Fill in the login form
        username_field = self.wait_for_element(By.NAME, "username")
        username_field.send_keys('loginuser')
        
        password_field = self.wait_for_element(By.NAME, "password")
        password_field.send_keys('loginpass123')
        
        # Take screenshot before submitting
        self.take_screenshot("before_submit")
        
        # Submit the form
        login_button = self.wait_for_element(By.XPATH, "//button[@type='submit']")
        login_button.click()
        
        # Wait a moment for the page to load
        time.sleep(2)
        
        # Take screenshot after login
        self.take_screenshot("after_login")
        
        # Print current URL and title for debugging
        print(f"Current URL after login: {self.driver.current_url}")
        print(f"Page title after login: {self.driver.title}")
        
        # Check that we're redirected to the home page
        self.assertNotIn('login', self.driver.current_url, "Still on login page - login failed")
        
        # Check for welcome message
        page_source = self.driver.page_source.lower()
        self.assertIn('welcome', page_source, "Welcome message not found")
        
        # Check for logout link (indicating we're logged in)
        self.assertIn('logout', page_source, "Logout link not found - not logged in")
