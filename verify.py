
import asyncio
from playwright.async_api import async_playwright, expect

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        try:
            # Go to the splash screen
            await page.goto("http://localhost:8000")
            await expect(page.locator("#screen-splash")).to_be_visible(timeout=10000)
            await expect(page.locator("#main-navigation")).to_be_hidden()

            # --- Go to Login and check nav is hidden ---
            await page.click("#btn-goto-login")
            await expect(page.locator("#screen-login")).to_be_visible()
            await expect(page.locator("#main-navigation")).to_be_hidden()
            await page.screenshot(path="verification/login_screen_no_nav.png")

            # --- Go back and Registration Flow ---
            await page.click("#login-back-btn")
            await page.click("#btn-goto-register")
            await expect(page.locator("#screen-register")).to_be_visible()
            await expect(page.locator("#main-navigation")).to_be_hidden()

            # Step 1: Identity
            await page.fill("#reg-nickname", "TestUser")
            unique_email = f"testuser_{asyncio.get_event_loop().time()}@test.com"
            await page.fill("#reg-email", unique_email)
            await page.fill("#reg-password", "password123")
            await page.click("#reg-next-btn")

            # Step 2: Vitals
            await expect(page.locator("#step-2")).to_be_visible()
            await page.fill("#reg-height", "180")
            await page.fill("#reg-weight", "80")
            await page.click("#reg-next-btn")

            # Step 3: Appearance
            await expect(page.locator("#step-3")).to_be_visible()
            await page.locator(".avatar-option").first.click()
            await page.click("#reg-next-btn")

            # After registration, it should go to the dashboard with nav visible
            await expect(page.locator("#screen-dashboard")).to_be_visible(timeout=20000)
            await expect(page.locator("#main-navigation")).to_be_visible()

            # --- Navigate to Character Screen and check nav is visible ---
            await page.click("#btn-goto-character")
            await expect(page.locator("#screen-character")).to_be_visible(timeout=10000)
            await expect(page.locator("#main-navigation")).to_be_visible()

            await page.screenshot(path="verification/character_screen_with_nav.png")
            print("Screenshots saved successfully.")

        except Exception as e:
            print(f"An error occurred: {e}")
            await page.screenshot(path="verification/error_screenshot.png")
        finally:
            await browser.close()

if __name__ == "__main__":
    import os
    os.makedirs("verification", exist_ok=True)
    asyncio.run(main())
