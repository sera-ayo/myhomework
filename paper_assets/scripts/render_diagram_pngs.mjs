import fs from "node:fs/promises";
import path from "node:path";

import { chromium } from "playwright";


const ROOT = path.resolve(import.meta.dirname, "..", "..");
const diagramDir = path.join(ROOT, "paper_assets", "figures", "diagrams");

const browser = await chromium.launch({ headless: true });
const page = await browser.newPage({
  viewport: { width: 1800, height: 1200 },
  deviceScaleFactor: 2,
});

try {
  const entries = (await fs.readdir(diagramDir)).filter((file) => file.endsWith(".svg")).sort();
  for (const file of entries) {
    const sourcePath = path.join(diagramDir, file);
    const targetPath = path.join(diagramDir, file.replace(/\.svg$/, ".png"));
    await page.goto(`file://${sourcePath}`, { waitUntil: "load" });
    await page.locator("svg").screenshot({ path: targetPath, timeout: 60000 });
    console.log(`Rendered ${path.basename(targetPath)}`);
  }
} finally {
  await browser.close();
}
