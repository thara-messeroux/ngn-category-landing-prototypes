/* Capture the appbar before and after scroll-condense, plus full page. */
const { chromium } = require('@playwright/test');

(async () => {
	const browser = await chromium.launch();
	const page = await browser.newPage({ viewportSize: { width: 1400, height: 1000 } });
	await page.goto('http://localhost:8127/06-composite.html', { waitUntil: 'networkidle' });

	await page.locator('.ngn-bar').screenshot({ path: 'screenshots/_bar-full.png' });

	await page.mouse.wheel(0, 1000);
	await page.waitForTimeout(1200);
	await page.locator('.ngn-bar').screenshot({ path: 'screenshots/_bar-condensed.png' });

	// mid-animation frame for smoothness check
	await page.mouse.wheel(0, -1000);
	await page.waitForTimeout(250);
	await page.locator('.ngn-bar').screenshot({ path: 'screenshots/_bar-mid.png' });

	await page.waitForTimeout(1000);
	await page.screenshot({ path: 'screenshots/06-composite-desktop.png', fullPage: true });
	await browser.close();
	console.log('done');
})();
