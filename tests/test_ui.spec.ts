import { test, expect } from "@playwright/test";

test("home page loads and shows title", async ({ page }) => {
  await page.goto("/");
  await expect(page.locator("#title")).toHaveText("FastAPI + Playwright Demo");
});

test("greet form shows greeting", async ({ page }) => {
  await page.goto("/");
  await page.fill("#name", "ouali");
  await page.click("text=Greet");
  await expect(page.locator("#greet-result")).toHaveText("Hello, ouali!");
});
