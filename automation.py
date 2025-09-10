import re
from playwright.async_api import Page, Expect
from config import general_config

class AutomationService():
    def __init__(self):
        self.config = general_config
        
    async def navigate_to_web(self, page: Page):
        await page.goto(self.config.BANNER_URL)