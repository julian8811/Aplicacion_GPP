import { test, expect } from '@playwright/test'

test.describe('GPP App', () => {
  test('login flow', async ({ page }) => {
    await page.goto('/login')
    await page.fill('input[type="email"]', 'test@example.com')
    await page.fill('input[type="password"]', 'password123')
    await page.click('button[type="submit"]')
    await expect(page).toHaveURL('/dashboard')
  })

  test('create evaluation flow', async ({ page }) => {
    // Login first
    await page.goto('/login')
    await page.fill('input[type="email"]', 'test@example.com')
    await page.fill('input[type="password"]', 'password123')
    await page.click('button[type="submit"]')

    // Navigate to new evaluation
    await page.click('text=Nueva Evaluacion')
    await expect(page).toHaveURL('/evaluate')

    // Select evaluation type
    await page.click('text=PA + PO')

    // Should navigate to wizard
    await expect(page).toHaveURL('/evaluate/wizard')
  })
})