import asyncio
from playwright.async_api import async_playwright

async def run():
    async with async_playwright() as p:
        # Lancer Chromium en mode headless avec des options adaptées pour CI
        browser = await p.chromium.launch(
            headless=True,
            args=[
                '--no-sandbox',
                '--disable-setuid-sandbox',
                '--disable-dev-shm-usage'
            ]
        )
        # Créer un contexte qui ignore les erreurs HTTPS
        context = await browser.new_context(ignore_https_errors=True)
        page = await context.new_page()

        # Fonction de gestion des requêtes pour afficher uniquement celles de type "xhr" ou "fetch"
        def log_request(request):
            if request.resource_type() in ["xhr", "fetch"]:
                print("REQUEST:", request.url())

        # Attacher la fonction au déclencheur "request"
        page.on("request", log_request)

        # Navigation vers la page cible
        await page.goto(
            "https://trigodoo.com",
            wait_until="load",  # On attend que la page soit complètement chargée
            timeout=60000       # Timeout de 60 secondes
        )

        # Attendre quelques secondes pour laisser le temps aux requêtes (fetch/XHR) d'être émis
        await page.wait_for_timeout(60000)

        await browser.close()

asyncio.run(run())
