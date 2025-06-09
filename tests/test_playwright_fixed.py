import os
import asyncio
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.test import override_settings
from django.urls import reverse
from django.contrib.auth.models import User
from asgiref.sync import sync_to_async
from playwright.async_api import async_playwright

class PlaywrightTest(StaticLiveServerTestCase):
    """Test using Playwright which works well on Mac M1"""
    
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        # Create a directory for screenshots if it doesn't exist
        os.makedirs('playwright_screenshots', exist_ok=True)
        
        # Create a test user
        cls.test_user = User.objects.create_user(
            username='playwrightuser',
            email='playwright@example.com',
            password='playwright123'
        )
    
    async def take_browsers_screenshots(self, url, name):
        """Take screenshots with multiple browsers"""
        async with async_playwright() as p:
            # Test with Chromium
            browser = await p.chromium.launch()
            page = await browser.new_page()
            await page.goto(url)
            await page.screenshot(path=f'playwright_screenshots/{name}_chromium.png')
            await browser.close()
            
            # Test with Firefox
            browser = await p.firefox.launch()
            page = await browser.new_page()
            await page.goto(url)
            await page.screenshot(path=f'playwright_screenshots/{name}_firefox.png')
            await browser.close()
            
            # Test with WebKit (Safari engine)
            browser = await p.webkit.launch()
            page = await browser.new_page()
            await page.goto(url)
            await page.screenshot(path=f'playwright_screenshots/{name}_webkit.png')
            await browser.close()
    
    async def test_homepage_all_browsers(self):
        """Test homepage in all browsers"""
        url = f"{self.live_server_url}/"
        await self.take_browsers_screenshots(url, "homepage")
        
    async def test_login_page_all_browsers(self):
        """Test login page in all browsers"""
        url = f"{self.live_server_url}{reverse('accounts:login')}"
        await self.take_browsers_screenshots(url, "login")
    
    async def test_signup_page_all_browsers(self):
        """Test signup page in all browsers"""
        url = f"{self.live_server_url}{reverse('accounts:signup')}"
        await self.take_browsers_screenshots(url, "signup")
    
    async def test_login_flow(self):
        """Test login flow with Playwright"""
        async with async_playwright() as p:
            # Use WebKit (Safari engine) for this test
            browser = await p.webkit.launch()
            page = await browser.new_page()
            
            # Go to login page
            await page.goto(f"{self.live_server_url}{reverse('accounts:login')}")
            await page.screenshot(path='playwright_screenshots/login_start.png')
            
            # Fill in login form
            await page.fill('input[name="username"]', 'playwrightuser')
            await page.fill('input[name="password"]', 'playwright123')
            await page.screenshot(path='playwright_screenshots/login_filled.png')
            
            # Click login button and wait for navigation
            await page.click('button[type="submit"]')
            await page.wait_for_load_state('networkidle')
            await page.screenshot(path='playwright_screenshots/after_login.png')
            
            # Check if we're logged in by looking for common elements
            content = await page.content()
            self.assertTrue(
                'logout' in content.lower() or 
                'dashboard' in content.lower() or 
                'profile' in content.lower(),
                "Login seems to have failed"
            )
            
            await browser.close()
    
    def test_run_async_tests(self):
        """Run the async tests"""
        loop = asyncio.get_event_loop()
        loop.run_until_complete(self.test_homepage_all_browsers())
        loop.run_until_complete(self.test_login_page_all_browsers())
        loop.run_until_complete(self.test_signup_page_all_browsers())
        loop.run_until_complete(self.test_login_flow())
