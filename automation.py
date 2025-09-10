import re
from playwright.async_api import Page, Expect
from config import general_config

class AutomationService():
    def __init__(self):
        self.config = general_config
        
    async def navigate_to_login(self, page: Page):
        await page.goto(self.config.BANNER_URL)
        async with page.expect_popup() as popup_info:
            login_button = page.locator(
                "a.btn.btn-white.mt-5.mx-1.btn-append",
                has_text="Acceso para estudiantes y egresados"
            )

            await login_button.wait_for(state="visible", timeout=15000)

            await login_button.click()
            
        new_page = await popup_info.value
        await new_page.wait_for_load_state("domcontentloaded")