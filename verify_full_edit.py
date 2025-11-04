
import re
import random
from playwright.sync_api import sync_playwright, expect

def run(playwright):
    browser = playwright.chromium.launch(headless=True)
    context = browser.new_context()
    page = context.new_page()

    try:
        page.goto("file:///app/index.html")

        # Take a screenshot of the initial page to see what's going on
        page.screenshot(path="/home/jules/verification/initial_view.png")
        print("Initial screenshot taken.")

        # Registration - Corrected selector
        page.click("text=Crie uma aqui") # Changed from "Crie uma conta"

        # Now on the registration screen, fill the form
        email = f"testuser_{random.randint(10000, 99999)}@example.com"
        password = "password123"
        page.fill("input[type='email']", email)
        page.fill("input[type='password']", password)
        page.click("button:has-text('Criar Conta')")

        # VERY IMPORTANT: Wait for the dashboard to be ready after registration
        dashboard_element = page.locator("#screen-dashboard")
        expect(dashboard_element).to_be_visible(timeout=20000)
        print("Registration successful, dashboard is visible.")

        # Create a new mission
        page.click("#btn-add-task")
        expect(page.locator("#screen-add-task")).to_be_visible()
        page.fill("#task-title-input", "Test Mission: Refactor Auth Module")
        page.select_option("#task-type-input", "Estudo")
        page.fill("#task-duration-input", "90")
        page.fill("#sub-task-input", "Sub-task 1\\nSub-task 2")
        page.click("#btn-generate-rewards")

        # Wait for AI rewards and save
        expect(page.locator("#xp-reward-value")).not_to_have_text("...", timeout=20000)
        expect(page.locator("#coin-reward-value")).not_to_have_text("...", timeout=20000)
        print("AI rewards generated.")
        page.click("#btn-save-task")

        # Verify mission is on dashboard
        expect(page.locator("#screen-dashboard")).to_be_visible()
        mission_card = page.locator(".task-item:has-text('Test Mission: Refactor Auth Module')")
        expect(mission_card).to_be_visible()
        print("Mission created successfully and visible on dashboard.")

        # Navigate to details and click edit
        mission_card.click()
        expect(page.locator("#screen-mission-details")).to_be_visible()
        page.click("#btn-edit-mission")

        # Edit the mission
        expect(page.locator("#screen-add-task")).to_be_visible()
        print("Editing screen opened.")

        expect(page.locator("#task-title-input")).to_have_value("Test Mission: Refactor Auth Module")
        expect(page.locator("#task-type-input")).to_have_value("Estudo")
        expect(page.locator("#task-duration-input")).to_have_value("90")
        expect(page.locator("#sub-task-input")).to_have_value("Sub-task 1\\nSub-task 2")
        print("Form is pre-filled correctly.")

        page.fill("#task-title-input", "Updated Mission: Complete Refactor")
        page.select_option("#task-type-input", "Trabalho")
        page.fill("#task-duration-input", "120")

        # Trigger reward recalculation
        page.click("#btn-generate-rewards")
        expect(page.locator("#xp-reward-value")).not_to_have_text("...", timeout=20000)
        print("Rewards recalculated.")

        # Save edited mission
        page.click("#btn-save-task")

        # Verify updated mission on dashboard
        expect(page.locator("#screen-dashboard")).to_be_visible()
        expect(page.locator(".task-item:has-text('Test Mission: Refactor Auth Module')")).not_to_be_visible()
        updated_mission_card = page.locator(".task-item:has-text('Updated Mission: Complete Refactor')")
        expect(updated_mission_card).to_be_visible()
        print("Mission updated successfully and visible on dashboard.")

        # Take a screenshot of the final dashboard
        screenshot_path = "/home/jules/verification/final_dashboard.png"
        page.screenshot(path=screenshot_path)
        print(f"Screenshot saved to {screenshot_path}")

    except Exception as e:
        print(f"An error occurred: {e}")
        page.screenshot(path="/home/jules/verification/error_screenshot.png")
        raise
    finally:
        browser.close()

if __name__ == "__main__":
    with sync_playwright() as p:
        run(p)
