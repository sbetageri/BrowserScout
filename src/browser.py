import asyncio

from playwright.async_api import async_playwright, playwright

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
        constants.TEXTBOX
    }
    def __init__(self, headless: bool=True):
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
            self.browser.close()

        if self.playwright is not None:
            self.playwright.stop()

    async def open_page(self, url: str):
        """Open the given page"""
        self.opened_page = await self.browser.new_page()
        await self.opened_page.goto(url)

    async def find_all_input_locators(self, url: str=None):
        """Identify all locators in the page that correspond to an input element"""
        if url is not None:
            await self.open_page(url)

        



async def main():
    try:
        browser = Browser(headless=False)
        utils.print("Setting up browser")
        await browser.setup_playwright_browser()
        utils.print("Browser setup complete")
        await browser.open_page("https://www.google.com")
        while True:
            continue
    except:
        utils.print("Exiting")
    finally:
        browser.cleanup()


if __name__ == "__main__":
    asyncio.run(main())