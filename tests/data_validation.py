from playwright.sync_api import sync_playwright, expect

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

    # File
    file_input = page.locator(".input-file")
    file_value = file_input.evaluate("el => el.value")
    data["file"] = file_value

    # Radio
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
    page.goto("http://127.0.0.1:5500/index.html")  # Update this if needed

    # === Test Data ===
    test_data = {
        "name": "John Doe",
        "email": "john@example.com",
        "password": "secret123",
        "dob": "1990-01-01",
        "gender": "male",
        "interests": ["music", "reading"],
        "country": "india",
        "bio": "I love automation!"
    }

    # === Fill Form ===
    page.locator(".input-text").fill(test_data["name"])
    page.locator(".input-email").fill(test_data["email"])
    page.locator(".input-password").fill(test_data["password"])
    page.locator(".input-date").fill(test_data["dob"])
    page.locator(".input-select").select_option(test_data["country"])
    page.locator(".input-textarea").fill(test_data["bio"])

    page.locator(f".radio-gender[value='{test_data['gender']}']").check()
    for interest in test_data["interests"]:
        page.locator(f".checkbox-interest[value='{interest}']").check()

    # === Fetch and Validate Data ===
    form_data = fetch_form_values(page)
    print("\n📋 Fetched Form Data:")
    for key, value in form_data.items():
        print(f"{key}: {value}")

    print("\n✅ Performing Validations...")

    # === Assertions ===
    assert form_data["name"] == test_data["name"], "Name mismatch"
    assert form_data["email"] == test_data["email"], "Email mismatch"
    assert form_data["password"] == test_data["password"], "Password mismatch"
    assert form_data["dob"] == test_data["dob"], "DOB mismatch"
    assert form_data["gender"] == test_data["gender"], "Gender mismatch"
    assert set(form_data["interests"]) == set(test_data["interests"]), "Interests mismatch"
    assert form_data["country"] == test_data["country"], "Country mismatch"
    assert form_data["bio"] == test_data["bio"], "Bio mismatch"

    print("✅ All validations passed.")
    browser.close()

def test_suite():
    with sync_playwright() as playwright:
        run(playwright)

if __name__ == "__main__":
    with sync_playwright() as playwright:
        run(playwright)
