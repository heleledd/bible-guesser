import { test, expect } from "@playwright/test";

test.describe("Bible Guesser UI", () => {
  test("homepage loads correctly", async ({ page }) => {
    await page.goto("/");

    await expect(page).toHaveTitle(/Bible Guesser/i);
    await expect(page.getByRole("link", { name: /Bible Guesser/i })).toBeVisible();
  });

  test("navbar shows login/signup when not authenticated", async ({ page }) => {
    await page.goto("/");

    await expect(page.getByRole("link", { name: /Login/i })).toBeVisible();
    await expect(page.getByRole("link", { name: /Sign Up/i })).toBeVisible();
  });

  test("navigates to Login page when clicking Login", async ({ page }) => {
    await page.goto("/");

    await page.getByRole("link", { name: /Login/i }).click();
    await expect(page).toHaveURL(/.*login/);
    await expect(page.locator("h1, h2, form")).toBeVisible();
  });

  test("navigates to Sign Up page when clicking Sign Up", async ({ page }) => {
    await page.goto("/");
    await page.getByRole("link", { name: /Sign Up/i }).click();
    await expect(page).toHaveURL(/.*signup/);
  });
});