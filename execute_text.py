from automation import AutomationService
from playwright.async_api import async_playwright
from config import general_config
import asyncio
automation_service = AutomationService()

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        page = await browser.new_page()
        login_page = await automation_service.navigate_to_login(page)
        await automation_service.microsft_login(login_page, general_config.TEST_EMAIL, general_config.TEST_PASSWORD)
        
asyncio.run(main())