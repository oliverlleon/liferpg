
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

            # --- Registration Flow ---
            await page.click("#btn-goto-register")
            await expect(page.locator("#screen-register")).to_be_visible()

            # Step 1: Identity
            await page.fill("#reg-nickname", "TestUser")
            # Use a unique email each time to avoid conflicts
            unique_email = f"testuser_{asyncio.get_event_loop().time()}@test.com"
            await page.fill("#reg-email", unique_email)
            await page.fill("#reg-password", "password123")
            await page.click("#reg-next-btn")

            # Step 2: Vitals
            await expect(page.locator("#step-2")).to_be_visible()
            await page.fill("#reg-height", "180")
            await page.fill("#reg-weight", "80")
            await page.fill("#reg-weight-target", "75")
            await page.click("#reg-next-btn")

            # Step 3: Appearance
            await expect(page.locator("#step-3")).to_be_visible()
            # Select the first avatar
            await page.locator(".avatar-option").first.click()
            await page.click("#reg-next-btn")

            # After registration, it should go to the dashboard
            await expect(page.locator("#screen-dashboard")).to_be_visible(timeout=20000)

            # --- Navigate to Character Screen ---
            await page.click("#btn-goto-character")
            await expect(page.locator("#screen-character")).to_be_visible(timeout=10000)

            # Wait for some elements on the character screen to be populated
            await expect(page.locator("#character-level-title")).not_to_be_empty(timeout=10000)
            await expect(page.locator("#attributes-list")).not_to_be_empty(timeout=10000)

            # Wait for the "Inventário" heading to be visible, which is more robust
            await expect(page.get_by_role("heading", name="Inventário")).to_be_visible(timeout=10000)


            # Take a screenshot of the character screen
            await page.screenshot(path="verification/character_screen.png")
            print("Screenshot saved to verification/character_screen.png")

        except Exception as e:
            print(f"An error occurred: {e}")
            await page.screenshot(path="verification/error_screenshot.png")
        finally:
            await browser.close()

if __name__ == "__main__":
    # Create verification directory if it doesn't exist
    import os
    os.makedirs("verification", exist_ok=True)
    asyncio.run(main())
