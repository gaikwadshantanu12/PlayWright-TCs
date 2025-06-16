from playwright.sync_api import sync_playwright, expect

def run(playwright):
    browser = playwright.chromium.launch(headless=False)
    page = browser.new_page()
    page.goto("http://127.0.0.1:5500/index.html")  # Update path accordingly

    # === Fill form with test data ===
    page.locator(".input-text").fill("John Doe")
    page.locator(".input-email").fill("john@example.com")
    page.locator(".input-password").fill("secret123")
    page.locator(".input-date").fill("1990-01-01")
    page.locator(".input-select").select_option("india")
    page.locator(".input-textarea").fill("Automation is fun!")
    page.locator(".radio-gender[value='male']").check()
    page.locator(".checkbox-interest[value='music']").check()
    page.locator(".checkbox-interest[value='reading']").check()

    # === Apply Various Filters ===

    # 1. Filter by has_text
    name_field = page.locator(".form-group").filter(has_text="Name")
    print("✔ Name field visible:", name_field.is_visible())

    # 2. Filter by nested element
    email_field = page.locator(".form-group").filter(has=page.locator(".input-email"))
    print("✔ Email field contains email input:", email_field.count())

    # 3. Filter by index
    second_input = page.locator("input").nth(1)
    print("✔ Second input field value:", second_input.input_value())

    # 4. First and Last filters
    first_input = page.locator("input").first
    last_input = page.locator("input").last
    print("✔ First input type:", first_input.get_attribute("type"))
    print("✔ Last input type:", last_input.get_attribute("type"))

    # 5. Count total checkboxes
    total_checkboxes = page.locator(".checkbox-interest").count()
    print("✔ Total interest checkboxes:", total_checkboxes)

    # 6. Get all selected checkboxes
    selected_interests = page.locator(".checkbox-interest:checked").evaluate_all("els => els.map(el => el.value)")
    print("✔ Selected interests:", selected_interests)

    # 7. Get label text using relative selector
    email_label = page.locator("label").filter(has=page.locator(".input-email"))
    print("✔ Email label count (via filter has):", email_label.count())

    # 8. Click nth option from dropdown (if applicable)
    dropdown_options = page.locator("select.input-select > option")
    print("✔ Available options in country select:")
    for i in range(dropdown_options.count()):
        print(f"  - {dropdown_options.nth(i).text_content()}")

    browser.close()


def test_suite():
    with sync_playwright() as playwright:
        run(playwright)

if __name__ == "__main__":
    with sync_playwright() as playwright:
        run(playwright)
