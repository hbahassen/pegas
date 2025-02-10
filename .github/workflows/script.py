import time
import json
from seleniumwire import webdriver  # Utilise selenium-wire pour intercepter le trafic réseau
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

# --- Configuration de Chrome ---
chrome_options = Options()
chrome_options.add_argument("--headless")  # Mode headless pour CI (retirez pour voir le navigateur)
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36")

# --- Configuration et lancement du driver ---
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=chrome_options)

# --- Navigation sur la page déclenchant l'appel API ---
# Cette URL déclenche en arrière-plan des appels fetch/XHR, dont celui qui nous intéresse.
url = "https://web.flypgs.com/flexible-search?adultCount=1&arrivalPort=SAW&currency=USD&dateOption=1&departureDate=2025-03-12&departurePort=BEY&language=fr&returnDate=2025-03-16"
print("Navigation vers :", url)
driver.get(url)

# Attendre quelques secondes pour que la page charge et que les requêtes réseau s'exécutent
time.sleep(10)

# --- Interception et filtrage de la requête ciblée ---
target_url = "https://web.flypgs.com/pegasus/cheapest-fare"
json_data = None

# Parcours de toutes les requêtes interceptées par selenium-wire
for request in driver.requests:
    if request.response and target_url in request.url:
        try:
            # Récupérer le corps de la réponse (en bytes), le décoder en UTF-8 et le parser en JSON
            body = request.response.body
            content = body.decode('utf-8')
            json_data = json.loads(content)
            print("\n=== JSON content from {} ===".format(request.url))
            print(json.dumps(json_data, indent=2))
            break  # Arrêter après la première correspondance
        except Exception as e:
            print("Erreur lors du traitement de la réponse :", e)

if not json_data:
    print("Aucune réponse JSON trouvée pour l'URL :", target_url)

driver.quit()
