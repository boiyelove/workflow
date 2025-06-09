import os
import time
import re
import logging
from urllib.parse import urljoin, urlparse
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.contrib.auth.models import User
from django.urls import reverse
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.safari.options import Options as SafariOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException, WebDriverException

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    filename='liveserver_test.log'
)
logger = logging.getLogger(__name__)

class LiveServerCrawlerTest(StaticLiveServerTestCase):
    """Test that crawls through the entire website checking links and buttons"""
    
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        
        # Create a directory for screenshots
        os.makedirs('crawler_screenshots', exist_ok=True)
        
        # Set up Chrome options for headless browser
        cls.chrome_options = ChromeOptions()
        cls.chrome_options.add_argument("--headless")
        cls.chrome_options.add_argument("--no-sandbox")
        cls.chrome_options.add_argument("--disable-dev-shm-usage")
        cls.chrome_options.add_argument("--window-size=1920,1080")
        
        # Try to set up Chrome driver
        try:
            from webdriver_manager.chrome import ChromeDriverManager
            from selenium.webdriver.chrome.service import Service as ChromeService
            cls.chrome_driver = webdriver.Chrome(
                service=ChromeService(ChromeDriverManager().install()),
                options=cls.chrome_options
            )
            cls.browsers = ['chrome']
            logger.info("Chrome driver initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize Chrome driver: {e}")
            cls.chrome_driver = None
            cls.browsers = []
        
        # Try to set up Safari driver if on macOS
        try:
            cls.safari_options = SafariOptions()
            cls.safari_driver = webdriver.Safari(options=cls.safari_options)
            cls.browsers.append('safari')
            logger.info("Safari driver initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize Safari driver: {e}")
            cls.safari_driver = None
        
        # Create test users
        cls.admin_user = User.objects.create_superuser(
            username='admin_crawler',
            email='admin_crawler@example.com',
            password='AdminPass123!'
        )
        
        cls.regular_user = User.objects.create_user(
            username='user_crawler',
            email='user_crawler@example.com',
            password='UserPass123!'
        )
        
        # Initialize visited links set
        cls.visited_links = set()
        cls.broken_links = set()
        cls.skipped_links = set()
        
        logger.info(f"LiveServerCrawlerTest setup complete with browsers: {cls.browsers}")
    
    @classmethod
    def tearDownClass(cls):
        # Quit all drivers
        if hasattr(cls, 'chrome_driver') and cls.chrome_driver:
            cls.chrome_driver.quit()
        
        if hasattr(cls, 'safari_driver') and cls.safari_driver:
            cls.safari_driver.quit()
        
        # Log summary
        logger.info(f"Total links visited: {len(cls.visited_links)}")
        logger.info(f"Total broken links: {len(cls.broken_links)}")
        logger.info(f"Total skipped links: {len(cls.skipped_links)}")
        
        if cls.broken_links:
            logger.error(f"Broken links: {cls.broken_links}")
        
        if cls.skipped_links:
            logger.info(f"Skipped links: {cls.skipped_links}")
        
        super().tearDownClass()
    
    def get_driver(self, browser_name):
        """Get the appropriate driver based on browser name"""
        if browser_name == 'chrome' and self.chrome_driver:
            return self.chrome_driver
        elif browser_name == 'safari' and self.safari_driver:
            return self.safari_driver
        else:
            self.fail(f"Browser {browser_name} not available")
    
    def wait_for_element(self, driver, by, value, timeout=10):
        """Wait for an element to be present"""
        try:
            element = WebDriverWait(driver, timeout).until(
                EC.presence_of_element_located((by, value))
            )
            return element
        except TimeoutException:
            # Take screenshot on timeout
            self.take_screenshot(driver, f"timeout_{value}")
            logger.error(f"Timed out waiting for element {value}")
            return None
    
    def take_screenshot(self, driver, name):
        """Take a screenshot with the given name"""
        try:
            timestamp = time.strftime("%Y%m%d-%H%M%S")
            filename = f"crawler_screenshots/{name}_{timestamp}.png"
            driver.save_screenshot(filename)
            logger.info(f"Screenshot saved: {filename}")
        except Exception as e:
            logger.error(f"Failed to take screenshot: {e}")
    
    def is_valid_link(self, link):
        """Check if a link is valid for crawling"""
        # Skip external links
        if not link.startswith(self.live_server_url):
            return False
        
        # Skip already visited links
        if link in self.visited_links:
            return False
        
        # Skip links with fragments
        if '#' in link:
            return False
        
        # Skip logout links to avoid ending the session
        if 'logout' in link:
            return False
        
        # Skip file downloads
        if any(ext in link for ext in ['.pdf', '.zip', '.csv', '.xlsx']):
            return False
        
        return True
    
    def extract_links(self, driver):
        """Extract all links from the current page"""
        links = []
        try:
            # Get all anchor tags
            elements = driver.find_elements(By.TAG_NAME, "a")
            for element in elements:
                try:
                    href = element.get_attribute("href")
                    if href and href.strip():
                        # Convert to absolute URL
                        absolute_url = urljoin(driver.current_url, href)
                        links.append(absolute_url)
                except Exception as e:
                    logger.error(f"Error extracting link: {e}")
        except Exception as e:
            logger.error(f"Error finding links: {e}")
        
        return links
    
    def find_clickable_elements(self, driver):
        """Find all clickable elements on the page"""
        clickables = []
        
        # Find buttons
        try:
            buttons = driver.find_elements(By.TAG_NAME, "button")
            clickables.extend(buttons)
        except Exception as e:
            logger.error(f"Error finding buttons: {e}")
        
        # Find inputs of type submit
        try:
            submits = driver.find_elements(By.XPATH, "//input[@type='submit']")
            clickables.extend(submits)
        except Exception as e:
            logger.error(f"Error finding submit inputs: {e}")
        
        # Find elements with click-related classes
        try:
            click_classes = driver.find_elements(By.CSS_SELECTOR, ".btn, .button, [role='button']")
            clickables.extend(click_classes)
        except Exception as e:
            logger.error(f"Error finding elements with click classes: {e}")
        
        return clickables
    
    def login(self, driver, username, password):
        """Login with the given credentials"""
        try:
            # Navigate to login page
            driver.get(f"{self.live_server_url}{reverse('accounts:login')}")
            
            # Fill in the login form
            username_field = self.wait_for_element(driver, By.NAME, "username")
            if username_field:
                username_field.send_keys(username)
            
            password_field = self.wait_for_element(driver, By.NAME, "password")
            if password_field:
                password_field.send_keys(password)
            
            # Take screenshot before submitting
            self.take_screenshot(driver, f"before_login_{username}")
            
            # Submit the form
            login_button = self.wait_for_element(driver, By.XPATH, "//button[@type='submit']")
            if login_button:
                login_button.click()
            
            # Wait a moment for the page to load
            time.sleep(2)
            
            # Take screenshot after login
            self.take_screenshot(driver, f"after_login_{username}")
            
            # Check if login was successful
            if "login" not in driver.current_url.lower():
                logger.info(f"Login successful for {username}")
                return True
            else:
                logger.warning(f"Login may have failed for {username}, still on login page")
                return False
        except Exception as e:
            logger.error(f"Error during login: {e}")
            return False
    
    def crawl_page(self, driver, url, depth=0, max_depth=3):
        """Crawl a page and its links up to max_depth"""
        if depth > max_depth:
            return
        
        if not self.is_valid_link(url):
            if url not in self.visited_links and url not in self.skipped_links:
                self.skipped_links.add(url)
                logger.info(f"Skipping link: {url}")
            return
        
        logger.info(f"Crawling: {url} (depth {depth})")
        
        try:
            # Navigate to the URL
            driver.get(url)
            self.visited_links.add(url)
            
            # Take screenshot
            page_name = urlparse(url).path.replace('/', '_') or 'home'
            self.take_screenshot(driver, f"page_{page_name}")
            
            # Test clickable elements
            clickables = self.find_clickable_elements(driver)
            logger.info(f"Found {len(clickables)} clickable elements on {url}")
            
            # Try clicking on a few elements (limited to avoid infinite loops)
            for i, element in enumerate(clickables[:5]):  # Limit to first 5 elements
                try:
                    # Save current URL to navigate back
                    current_url = driver.current_url
                    
                    # Scroll element into view
                    driver.execute_script("arguments[0].scrollIntoView(true);", element)
                    time.sleep(0.5)
                    
                    # Take screenshot before clicking
                    self.take_screenshot(driver, f"before_click_{page_name}_{i}")
                    
                    # Click the element
                    element.click()
                    time.sleep(1)
                    
                    # Take screenshot after clicking
                    self.take_screenshot(driver, f"after_click_{page_name}_{i}")
                    
                    # Go back to the original page
                    driver.get(current_url)
                    time.sleep(1)
                except Exception as e:
                    logger.warning(f"Could not click element {i} on {url}: {e}")
            
            # Extract links for further crawling
            links = self.extract_links(driver)
            logger.info(f"Found {len(links)} links on {url}")
            
            # Recursively crawl links
            for link in links:
                if self.is_valid_link(link):
                    self.crawl_page(driver, link, depth + 1, max_depth)
        
        except Exception as e:
            logger.error(f"Error crawling {url}: {e}")
            self.broken_links.add(url)
            self.take_screenshot(driver, f"error_{urlparse(url).path.replace('/', '_')}")
    
    def test_crawl_as_anonymous(self):
        """Test crawling the site as an anonymous user"""
        for browser_name in self.browsers:
            logger.info(f"Starting anonymous crawl with {browser_name}")
            driver = self.get_driver(browser_name)
            
            # Reset visited links for this test
            self.__class__.visited_links = set()
            self.__class__.broken_links = set()
            self.__class__.skipped_links = set()
            
            # Start crawling from the home page
            self.crawl_page(driver, self.live_server_url, max_depth=2)
            
            # Log results
            logger.info(f"Anonymous crawl with {browser_name} complete")
            logger.info(f"Visited {len(self.visited_links)} pages")
            logger.info(f"Found {len(self.broken_links)} broken links")
    
    def test_crawl_as_user(self):
        """Test crawling the site as a regular user"""
        for browser_name in self.browsers:
            logger.info(f"Starting user crawl with {browser_name}")
            driver = self.get_driver(browser_name)
            
            # Reset visited links for this test
            self.__class__.visited_links = set()
            self.__class__.broken_links = set()
            self.__class__.skipped_links = set()
            
            # Login first
            if self.login(driver, 'user_crawler', 'UserPass123!'):
                # Start crawling from the home page
                self.crawl_page(driver, self.live_server_url, max_depth=2)
                
                # Log results
                logger.info(f"User crawl with {browser_name} complete")
                logger.info(f"Visited {len(self.visited_links)} pages")
                logger.info(f"Found {len(self.broken_links)} broken links")
            else:
                logger.error(f"Login failed for user_crawler with {browser_name}, skipping crawl")
    
    def test_crawl_as_admin(self):
        """Test crawling the site as an admin user"""
        for browser_name in self.browsers:
            logger.info(f"Starting admin crawl with {browser_name}")
            driver = self.get_driver(browser_name)
            
            # Reset visited links for this test
            self.__class__.visited_links = set()
            self.__class__.broken_links = set()
            self.__class__.skipped_links = set()
            
            # Login first
            if self.login(driver, 'admin_crawler', 'AdminPass123!'):
                # Start crawling from the home page
                self.crawl_page(driver, self.live_server_url, max_depth=2)
                
                # Also crawl the admin site
                admin_url = f"{self.live_server_url}/admin/"
                self.crawl_page(driver, admin_url, max_depth=2)
                
                # Log results
                logger.info(f"Admin crawl with {browser_name} complete")
                logger.info(f"Visited {len(self.visited_links)} pages")
                logger.info(f"Found {len(self.broken_links)} broken links")
            else:
                logger.error(f"Login failed for admin_crawler with {browser_name}, skipping crawl")
