import asyncio
from playwright.async_api import async_playwright
import json

async def run():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True, args=[
            '--no-sandbox',
            '--disable-setuid-sandbox',
            '--disable-dev-shm-usage'
        ])
        context = await browser.new_context()
        page = await context.new_page()

        async def handle_response(response):
            if '/pegasus/cheapest-fare' in response.url:
                try:
                    data = await response.json()
                    print("JSON récupéré :")
                    print(json.dumps(data, indent=2))
                except Exception as e:
                    print("Erreur lors de l'extraction du JSON :", e)

        page.on("response", handle_response)

        url = "https://web.flypgs.com/flexible-search?adultCount=1&arrivalPort=SAW&currency=EUR&dateOption=1&departureDate=2025-04-15&departurePort=BEY&language=fr&returnDate=2025-04-30"
        
        retries = 3
        for attempt in range(retries):
            try:
                await page.goto(url, wait_until="networkidle", timeout=60000)
                break
            except Exception as e:
                print(f"Attempt {attempt + 1} failed: {e}")
                if attempt == retries - 1:
                    raise

        await page.wait_for_timeout(5000)
        await browser.close()

asyncio.run(run())
