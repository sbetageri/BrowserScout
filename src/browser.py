import io
import base64
import asyncio

from PIL import Image
from playwright.async_api import async_playwright

import utils
import constants


class Browser:
    CLICKABLE_ITEMS = {
        constants.BUTTON,
        constants.CHECKBOX,
        constants.LINK,
        constants.MENU,
        constants.MENU_BAR,
        constants.MENU_ITEM,
        constants.MENU_ITEM_CHECKBOX,
        constants.MENU_ITEM_RADIO,
        constants.NAVIGATION,
        constants.RADIO,
        constants.RADIO_GROUP,
        constants.SEARCH,
        constants.SEARCH_BOX,
        constants.SPIN_BUTTON,
        constants.TEXTBOX,
    }

    def __init__(self, headless: bool = True):
        self.playwright = None
        self.browser = None
        self.headless = headless
        self.opened_page = None

    async def setup_playwright_browser(self):
        """
        Setup the browser
        :return:
        """
        self.playwright = await async_playwright().start()
        self.browser = await self.playwright.chromium.launch(headless=self.headless)

    async def cleanup(self):
        """
        Cleanup any resources used
        :return:
        """
        if self.browser is not None:
            await self.browser.close()

        if self.playwright is not None:
            await self.playwright.stop()

    async def open_page(self, url: str):
        """Open the given page"""
        self.opened_page = await self.browser.new_page()
        await self.opened_page.goto(url)

    async def _find_all_clickable_locators(self):
        """Identify all locators in the page that correspond to an input element"""
        input_locators = []
        if self.opened_page is None:
            raise ValueError("No open page available")

        for clickable_item in Browser.CLICKABLE_ITEMS:
            locator = self.opened_page.get_by_role(clickable_item).filter(visible=True)
            input_locators.append(locator)

        return input_locators

    async def _get_screenshot(self) -> Image:
        """Save screenshot at the path provided"""
        screenshot_bytes = await self.opened_page.screenshot()
        image_bytes = base64.b64decode(screenshot_bytes)
        img = Image.open(io.BytesIO(image_bytes))
        return img

    async def _get_all_locatos_in_screen(self):
        """Get all the locators visible in the viewport"""
        screenshot = await self._get_screenshot()
        clickable_locators = await self._find_all_clickable_locators()
        bbox_values = []
        for locator in clickable_locators:
            bbox = await locator.bounding_box()


async def main():
    try:
        browser = Browser(headless=False)
        utils.print("Setting up browser")
        await browser.setup_playwright_browser()
        utils.print("Browser setup complete")
        await browser.open_page("https://www.google.com")
        await browser._find_all_clickable_locators()
        while True:
            continue
    except Exception as ex:
        utils.print(ex)
        utils.print("Exiting")
    finally:
        await browser.cleanup()


if __name__ == "__main__":
    asyncio.run(main())
