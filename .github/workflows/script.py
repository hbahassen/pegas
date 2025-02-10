from seleniumwire import webdriver  # Import de Selenium Wire pour intercepter le trafic
import time

# Configuration des options de Chrome pour une navigation visible (non-headless)
options = webdriver.ChromeOptions()
# On n'ajoute PAS '--headless' pour que le navigateur soit visible
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
options.add_argument('--window-size=1920,1080')  # Taille de la fenêtre pour une meilleure visibilité

# IMPORTANT : définir la localisation du binaire Chromium
# Sur Ubuntu, le binaire est souvent à cet emplacement :
options.binary_location = '/usr/bin/chromium-browser'

# Créer le driver Selenium Wire
driver = webdriver.Chrome(options=options)

# URL de la page cible
url = "https://web.flypgs.com/flexible-search?adultCount=1&arrivalPort=SAW&currency=EUR&dateOption=1&departureDate=2025-04-15&departurePort=BEY&language=fr&returnDate=2025-04-30"
driver.get(url)

# Attendre quelques secondes pour laisser le temps aux requêtes (fetch/XHR) de s'exécuter
time.sleep(10)

print("Liste des requêtes interceptées (fetch/XHR) :")
for request in driver.requests:
    if request.response:
        # Afficher les requêtes XHR (en filtrant par l'en-tête "x-requested-with" si disponible)
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            print("XHR Request:", request.url)
        else:
            # Sinon, afficher toutes les autres requêtes
            print("Requête:", request.url)

# Fermer le navigateur
driver.quit()
