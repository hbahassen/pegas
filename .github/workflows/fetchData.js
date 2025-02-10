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
      '--no-zygote',
      '--disable-http2'
    ],
    ignoreHTTPSErrors: true
  });

  const page = await browser.newPage();

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

  await page.goto('https://web.flypgs.com/flexible-search?adultCount=1&arrivalPort=SAW&currency=EUR&dateOption=1&departureDate=2025-04-15&departurePort=BEY&language=fr&returnDate=2025-04-30', {
    waitUntil: 'networkidle2',
    timeout: 60000 // Increase timeout to 60 seconds
  });
  await page.waitForTimeout(5000);
  await browser.close();
})();
