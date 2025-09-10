import re
from playwright.async_api import Page, TimeoutError as PlaywrightTimeoutError
from config import general_config
import asyncio
class AutomationService():
    def __init__(self):
        self.config = general_config
    
    async def _get_element(selef, page: Page, selector: str, text: str = None, timeout: int = 15000):
        try:
            if text:
                element = page.locator(selector, has_text=text)
            else:
                element = page.locator(selector)

            await element.wait_for(state="visible", timeout=timeout)
            return element

        except PlaywrightTimeoutError:
            print(f"Timeout: Element '{selector}' with text '{text}' not found within {timeout/1000:.1f}s.")
            return None
        except Exception as e:
            print(f"Unexpected error while searching for '{selector}' with text '{text}': {e}")
            return None
    
    async def navigate_to_login(self, page: Page):
        try:
            await page.goto(self.config.BANNER_URL)
            async with page.expect_popup() as popup_info:
                login_button = self._get_element(
                    page,
                    "a.btn.btn-white.mt-5.mx-1.btn-append",
                    has_text="Acceso para estudiantes y egresados"
                )

                await login_button.click()
                
            new_page = await popup_info.value
            await new_page.wait_for_load_state("domcontentloaded")
            return new_page
        except PlaywrightTimeoutError as e:
            print(f"Timeout while navigating to login: {e}")
            return None
        except Exception as e:
            print(f"Unexpected error during navigation to login: {e}")
            return None



