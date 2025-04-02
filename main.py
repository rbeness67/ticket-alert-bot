import time
import logging
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from twilio.rest import Client 
 # Twilio client

# Charger les variables d'environnement depuis .env

# Récupération des infos Twilio depuis l'environnement
ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
FROM_NUMBER = os.getenv("TWILIO_FROM_NUMBER")
TO_NUMBER = os.getenv("TWILIO_TO_NUMBER")

def send_twilio_message(message):
    """Send an SMS using Twilio API."""
    client = Client(ACCOUNT_SID, AUTH_TOKEN)
    client.messages.create(
        body=message,
        from_=FROM_NUMBER,
        to=TO_NUMBER
    )

def start_driver():
    logging.info("🚀 Lancement du WebDriver...")

    chrome_options = Options()
    chrome_options.binary_location = "/usr/bin/google-chrome"

    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--window-size=1920x1080")

    driver = webdriver.Chrome(
        executable_path="/opt/chromedriver/chromedriver",  # 👈 Chemin personnalisé
        options=chrome_options
    )
    driver.maximize_window()
    return driver

def open_ticket_page(driver):
    url = "https://billetterie.rcstrasbourgalsace.fr/fr/acheter/billet-unite-premium-tout-public-rcsa-ogc-nice-2024-wqxeuidmshon"
    driver.get(url)

def is_tickets_available(driver):
    sections = ["NORD", "OUEST", "EST"]
    
    for section in sections:
        try:
            button = driver.find_element(By.XPATH, f"//button[.//b[contains(text(), '{section}')]]")
            button.click()
            if section != "OUEST":
                for sub in 'ABCDEFGHIJKL':
                    try:
                        button_detail = driver.find_element(By.XPATH, f"//button[.//b[contains(text(), ' - {sub}')]]")
                        button_detail.click()
                        message = f"🎫 Tickets trouvés ! Section: {section}, Sous-section: {sub}"
                        send_twilio_message(message)  # ✅ TWILIO MESSAGE ICI
                        return False
                    except:
                        time.sleep(1)     
            else:
                message = f"🎫 Tickets trouvés dans la section {section} !"
                send_twilio_message(message)  # ✅ TWILIO MESSAGE POUR SECTION OUEST
                time.sleep(1)     
        except:
            time.sleep(0.1)

def attempt_booking(driver):
    while True:
        is_tickets_available(driver)
        driver.refresh()
        time.sleep(30)

def launch_new_instance():
    new_driver = start_driver()
    open_ticket_page(new_driver)
    attempt_booking(new_driver)

def main():
    driver = start_driver()
    open_ticket_page(driver)
    attempt_booking(driver)

if __name__ == "__main__":
    main()
