from seleniumwire import webdriver  # Import de Selenium Wire pour intercepter le trafic
import time

# Configuration des options de Chrome pour une navigation visible (non-headless)
options = webdriver.ChromeOptions()
# Ne PAS ajouter l'argument '--headless' pour que le navigateur soit visible
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
options.add_argument('--window-size=1920,1080')  # Taille de fenêtre pour une meilleure visibilité

# Créer le driver Selenium Wire
driver = webdriver.Chrome(options=options)

# URL de la page cible
url = "https://web.flypgs.com/flexible-search?adultCount=1&arrivalPort=SAW&currency=EUR&dateOption=1&departureDate=2025-04-15&departurePort=BEY&language=fr&returnDate=2025-04-30"
driver.get(url)

# Attendre quelques secondes pour que la page charge et que les requêtes réseau s'exécutent
time.sleep(10)

print("Liste des requêtes interceptées (fetch/XHR) :")
for request in driver.requests:
    if request.response:
        # Certains appels XHR incluent l'en-tête 'x-requested-with' avec la valeur 'XMLHttpRequest'
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            print("XHR Request:", request.url)
        else:
            # Vous pouvez adapter le filtrage en fonction d'autres critères,
            # ici nous affichons toutes les requêtes pour que vous puissiez examiner leurs URL.
            print("Requête:", request.url)

# Fermer le navigateur
driver.quit()
