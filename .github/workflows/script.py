import time
import json
import gzip
from seleniumwire import webdriver  # Utilise selenium-wire pour intercepter le trafic réseau
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

# --- Configuration de Chrome ---
chrome_options = Options()
chrome_options.add_argument("--headless")  # Mode headless pour CI (retirer si besoin du mode non-headless)
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36")

# --- Configuration et lancement du driver ---
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=chrome_options)

# --- Navigation sur la page déclenchant l'appel API ---
url = "https://web.flypgs.com/flexible-search?adultCount=1&arrivalPort=SAW&currency=USD&dateOption=1&departureDate=2025-03-12&departurePort=BEY&language=fr&returnDate=2025-03-16"
print("Navigation vers :", url)
driver.get(url)

# Attendre quelques secondes pour que la page charge et que les requêtes réseau se déclenchent
time.sleep(10)

# --- Interception et traitement de la réponse ciblée ---
target_url = "https://web.flypgs.com/pegasus/cheapest-fare"
json_data = None

for request in driver.requests:
    if request.response and target_url in request.url:
        try:
            # Récupérer le corps de la réponse
            body = request.response.body

            # Vérifier si la réponse est compressée (gzip)
            encoding = request.response.headers.get('Content-Encoding', '')
            if 'gzip' in encoding.lower():
                content = gzip.decompress(body).decode('utf-8')
            else:
                content = body.decode('utf-8')

            # Charger le contenu JSON
            json_data = json.loads(content)
            print("\n=== JSON content from {} ===".format(request.url))
            print(json.dumps(json_data, indent=2))
            break  # Arrêter après la première réponse trouvée
        except Exception as e:
            print("Erreur lors du traitement de la réponse :", e)

if not json_data:
    print("Aucune réponse JSON trouvée pour l'URL :", target_url)

driver.quit()
