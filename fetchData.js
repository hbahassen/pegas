const puppeteer = require('puppeteer');
const fs = require('fs');

(async () => {
  const browser = await puppeteer.launch({ headless: true });
  const page = await browser.newPage();

  // Intercepter la réponse de l'endpoint qui vous intéresse
  page.on('response', async response => {
    if (response.url().includes('/pegasus/cheapest-fare')) {
      try {
        const data = await response.json();
        // Sauvegarder le JSON dans un fichier
        fs.writeFileSync('data.json', JSON.stringify(data, null, 2));
        console.log('JSON récupéré et sauvegardé.');
      } catch (error) {
        console.error('Erreur d’extraction du JSON :', error);
      }
    }
  });

  await page.goto('https://web.flypgs.com/flexible-search?adultCount=1&arrivalPort=SAW&currency=USD&dateOption=1&departureDate=2025-03-12&departurePort=BEY&language=fr&returnDate=2025-03-16', { waitUntil: 'networkidle2' });
  await page.waitForTimeout(5000);
  await browser.close();
})();
