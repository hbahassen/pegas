import time
import json
from seleniumwire import webdriver  # Import de Selenium Wire pour intercepter le trafic
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

# Configuration des options de Chrome
chrome_options = Options()
chrome_options.add_argument("--headless")  # Vous pouvez retirer cette option pour du mode non-headless
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36")
chrome_options.set_capability("goog:loggingPrefs", {"performance": "ALL"})

# Créer un objet Service qui gère le chemin de ChromeDriver
service = Service(ChromeDriverManager().install())

# Créer le driver en utilisant l'objet service et les options
driver = webdriver.Chrome(service=service, options=chrome_options)

# Accès à la page cible (exemple pour Pegasus)
url = "https://web.flypgs.com/flexible-search?adultCount=1&arrivalPort=SAW&currency=USD&dateOption=1&departureDate=2025-03-12&departurePort=BEY&language=fr&returnDate=2025-03-16"
print("Accès à l'URL :", url)
driver.get(url)

# Attendre quelques secondes pour que la page charge et que les requêtes réseau soient lancées
time.sleep(10)

# Extraction des logs de performance et détection des URL JSON
logs = driver.get_log("performance")
json_urls = []

for entry in logs:
    try:
        log_message = json.loads(entry["message"])["message"]
        if "Network.responseReceived" in log_message["method"]:
            response_url = log_message["params"]["response"]["url"]
            mime_type = log_message["params"]["response"].get("mimeType", "")
            # Filtrer les URL qui contiennent "pegasus" et qui ont le type MIME "application/json"
            if "pegasus" in response_url.lower() and "application/json" in mime_type.lower():
                if response_url not in json_urls:
                    json_urls.append(response_url)
                    print("URL JSON détectée :", response_url)
    except Exception:
        continue

driver.quit()
