/* Real layout and cross-window completion, driven by workspace_viraltrac_browser.py.
   Requires separately installed Playwright; no product dependency is added. */
const assert = require('node:assert/strict');
const { chromium } = require(process.env.AURA_PLAYWRIGHT_MODULE || '@playwright/test');

(async () => {
  const browser = await chromium.launch({ headless: true });
  try {
    const page = await browser.newPage({ viewport: { width: 1400, height: 900 } });
    const errors = [];
    page.on('pageerror', error => errors.push(error.message));
    await page.goto(process.argv[2]);
    // A fresh workspace must show the explicit business chooser rather than
    // burying the requested connection under first-use AI setup.
    await page.getByRole('combobox', { name: 'AURA business', exact: true }).selectOption(process.argv[3]);
    await page.getByRole('button', { name: 'Continue', exact: true }).click();
    const pairingWindow = page.waitForEvent('popup');
    await page.getByRole('button', { name: 'Connect ViralTrac', exact: true }).click();
    const pairing = await pairingWindow;
    pairing.on('pageerror', error => errors.push(error.message));
    const approvalWindow = pairing.waitForEvent('popup');
    await pairing.getByRole('button', { name: 'Continue to ViralTrac' }).click();
    const approval = await approvalWindow;
    await approval.getByRole('button', { name: 'Approve synthetic business' }).click();
    await pairing.getByText('Connected to Synthetic Studio.', { exact: false }).waitFor();
    // Completion must refresh the original card without a manual page reload.
    await page.getByRole('button', { name: 'Marketing summary', exact: true }).click();
    await page.getByText('1400', { exact: true }).waitFor();
    await page.getByRole('button', { name: 'Save latest for this period' }).click();
    await page.getByText('Saved the latest report for this period.', { exact: false }).waitFor();
    await page.evaluate(() => showApiConnections(''));
    await page.getByText('Saved reports', { exact: true }).click();
    assert.equal(await page.locator('[data-viraltrac-refresh]').count(), 1);
    await page.locator('[data-viraltrac-refresh]').click();
    await page.getByText('No changes to measurements', { exact: false }).waitFor();
    await page.setViewportSize({ width: 390, height: 844 });
    assert.equal(await page.evaluate(() => document.documentElement.scrollWidth > innerWidth), false);
    await page.getByRole('button', { name: 'Work with this in chat' }).click();
    assert.match(await page.locator('#request').inputValue(), /ViralTrac performance/);
    assert.deepEqual(errors, []);
    console.log('ViralTrac browser passed: explicit business, pairing completion, report, save, refresh, mobile and chat draft.');
  } finally {
    await browser.close();
  }
})().catch(error => { console.error(error); process.exitCode = 1; });
