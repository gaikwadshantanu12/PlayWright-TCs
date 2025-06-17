from playwright.sync_api import sync_playwright, expect
import time

"""
def scroll_table_both_axes(page, container_selector, scroll_step=100, delay=0.3):
    # Get scrollable dimensions
    scroll_height = page.evaluate(f"document.querySelector('{container_selector}').scrollHeight")
    scroll_width = page.evaluate(f"document.querySelector('{container_selector}').scrollWidth")
    client_height = page.evaluate(f"document.querySelector('{container_selector}').clientHeight")
    client_width = page.evaluate(f"document.querySelector('{container_selector}').clientWidth")

    print(f"\n📏 Vertical: content={scroll_height}px, viewport={client_height}px")
    print(f"📏 Horizontal: content={scroll_width}px, viewport={client_width}px")

    # Scroll vertically
    y = 0
    while y + client_height < scroll_height:
        page.evaluate(f"document.querySelector('{container_selector}').scrollTo({{ top: {y}, left: 0 }})")
        print(f"🔽 Scrolling vertically to {y}px")
        time.sleep(delay)
        y += scroll_step

    # Scroll horizontally
    x = 0
    while x + client_width < scroll_width:
        page.evaluate(f"document.querySelector('{container_selector}').scrollTo({{ top: 0, left: {x} }})")
        print(f"➡️ Scrolling horizontally to {x}px")
        time.sleep(delay)
        x += scroll_step
"""

def is_element_in_viewport(page, element):
    """Check if an element is inside the viewport using bounding box."""
    box = element.bounding_box()
    if not box:
        return False
    viewport_height = page.viewport_size["height"]
    viewport_width = page.viewport_size["width"]
    return (
        0 <= box["x"] < viewport_width and
        0 <= box["y"] < viewport_height and
        box["x"] + box["width"] <= viewport_width and
        box["y"] + box["height"] <= viewport_height
    )

def get_visible_matrix(page, row_selector, col_selector):
    """Get visible cells only based on bounding box check."""
    visible_matrix = []
    rows = page.locator(row_selector)
    row_count = rows.count()

    for i in range(row_count):
        row = rows.nth(i)
        if not row.bounding_box():
            continue
        cols = row.locator(col_selector)
        row_data = []
        for j in range(cols.count()):
            cell = cols.nth(j)
            if is_element_in_viewport(page, cell):
                row_data.append(cell.inner_text().strip())
        if row_data:
            visible_matrix.append(row_data)

    return visible_matrix

def scroll_and_print_matrix(page, container_selector, row_selector, col_selector, v_step=100, h_step=100, delay=0.4):
    scroll_height = page.evaluate(f"document.querySelector('{container_selector}').scrollHeight")
    client_height = page.evaluate(f"document.querySelector('{container_selector}').clientHeight")
    scroll_width = page.evaluate(f"document.querySelector('{container_selector}').scrollWidth")
    client_width = page.evaluate(f"document.querySelector('{container_selector}').clientWidth")

    top = 0
    while top <= scroll_height - client_height:
        left = 0
        while left <= scroll_width - client_width:
            page.evaluate(f"document.querySelector('{container_selector}').scrollTo({{ top: {top}, left: {left} }})")
            print(f"\n📍 Scroll Position: top={top}px, left={left}px")
            matrix = get_visible_matrix(page, row_selector, col_selector)
            for row in matrix:
                print(" | ".join(row))
            left += h_step
            time.sleep(delay)
        top += v_step

def scroll_to_cell_and_click(page, container_selector, target_text, double_click=False):
    """Scroll both directions and click/double-click the target cell."""
    scroll_height = page.evaluate(f"document.querySelector('{container_selector}').scrollHeight")
    client_height = page.evaluate(f"document.querySelector('{container_selector}').clientHeight")
    scroll_width = page.evaluate(f"document.querySelector('{container_selector}').scrollWidth")
    client_width = page.evaluate(f"document.querySelector('{container_selector}').clientWidth")

    for top in range(0, scroll_height, 50):
        for left in range(0, scroll_width, 100):
            page.evaluate(f"document.querySelector('{container_selector}').scrollTo({{ top: {top}, left: {left} }})")
            page.wait_for_timeout(200)

            cell_locator = page.locator(f"{container_selector} td")
            count = cell_locator.count()

            for i in range(count):
                cell = cell_locator.nth(i)
                if cell.inner_text().strip() == target_text:
                    box = cell.bounding_box()
                    if box:
                        if double_click:
                            cell.dblclick()
                        else:
                            cell.click()
                        page.evaluate(
                            """(text) => {
                                const el = Array.from(document.querySelectorAll('td')).find(td => td.innerText.trim() === text);
                                if (el) el.style.backgroundColor = 'orange';
                            }""",
                            target_text
                        )
                        return True
        time.sleep(0.2)
    return False

def test_dialog_open_close():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        page.goto("http://127.0.0.1:5500/index.html")  # Change this if your HTML is hosted elsewhere

        # ✅ The modal should initially be hidden
        modal = page.locator("#popupModal")
        expect(modal).not_to_be_visible()

        # ✅ Click the "Show Info" button to open the modal
        page.locator(".btn-open-dialog").click()
        expect(modal).to_be_visible()
        print("✅ Modal opened successfully")

        # ✅ Click the close button (×)
        page.locator(".modal-close").click()
        expect(modal).not_to_be_visible()
        print("✅ Modal closed via close button")

        # ✅ Reopen the modal again
        page.locator(".btn-open-dialog").click()
        expect(modal).to_be_visible()
        print("✅ Modal reopened")

        # ✅ Click outside the modal to close it
        page.mouse.click(10, 10)  # Click somewhere in the overlay
        expect(modal).not_to_be_visible()
        print("✅ Modal closed by clicking outside")

        """--------------------------------------------------------------------------------------"""
        # Open modal if table is inside modal
        page.click(".btn-open-dialog")
        page.wait_for_selector(".modal-content", state="visible")

        print("🟢 Modal opened. Starting to scroll the table...")

        # Scroll inside the scroll-box div that contains the table
        scroll_and_print_matrix(
            page,
            container_selector=".scroll-box",
            row_selector=".scroll-box table tr",
            col_selector="td"
        )

        print("✅ Done scrolling.")

        """---------------------------------------------------------------------------------------------"""
        found = scroll_to_cell_and_click(page, ".scroll-box", "R11C7", double_click=True)
        if found:
            print("✅ Cell 'R11C7' clicked and highlighted.")
        else:
            print("❌ Cell 'R11C7' not found.")

        page.wait_for_timeout(3000)
