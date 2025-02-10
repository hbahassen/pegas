import time
import json
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from webdriver_manager.chrome import ChromeDriverManager

# --- Configuration de Chrome et du driver ---
chrome_options = Options()
chrome_options.add_argument("--headless")  # Mode headless pour l'exécution en CI
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36")

# Configuration des capacités pour récupérer les logs de performance
caps = DesiredCapabilities.CHROME
caps["goog:loggingPrefs"] = {"performance": "ALL"}

# Initialiser le driver avec ChromeDriver Manager
driver = webdriver.Chrome(ChromeDriverManager().install(), options=chrome_options, desired_capabilities=caps)

# --- Navigation sur le site Pegasus ---
# Remplacez l'URL ci-dessous par celle qui déclenche l'appel fetch/XHR de Pegasus.
url = "https://web.flypgs.com/flexible-search?adultCount=1&arrivalPort=SAW&currency=USD&dateOption=1&departureDate=2025-03-12&departurePort=BEY&language=fr&returnDate=2025-03-16"
print("Accès à l'URL :", url)
driver.get(url)

# Attendre quelques secondes pour laisser le temps aux requêtes réseau de se déclencher
time.sleep(10)

# --- Extraction des logs de performance et détection des URL JSON ---
logs = driver.get_log("performance")
json_urls = []

for entry in logs:
    try:
        log_message = json.loads(entry["message"])["message"]
        if "Network.responseReceived" in log_message["method"]:
            response_url = log_message["params"]["response"]["url"]
            mime_type = log_message["params"]["response"].get("mimeType", "")
            # Filtrer : URL contenant "pegasus" et type MIME "application/json"
            if "pegasus" in response_url.lower() and "application/json" in mime_type.lower():
                if response_url not in json_urls:
                    json_urls.append(response_url)
                    print("URL JSON détectée :", response_url)
    except Exception:
        continue

driver.quit()
