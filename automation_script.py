import random
import asyncio
import time

from playwright.async_api import async_playwright
import openpyxl
from interaction_logger import InteractionLogger

USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.111 Safari/537.36",
    "Mozilla/5.0 (X11; CrOS x86_64 8172.45.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.64 Safari/537.36"
]

GEO_LOCATIONS = [
    {"latitude": 37.7749, "longitude": -122.4194},  # San Francisco
    {"latitude": 48.8566, "longitude": 2.3522},     # Paris
    {"latitude": 35.6895, "longitude": 139.6917}    # Tokyo
]

class Virtoxed:

    def __init__(self, excel_path: str, log_format='json'):
        self.excel_path = excel_path
        self.websites = self.load_websites()
        self.logger = InteractionLogger(format=log_format)

    def load_websites(self):
        workbook = openpyxl.load_workbook(self.excel_path)
        sheet = workbook.active
        websites = []
        for row in sheet.iter_rows(min_row=2, values_only=True):
            url = row[0]
            if url:
                websites.append(str(url).strip())
        return websites

    async def scroll_to_bottom(self, page, url, browser_id, delay=1, max_scrolls=20):
        for i in range(max_scrolls):
            await page.evaluate("window.scrollBy(0, window.innerHeight);")
            await asyncio.sleep(delay)
        self.logger.log(browser_id, url, "scroll", f"scroll")

    async def click_button_and_wait(self, page, url, browser_id, selector="#header > div > div > nav > div.header-quote > a"):
        try:
            await page.click(selector)
            await page.wait_for_load_state('networkidle')
            self.logger.log(browser_id, url, "click", f"Clicked '{selector}'")
        except Exception as e:
            self.logger.log(browser_id, url, "click_failed", str(e))


    async def handle_interactions(self, page, url, browser_id):
        if "jamescropper.com" in url:
            await self.scroll_to_bottom(page, url, browser_id)
        elif "code.org" in url:
            await self.scroll_to_bottom(page, url, browser_id)
        elif "ittehad.com.pk" in url:
            await self.click_button_and_wait(page, url, browser_id)

    async def visit_multiple_websites(self, browser, urls, browser_id):
        user_agent = random.choice(USER_AGENTS)
        geo = random.choice(GEO_LOCATIONS)

        context = await browser.new_context(
            user_agent=user_agent,
            viewport={"width": 1920, "height": 1080},
            geolocation=geo,
            permissions=["geolocation"]
        )
        page = await context.new_page()

        try:
            for url in urls:
                start = time.time()
                await page.goto(url, wait_until='domcontentloaded', timeout=30000)
                self.logger.log(browser_id, url, "visit", f"UA: {user_agent}, GEO: {geo}")
                await asyncio.sleep(random.randint(5,10))
                await self.handle_interactions(page, url, browser_id)
                end = time.time()
                time_spent = end - start
                self.logger.log(browser_id, url, "time_spent", time_spent=f"{str(time_spent)}s")
        except Exception as e:
            self.logger.log(browser_id, url, "visit_failed", str(e))
        finally:
            await context.close()

    async def launch_concurrent_visits(self, instances=10):
        async with async_playwright() as playwright:
            browser1 = await playwright.chromium.launch(headless=False)
            browser2 = await playwright.chromium.launch(headless=False)

            tasks = []
            for i in range(instances):
                urls = random.sample(self.websites, k=3)
                browser = browser1 if i < instances // 2 else browser2
                browser_id = f"Browser-{1 if browser == browser1 else 2}"
                tasks.append(self.visit_multiple_websites(browser, urls, browser_id))

            await asyncio.gather(*tasks)

            await browser1.close()
            await browser2.close()


if __name__ == "__main__":
    launcher = Virtoxed("sites.xlsx", log_format='json')  # or 'csv'
    asyncio.run(launcher.launch_concurrent_visits(instances=10))