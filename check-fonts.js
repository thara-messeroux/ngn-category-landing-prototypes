/* Inspect computed fonts on the production homepage. */
const { chromium } = require('@playwright/test');

(async () => {
	const browser = await chromium.launch();
	const page = await browser.newPage({ viewportSize: { width: 1400, height: 1000 } });
	await page.goto('https://news.northeastern.edu/', { waitUntil: 'domcontentloaded' });
	const out = await page.evaluate(() => {
		const pick = (sel) => {
			const el = document.querySelector(sel);
			if (!el) return null;
			const cs = getComputedStyle(el);
			return { sel, font: cs.fontFamily, weight: cs.fontWeight, size: cs.fontSize,
				sample: (el.textContent || '').trim().slice(0, 60) };
		};
		return [
			pick('.headline'), pick('h1'), pick('h2'), pick('h3'),
			pick('.story-link-v3 .headline'), pick('.story-link .headline'),
			pick('.blurb'), pick('.kicker'), pick('body'),
		].filter(Boolean);
	});
	console.log(JSON.stringify(out, null, 1));
	await browser.close();
})();
