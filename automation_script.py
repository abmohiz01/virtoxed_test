import random
import asyncio
from playwright.async_api import async_playwright
import openpyxl

class Virtoxed:

    def __init__(self, excel_path: str):
        self.excel_path = excel_path
        self.websites = self.load_websites()

    def load_websites(self):
        workbook = openpyxl.load_workbook(self.excel_path)
        sheet = workbook.active
        websites = []

        for row in sheet.iter_rows(min_row=2, values_only=True):
            url = row[0]  # Assuming URLs are in the first column (A)
            if url:
                websites.append(str(url).strip())

        return websites

    async def visit_multiple_websites(self, browser, urls):
        context = await browser.new_context()
        page = await context.new_page()

        try:
            for url in urls:
                print(f"Visiting: {url}")
                await page.goto(url, wait_until='domcontentloaded', timeout=30000)
                await asyncio.sleep(10)
        except Exception as e:
            print(f"Error while visiting sites: {e}")
        finally:
            await context.close()

    async def launch_concurrent_visits(self, instances=10):
        async with async_playwright() as playwright:
            # Launch 2 browsers
            browser1 = await playwright.chromium.launch(headless=False)
            browser2 = await playwright.chromium.launch(headless=False)

            tasks = []
            for i in range(instances):
                random_urls = random.sample(self.websites, k=3)
                browser = browser1 if i < instances // 2 else browser2
                tasks.append(self.visit_multiple_websites(browser, random_urls))

            await asyncio.gather(*tasks)

            await browser1.close()
            await browser2.close()


if __name__ == "__main__":
    launcher = Virtoxed("sites.xlsx")
    asyncio.run(launcher.launch_concurrent_visits())