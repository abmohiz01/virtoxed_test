import asyncio
import time

from playwright.async_api import async_playwright
import random
import openpyxl

class Virtoxed:

    def __init__(self, excel_path: str, column_letter: str = 'Websites'):
        self.excel_path = excel_path
        self.column_letter = column_letter
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

    async def visit_multiple_websites(self, playwright, urls):
        browser = await playwright.chromium.launch(headless=False)
        context = await browser.new_context()
        page = await context.new_page()

        try:
            for url in urls:
                print(f"Visiting: {url}")
                await page.goto(url, wait_until = 'domcontentloaded',timeout=30000)
                await asyncio.sleep(10)
        except Exception as e:
            print(f"Error while visiting sites: {e}")
        finally:
            await browser.close()

    async def launch_concurrent_visits(self, instances=10):
        async with async_playwright() as playwright:
            tasks = []

            for _ in range(instances):
                # Choose 3 unique random websites for each instance
                random_urls = random.sample(self.websites, k=3)
                tasks.append(self.visit_multiple_websites(playwright, random_urls))

            await asyncio.gather(*tasks)


if __name__ == "__main__":
    launcher = Virtoxed("sites.xlsx")
    asyncio.run(launcher.launch_concurrent_visits())