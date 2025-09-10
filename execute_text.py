from automation import AutomationService
from playwright.async_api import async_playwright
import asyncio
automation_service = AutomationService()

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        page = await browser.new_page()
        await automation_service.navigate_to_login(page)
        
asyncio.run(main())