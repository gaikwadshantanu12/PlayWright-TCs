from playwright.sync_api import sync_playwright, expect

def run(playwright):
    browser = playwright.chromium.launch(headless=False)
    page = browser.new_page()
    page.goto("http://127.0.0.1:5500/index.html")

    # === Dropdown handling ===
    expected_country = "india"
    dropdown = page.locator(".input-select")
    dropdown.select_option(expected_country)

    selected_country = dropdown.input_value()
    assert selected_country == expected_country, "Dropdown value mismatch"
    print(f"✔ Selected country: {selected_country}")

    print("✔ Available countries:")
    for i in range(dropdown.locator("option").count()):
        option = dropdown.locator("option").nth(i)
        print(f"  - {option.text_content().strip()}")

    browser.close()

def test_suite():
    with sync_playwright() as playwright:
        run(playwright)

if __name__ == "main":
    with sync_playwright() as playwright:
        run(playwright)