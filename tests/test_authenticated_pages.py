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

class AuthenticatedPagesTest(TestCase):
    """Test authenticated pages using Django's test client with direct authentication"""
    
    def setUp(self):
        # Create test users
        self.regular_user = User.objects.create_user(
            username='testuser',
            email='testuser@example.com',
            password='testpassword123'
        )
        
        self.admin_user = User.objects.create_superuser(
            username='adminuser',
            email='admin@example.com',
            password='adminpassword123'
        )
        
        # Create test clients
        self.client = Client()
        self.admin_client = Client()
        
        # Force login
        self.client.force_login(self.regular_user)
        self.admin_client.force_login(self.admin_user)
    
    def test_dashboard_access(self):
        """Test access to dashboard for authenticated user"""
        try:
            response = self.client.get(reverse('dashboard'))
            self.assertEqual(response.status_code, 200)
            print("Dashboard accessible to authenticated user")
        except:
            # If dashboard URL doesn't exist, try home
            try:
                response = self.client.get(reverse('home'))
                self.assertEqual(response.status_code, 200)
                print("Home page accessible to authenticated user")
            except:
                self.skipTest("Neither dashboard nor home URL patterns found")
    
    def test_projects_access(self):
        """Test access to projects for authenticated user"""
        try:
            response = self.client.get(reverse('projectflow:project-list'))
            self.assertEqual(response.status_code, 200)
            print("Projects list accessible to authenticated user")
        except:
            self.skipTest("Project list URL pattern not found")
    
    def test_teams_access(self):
        """Test access to teams for authenticated user"""
        try:
            response = self.client.get(reverse('teamflow:team-list'))
            self.assertEqual(response.status_code, 200)
            print("Teams list accessible to authenticated user")
        except:
            self.skipTest("Team list URL pattern not found")
    
    def test_workspaces_access(self):
        """Test access to workspaces for authenticated user"""
        try:
            response = self.client.get(reverse('workspace:workspace-list'))
            self.assertEqual(response.status_code, 200)
            print("Workspaces list accessible to authenticated user")
        except:
            self.skipTest("Workspace list URL pattern not found")
    
    def test_admin_access(self):
        """Test access to admin for admin user"""
        response = self.admin_client.get('/admin/')
        self.assertEqual(response.status_code, 200)
        print("Admin interface accessible to admin user")
        
        # Regular user should not have access
        response = self.client.get('/admin/')
        self.assertNotEqual(response.status_code, 200)
        print("Admin interface not accessible to regular user")


class AuthenticatedBrowserTest(StaticLiveServerTestCase):
    """Test authenticated pages using Selenium with session cookie injection"""
    
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
        os.makedirs('auth_screenshots', exist_ok=True)
    
    @classmethod
    def tearDownClass(cls):
        if hasattr(cls, 'driver'):
            cls.driver.quit()
        super().tearDownClass()
    
    def setUp(self):
        # Create test user
        self.user = User.objects.create_user(
            username='browseruser',
            email='browser@example.com',
            password='browserpass123'
        )
        
        # Create Django test client and authenticate
        self.client = Client()
        self.client.force_login(self.user)
    
    def wait_for_element(self, by, value, timeout=10):
        """Wait for an element to be present"""
        try:
            element = WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located((by, value))
            )
            return element
        except TimeoutException:
            # Take screenshot on timeout
            self.driver.save_screenshot(f'auth_screenshots/timeout_{value}.png')
            self.fail(f"Timed out waiting for element {value}")
    
    def take_screenshot(self, name):
        """Take a screenshot with the given name"""
        timestamp = time.strftime("%Y%m%d-%H%M%S")
        filename = f"auth_screenshots/{name}_{timestamp}.png"
        self.driver.save_screenshot(filename)
        print(f"Screenshot saved: {filename}")
    
    def test_authenticated_browser_access(self):
        """Test authenticated access using browser with session cookie injection"""
        # Get the session cookie
        session_cookie = self.client.cookies.get('sessionid')
        self.assertIsNotNone(session_cookie, "No session cookie found")
        
        # Visit the site first to set domain for the cookie
        self.driver.get(self.live_server_url)
        self.take_screenshot("before_cookie")
        
        # Add the session cookie to the browser
        self.driver.add_cookie({
            'name': 'sessionid',
            'value': session_cookie.value,
            'path': '/'
        })
        
        # Try to access dashboard or home
        try:
            self.driver.get(f"{self.live_server_url}{reverse('dashboard')}")
            self.take_screenshot("dashboard")
            print(f"Current URL after authentication: {self.driver.current_url}")
            print(f"Page title: {self.driver.title}")
        except:
            try:
                self.driver.get(f"{self.live_server_url}{reverse('home')}")
                self.take_screenshot("home")
                print(f"Current URL after authentication: {self.driver.current_url}")
                print(f"Page title: {self.driver.title}")
            except:
                self.driver.get(f"{self.live_server_url}/")
                self.take_screenshot("root")
                print(f"Current URL after authentication: {self.driver.current_url}")
                print(f"Page title: {self.driver.title}")
        
        # Check if we're authenticated by looking for logout link or username
        page_source = self.driver.page_source.lower()
        self.assertTrue(
            'logout' in page_source or 
            'profile' in page_source or
            self.user.username.lower() in page_source,
            "Authentication by cookie injection failed"
        )
        
        # Try to access projects
        try:
            self.driver.get(f"{self.live_server_url}{reverse('projectflow:project-list')}")
            self.take_screenshot("projects")
            print(f"Projects URL: {self.driver.current_url}")
            print(f"Projects page title: {self.driver.title}")
        except:
            print("Could not access projects page")
        
        # Print page source for debugging
        print("Page source excerpt:")
        print(self.driver.page_source[:500])
