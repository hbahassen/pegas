const puppeteer = require('puppeteer');

(async () => {
  const browser = await puppeteer.launch({
    headless: true,
    args: [
      '--no-sandbox',
      '--disable-setuid-sandbox',
      '--disable-dev-shm-usage',
      '--disable-gpu',
      '--single-process',
      '--no-zygote'
    ],
    ignoreHTTPSErrors: true // Ignore HTTPS errors
  });

  const page = await browser.newPage();

  // Set request headers to disable HTTP/2
  await page.setExtraHTTPHeaders({
    'Upgrade-Insecure-Requests': '1'
  });

  // Handle JSON response interception
  page.on('response', async response => {
    if (response.url().includes('/pegasus/cheapest-fare')) {
      try {
        const data = await response.json();
        const fs = require('fs');
        fs.writeFileSync('data.json', JSON.stringify(data, null, 2));
        console.log('JSON récupéré et sauvegardé.');
      } catch (error) {
        console.error('Erreur lors de l’extraction du JSON:', error);
      }
    }
  });

  await page.goto('https://web.flypgs.com/flexible-search?adultCount=1&arrivalPort=SAW&currency=USD&dateOption=1&departureDate=2025-03-12&departurePort=BEY&language=fr&returnDate=2025-03-16', { waitUntil: 'networkidle2' });
  await page.waitForTimeout(5000);
  await browser.close();
})();
