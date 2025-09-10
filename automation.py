import re
from playwright.async_api import Page, TimeoutError as PlaywrightTimeoutError
from config import general_config
import asyncio
class AutomationService():
    def __init__(self):
        self.config = general_config
    
    async def _get_element(selef, page: Page, selector: str, text: str = None, timeout: int = 15000, wait_visibility: bool = True):
        try:
            if text:
                element = page.locator(selector, has_text=text)
            else:
                element = page.locator(selector)

            if wait_visibility:
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
                login_button = await self._get_element(
                    page,
                    "a.btn.btn-white.mt-5.mx-1.btn-append",
                    text="Acceso para estudiantes y egresados"
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
    
    async def microsft_login(self, page: Page, email: str, password: str):
        try:
            EMAIL_INPUT_ID = "i0116"
            PASSWORD_INPUT_ID = "i0118"
            NEXT_BUTTON_ID = "idSIButton9"
            USERNAME_ERROR_ID = "usernameError"
            PASSWORD_ERROR_ID = "passwordError"
            NO_STAY_SIGNED_IN_ID = "idBtn_Back"
            login_input = await self._get_element(page, f"input#{EMAIL_INPUT_ID}")
            next_button_input = await self._get_element(page, f"input#{NEXT_BUTTON_ID}")
            
            await login_input.fill(email)
                    
            await next_button_input.click()

            try:
                username_error_div = await self._get_element(page, f"div#{USERNAME_ERROR_ID}", wait_visibility=False)
                await username_error_div.wait_for(state='visible', timeout=5000)
                err = (await username_error_div.text_content() or "").strip()
                return {"success": False, "error": err or "Invalid username/email."}
            except PlaywrightTimeoutError:
                pass
            password_input = await self._get_element(page, f"input#{PASSWORD_INPUT_ID}")
            
            await password_input.fill(password)
            
            await next_button_input.click()

            try:
                password_error_div = await self._get_element(page, f"div#{PASSWORD_ERROR_ID}", wait_visibility=False)
                await password_error_div.wait_for(state='visible', timeout=5000)
                err = (await password_error_div.text_content() or "").strip()
                return {"success": False, "error": err or "Invalid password."}
            except PlaywrightTimeoutError:
                pass
            
            no_stay_signed_in_input = await self._get_element(page, f"input#{NO_STAY_SIGNED_IN_ID}")

            await no_stay_signed_in_input.click()
            
            return True
        except PlaywrightTimeoutError as e:
            print(f"Timeout while navigating to login: {e}")
            return None
        except Exception as e:
            print(f"Unexpected error during navigation to login: {e}")
            return None

