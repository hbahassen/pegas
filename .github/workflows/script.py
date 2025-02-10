# script.py
from seleniumwire import webdriver  # Import de Selenium Wire (remplace Selenium WebDriver)
import time

# Configuration des options pour Chrome
options = webdriver.ChromeOptions()
options.add_argument('--headless')                # Mode headless (sans interface graphique)
options.add_argument('--no-sandbox')              # Nécessaire dans certains environnements CI
options.add_argument('--disable-dev-shm-usage')     # Utilise /tmp au lieu de /dev/shm
options.add_argument('--disable-gpu')             # Désactive l'accélération GPU (optionnel)

# Créer le driver avec Selenium Wire pour intercepter les requêtes réseau
driver = webdriver.Chrome(options=options)

# (Optionnel) Vous pouvez définir un "scope" pour filtrer les requêtes, par exemple pour ne capturer que celles qui vous intéressent
# driver.scopes = ['.*']  # Ici, on laisse toutes les requêtes passer

# URL de la page cible
url = "https://web.flypgs.com/flexible-search?adultCount=1&arrivalPort=SAW&currency=EUR&dateOption=1&departureDate=2025-04-15&departurePort=BEY&language=fr&returnDate=2025-04-30"

# Accéder à la page
driver.get(url)

# Attendre quelques secondes pour laisser le temps aux requêtes (fetch/XHR) de s'exécuter
time.sleep(10)

# Parcourir toutes les requêtes interceptées
print("Liste des URL interceptées (toutes requêtes) :")
for request in driver.requests:
    # Pour filtrer et n'afficher que les requêtes de type XHR, vous pouvez vérifier l'en-tête "x-requested-with"
    # Cet en-tête est souvent défini à "XMLHttpRequest" pour les appels AJAX.
    if request.response:
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            print("XHR Request:", request.url)
        else:
            # Vous pouvez également afficher les requêtes de type fetch.
            # Note : Selenium Wire ne donne pas directement le type "fetch", donc vous pouvez afficher tout ou filtrer selon l'URL.
            print("Autre requête:", request.url)

# Fermer le navigateur
driver.quit()
