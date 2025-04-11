import random
import asyncio
from playwright.async_api import async_playwright
import openpyxl
from interaction_logger import setup_logger

class Virtoxed:

    def __init__(self, excel_path: str):
        self.excel_path = excel_path
        self.websites = self.load_websites()
        self.logger = setup_logger()

    def load_websites(self):
        workbook = openpyxl.load_workbook(self.excel_path)
        sheet = workbook.active
        websites = []
        for row in sheet.iter_rows(min_row=2, values_only=True):
            url = row[0]
            if url:
                websites.append(str(url).strip())
        return websites

    async def scroll_to_bottom(self, page, delay=1, max_scrolls=20, site_name="Unknown"):
        for i in range(max_scrolls):
            await page.evaluate("window.scrollBy(0, window.innerHeight);")
            self.logger.info(f"Scrolled down on {site_name} - scroll #{i+1}")
            await asyncio.sleep(delay)

    async def click_button_and_wait(self, page, selector, site_name="Unknown"):
        try:
            await page.click(selector)
            await page.wait_for_load_state('networkidle')
            self.logger.info(f"Clicked button '{selector}' on {site_name}")
        except Exception as e:
            self.logger.error(f"Failed to click on {site_name}: {e}")

    async def handle_interactions(self, page, url):
        if "jamescropper.com" in url:
            await self.scroll_to_bottom(page, site_name="James Cropper")
        elif "code.org" in url:
            await self.scroll_to_bottom(page, site_name="Code")
        elif "ittehad.com.pk" in url:
            await self.click_button_and_wait(page, "#header > div > div > nav > div.header-quote > a", site_name="Ittehad")

    async def visit_multiple_websites(self, browser, urls, browser_id):
        context = await browser.new_context()
        page = await context.new_page()
        try:
            for url in urls:
                self.logger.info(f"[Browser-{browser_id}] Visiting: {url}")
                await page.goto(url, wait_until='domcontentloaded', timeout=30000)
                r_wait=random.randint(1,5)
                await asyncio.sleep(r_wait)
                self.logger(f"Waiting for {r_wait} to open website")
                await self.handle_interactions(page, url)
                await asyncio.sleep(5)
        except Exception as e:
            self.logger.error(f"[Browser-{browser_id}] Error while visiting sites: {e}")
        finally:
            await context.close()

    async def launch_concurrent_visits(self, instances=10):
        async with async_playwright() as playwright:
            browser1 = await playwright.chromium.launch(headless=False)
            browser2 = await playwright.chromium.launch(headless=False)

            tasks = []
            for i in range(instances):
                random_urls = random.sample(self.websites, k=3)
                browser = browser1 if i < instances // 2 else browser2
                browser_id = 1 if browser == browser1 else 2
                tasks.append(self.visit_multiple_websites(browser, random_urls, browser_id))

            await asyncio.gather(*tasks)

            await browser1.close()
            await browser2.close()

if __name__ == "__main__":
    launcher = Virtoxed("sites.xlsx")
    asyncio.run(launcher.launch_concurrent_visits())