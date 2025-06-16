import re
from playwright.sync_api import Playwright, sync_playwright, expect

def run(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    page.goto("http://127.0.0.1:5500/index.html")
    
    # Check visibility of all input fields
    assert page.is_visible(".input-text")
    assert page.is_visible(".input-email")
    assert page.is_visible(".input-password")
    assert page.is_visible(".input-date")
    assert page.is_visible(".input-file")
    assert page.is_visible(".input-select")
    assert page.is_visible(".input-textarea")
    assert page.is_visible(".btn-submit")

    # All fields are nested under .form-group and .nested-div
    assert page.is_visible(".form-group .input-text")
    assert page.is_visible(".nested-div .input-email")
    assert page.is_visible(".form-group .input-select")

    # Visibility + Enabled
    assert page.is_enabled(".input-text")
    assert page.is_enabled(".btn-submit")

    # Expect style assertion
    expect(page.locator(".input-password")).to_be_visible()
    expect(page.locator(".input-date")).to_be_enabled()
    # expect(page.locator(".form-group")).to_be_attached()

    # Iterate over all fields
    fields = [
    ".input-text", ".input-email", ".input-password",
    ".input-date", ".input-file", ".input-select",
    ".input-textarea", ".btn-submit"
    ]

    for field in fields:
        el = page.locator(field)
        expect(el).to_be_visible()
        expect(el).to_be_enabled()

    # Negative visibility checks
    # Simulate hiding element and check
    page.eval_on_selector(".input-text", "el => el.style.display = 'none'")
    assert not page.is_visible(".input-text")

    # Deep nested access example
    expect(page.locator(".form-container .form-group.nested-div .input-email")).to_be_visible()

    # ✅ Radio buttons
    radios = page.locator(".radio-gender")
    for i in range(radios.count()):
        expect(radios.nth(i)).to_be_visible()

    # ✅ Checkboxes
    checkboxes = page.locator(".checkbox-interest")
    for i in range(checkboxes.count()):
        expect(checkboxes.nth(i)).to_be_visible()

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