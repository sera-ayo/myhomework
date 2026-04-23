import fs from "node:fs/promises";
import path from "node:path";

import { chromium } from "playwright";


const ROOT = path.resolve(import.meta.dirname, "..", "..");
const outputDir = path.join(ROOT, "paper_assets", "figures", "web");
const baseUrl = process.env.PAPER_WEB_URL ?? "http://127.0.0.1:4173";

async function ensureDir() {
  await fs.mkdir(outputDir, { recursive: true });
}

async function clickIfVisible(page, selectors) {
  for (const selector of selectors) {
    const locator = page.locator(selector);
    if (await locator.count()) {
      const first = locator.first();
      if (await first.isVisible()) {
        await first.click();
        return true;
      }
    }
  }
  return false;
}

async function login(page) {
  await page.goto(`${baseUrl}/login`, { waitUntil: "networkidle" });
  await page.locator(".submit").waitFor({ state: "visible", timeout: 20000 });
  await page.locator('input[type="text"]').first().fill("demo");
  await page.locator('input[type="password"]').first().fill("demo123456");
  await page.locator(".submit").first().click();
  await page.waitForURL(/dashboard/, { timeout: 20000 });
  await page.waitForLoadState("networkidle");
}

async function capturePage(page, urlPath, fileName, waitForSelector) {
  await page.goto(`${baseUrl}${urlPath}`, { waitUntil: "networkidle" });
  if (waitForSelector) {
    await page.locator(waitForSelector).first().waitFor({ state: "visible", timeout: 20000 });
  }
  await clickIfVisible(page, [
    'button:has-text("知道了")',
    'button:has-text("确定")',
    'button:has-text("OK")',
    '.el-message-box__btns button',
  ]);
  await page.screenshot({
    path: path.join(outputDir, fileName),
    fullPage: true,
  });
}

const browser = await chromium.launch({ headless: true });
const context = await browser.newContext({
  locale: "zh-CN",
  viewport: { width: 1600, height: 1100 },
  deviceScaleFactor: 1.5,
});
const page = await context.newPage();

try {
  await ensureDir();
  await capturePage(page, "/login", "01_web_login.png", 'input[type="password"]');
  await login(page);
  await capturePage(page, "/dashboard", "02_web_dashboard.png", ".hero-panel, .metric-grid");
  await capturePage(page, "/analysis", "03_web_analysis.png", ".insight-panel, .chart-grid");
  await capturePage(page, "/warnings", "04_web_warnings.png", ".latest, .panel");
  await capturePage(page, "/experiments", "05_web_experiments.png", ".metric-grid, .panel");
  console.log(`Captured web screenshots under ${outputDir}`);
} finally {
  await context.close();
  await browser.close();
}
