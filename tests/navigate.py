import re
from playwright.sync_api import Playwright, sync_playwright, expect

def run(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    page.goto("http://127.0.0.1:5500/index.html")
    page.close()

    # ---------------------
    context.close()
    browser.close()

def test_suite():
    with sync_playwright() as playwright:
        run(playwright)

if __name__ == "main":
    with sync_playwright() as playwright:
        run(playwright)