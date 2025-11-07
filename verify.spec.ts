import { test, expect } from '@playwright/test';

test('Full registration and inventory check', async ({ page }) => {
  // Use a unique email for each test run to avoid conflicts
  const uniqueEmail = `user_${Date.now()}@example.com`;
  const password = 'password123';

  // 1. Navigate to the app
  await page.goto('http://localhost:8000');

  // Wait for the splash screen to be ready
  await expect(page.locator('#screen-splash')).toBeVisible();

  // 2. Start Registration
  await page.locator('#btn-goto-register').click();
  await expect(page.locator('#screen-register')).toBeVisible();

  // --- Step 1: Identity ---
  await expect(page.locator('#step-1')).toBeVisible();
  await page.locator('#reg-nickname').fill('Test User');
  await page.locator('#reg-email').fill(uniqueEmail);
  await page.locator('#reg-password').fill(password);
  await page.locator('#reg-next-btn').click();

  // --- Step 2: Vitals ---
  await expect(page.locator('#step-2')).toBeVisible();
  await page.locator('#reg-height').fill('180');
  await page.locator('#reg-weight').fill('80');
  await page.locator('#reg-weight-target').fill('75');
  await page.locator('#reg-next-btn').click();

  // --- Step 3: Appearance ---
  await expect(page.locator('#step-3')).toBeVisible();
  // Select the first avatar
  await page.locator('.avatar-option').first().click();
  await page.locator('#reg-next-btn').click();

  // 4. Wait for Dashboard to load after registration
  // The app should automatically log in and redirect.
  await expect(page.locator('#screen-dashboard')).toBeVisible({ timeout: 15000 });
  await expect(page.locator('#hub-nickname')).toHaveText('Test User');

  // 5. Navigate to Character Screen
  await page.locator('#btn-goto-character').click();
  await expect(page.locator('#screen-character')).toBeVisible();

  // 6. Verify Inventory
  // Wait for the inventory grid to be populated by checking for the first item.
  const inventoryItem = page.locator('#inventory-grid .inventory-item');
  await expect(inventoryItem.first()).toBeVisible({ timeout: 10000 });

  // Also check for equipment slots
  const equipmentSlot = page.locator('#equipment-slots [data-slot="head"]');
  await expect(equipmentSlot).toBeVisible();

  // 7. Take a screenshot
  const screenshotPath = 'character_screen_with_inventory.png';
  await page.screenshot({ path: screenshotPath });
  console.log(`Screenshot saved to ${screenshotPath}`);

  // Optional: A final check to ensure the file exists, though screenshot() would fail if it couldn't write.
  const fs = require('fs');
  expect(fs.existsSync(screenshotPath)).toBe(true);
});
