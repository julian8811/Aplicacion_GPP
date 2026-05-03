import { test, expect } from '@playwright/test'

test('smoke test - full flow', async ({ page }) => {
  // 1. Login
  await page.goto('/login')
  await page.fill('input[type="email"]', 'test@example.com')
  await page.fill('input[type="password"]', 'testpassword123')
  await page.click('button[type="submit"]')
  await expect(page).toHaveURL('/dashboard')
  
  // 2. Dashboard loads
  await expect(page.locator('h1')).toContainText('Hola')
  
  // 3. Navigate to new evaluation
  await page.click('text=Nueva Evaluacion')
  
  // 4. Go through evaluation wizard
  // ... (simplified smoke test)
})