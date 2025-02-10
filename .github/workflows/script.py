import time
import json
import gzip
import os
from seleniumwire import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

# Afficher le répertoire de travail
print("Répertoire de travail :", os.getcwd())

# Chemin de sortie pour le fichier JSON à la racine du dépôt
output_file = os.path.join(os.getcwd(), "pegsu.json")

# --- Configuration de Chrome ---
chrome_options = Options()
chrome_options.add_argument("--headless")
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

time.sleep(10)

# --- Interception et traitement de la réponse ciblée ---
target_url = "https://web.flypgs.com/pegasus/cheapest-fare"
json_data = None

for request in driver.requests:
    if request.response and request.url.rstrip("/") == target_url.rstrip("/"):
        try:
            body = request.response.body
            encoding = request.response.headers.get('Content-Encoding', '')
            if 'gzip' in encoding.lower():
                content = gzip.decompress(body).decode('utf-8')
            else:
                content = body.decode('utf-8')
            json_data = json.loads(content)
            print("\n=== JSON content from {} ===".format(request.url))
            print(json.dumps(json_data, indent=2))
            break
        except Exception as e:
            print("Erreur lors du traitement de la réponse :", e)

if json_data:
    # Ajouter une info de timestamp pour forcer une modification
    json_data['updated_at'] = time.strftime("%Y-%m-%d %H:%M:%S")
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(json_data, f, ensure_ascii=False, indent=2)
    print("Fichier sauvegardé :", output_file)
else:
    print("Aucune réponse JSON trouvée pour l'URL exacte :", target_url)

driver.quit()
