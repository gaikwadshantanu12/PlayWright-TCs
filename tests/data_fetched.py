from playwright.sync_api import sync_playwright

def fetch_form_values(page):
    data = {}

    # Text input
    data["name"] = page.locator(".input-text").input_value()

    # Email
    data["email"] = page.locator(".input-email").input_value()

    # Password
    data["password"] = page.locator(".input-password").input_value()

    # Date
    data["dob"] = page.locator(".input-date").input_value()

    # File - returns the file name (if any)
    file_input = page.locator(".input-file")
    file_value = file_input.evaluate("el => el.value")
    data["file"] = file_value

    # Radio buttons
    selected_gender = page.locator(".radio-gender:checked")
    data["gender"] = selected_gender.evaluate("el => el.value") if selected_gender.count() > 0 else None

    # Checkboxes
    checked_interests = page.locator(".checkbox-interest:checked")
    data["interests"] = checked_interests.evaluate_all("els => els.map(el => el.value)")

    # Dropdown
    data["country"] = page.locator(".input-select").input_value()

    # Textarea
    data["bio"] = page.locator(".input-textarea").input_value()

    return data

def run(playwright):
    browser = playwright.chromium.launch(headless=False)
    page = browser.new_page()
    page.goto("http://127.0.0.1:5500/index.html")  # Change to your local file/server

    # Fill dummy values for testing
    page.locator(".input-text").fill("John Doe")
    page.locator(".input-email").fill("john@example.com")
    page.locator(".input-password").fill("secret123")
    page.locator(".input-date").fill("1990-01-01")
    page.locator(".input-select").select_option("india")
    page.locator(".input-textarea").fill("I love automation!")

    # Simulate checking checkboxes and selecting radio
    page.locator(".radio-gender[value='male']").check()
    page.locator(".checkbox-interest[value='music']").check()
    page.locator(".checkbox-interest[value='reading']").check()

    # Fetch all field values
    form_data = fetch_form_values(page)
    print("\n📋 Fetched Form Data:")
    for field, value in form_data.items():
        print(f"{field}: {value}")

    browser.close()

def test_suite():
    with sync_playwright() as playwright:
        run(playwright)

if __name__ == "__main__":
    with sync_playwright() as playwright:
        run(playwright)
