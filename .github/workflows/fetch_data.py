import asyncio
from playwright.async_api import async_playwright
import json

async def run():
    async with async_playwright() as p:
        # Lancer Chromium en mode headless avec des options pour CI, en désactivant HTTP/2
        browser = await p.chromium.launch(
            headless=True,
            args=[
                '--no-sandbox',
                '--disable-setuid-sandbox',
                '--disable-dev-shm-usage',
                '--disable-http2'
            ]
        )
        # Créer un contexte en ignorant les erreurs HTTPS
        context = await browser.new_context(ignore_https_errors=True)
        page = await context.new_page()

        # Gestionnaire pour intercepter et traiter les réponses ciblées
        async def handle_response(response):
            if '/pegasus/cheapest-fare' in response.url:
                try:
                    data = await response.json()
                    print("JSON récupéré :")
                    print(json.dumps(data, indent=2))
                except Exception as e:
                    print("Erreur lors de l'extraction du JSON :", e)

        page.on("response", handle_response)

        try:
            # Utiliser "load" (chargement complet de la page) plutôt que "networkidle"
            await page.goto(
                "https://web.flypgs.com/flexible-search?adultCount=1&arrivalPort=SAW&currency=EUR&dateOption=1&departureDate=2025-04-15&departurePort=BEY&language=fr&returnDate=2025-04-30",
                wait_until="load",
                timeout=60000  # Timeout de 60 secondes
            )
        except Exception as e:
            print("Erreur de navigation :", e)

        # Attendre quelques secondes pour laisser le temps aux requêtes d'être émises
        await page.wait_for_timeout(5000)
        await browser.close()

asyncio.run(run())
