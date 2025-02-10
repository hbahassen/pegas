import time
import json
import requests
from seleniumwire import webdriver  # Utilise selenium-wire pour récupérer les cookies et lancer la navigation
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

# --- Configuration de Chrome (mode headless) ---
chrome_options = Options()
chrome_options.add_argument("--headless")  # Vous pouvez retirer cette option pour voir le navigateur
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36")

# --- Lancement du driver ---
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=chrome_options)

# --- Navigation sur une page qui initialise la session (par exemple la page de recherche) ---
search_url = ("https://web.flypgs.com/flexible-search?"
              "adultCount=1&arrivalPort=SAW&currency=USD&dateOption=1&"
              "departureDate=2025-03-12&departurePort=BEY&language=fr&returnDate=2025-03-16")
print("Navigation vers :", search_url)
driver.get(search_url)
# Attendre quelques secondes pour que la page charge et que les cookies soient définis
time.sleep(10)

# Récupérer les cookies générés par la session Selenium
selenium_cookies = driver.get_cookies()
cookies = {}
for cookie in selenium_cookies:
    cookies[cookie['name']] = cookie['value']

driver.quit()  # On ferme le navigateur, les cookies sont maintenant dans notre variable 'cookies'

# --- Préparation de la requête POST pour obtenir les vols directs ---
post_url = "https://web.flypgs.com/pegasus/cheapest-fare"

# Préparer les headers identiques à ceux de votre commande cURL (vous pouvez ajuster si nécessaire)
headers = {
    "Accept": "application/json, text/plain, */*",
    "Accept-Language": "fr",
    "Access-Control-Allow-Origin": "*",
    "Cache-Control": "no-cache, no-store, must-revalidate",
    "Connection": "keep-alive",
    "Content-Type": "application/json",
    "Origin": "https://web.flypgs.com",
    "Pragma": "no-cache",
    "Referer": search_url,
    "User-Agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Mobile Safari/537.36",
    "X-PLATFORM": "web",
    "X-VERSION": "1.54.0"
}

# Préparer le payload pour obtenir uniquement les vols directs
payload = {
    "viewType": "DAILY",
    "currency": "USD",
    "flightSearch": {
        "departureDate": "2025-03-12",
        "departurePort": "BEY",
        "returnDate": "2025-03-16",
        "arrivalPort": "SAW"
    },
    "finalMonth": False,
    "departureFlightTypeSelection": ["DIRECT"],
    "departureFlightTimeSelection": [],
    "returnFlightTypeSelection": ["DIRECT"],
    "returnFlightTimeSelection": []
}

print("\nEnvoi de la requête POST pour obtenir les vols directs...")
response = requests.post(post_url, headers=headers, json=payload, cookies=cookies)

if response.status_code == 200:
    json_data = response.json()
    print("\n=== JSON content for direct flights ===")
    print(json.dumps(json_data, indent=2))
else:
    print("Erreur lors de la requête POST:", response.status_code)
