const { chromium } = require('playwright');

(async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 1365, height: 900 } });
  await page.goto('http://localhost:8080/countries-we-are-visiting/', { waitUntil: 'networkidle' });
  await page.waitForTimeout(2500);

  const map = await page.$('#destinations-map');
  if (!map) throw new Error('Map element not found');

  await map.scrollIntoViewIfNeeded();
  await page.waitForTimeout(800);
  await map.screenshot({ path: 'tmp-map-only.png' });

  await browser.close();
})();
