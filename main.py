import time
import logging
import os

# En LOCAL : décommente la ligne suivante si tu testes avec un fichier .env
# from dotenv import load_dotenv
# load_dotenv()

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from twilio.rest import Client 

# Récupération des variables d'environnement
TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
TWILIO_WHATSAPP_FROM = os.getenv("TWILIO_WHATSAPP_FROM")
TWILIO_WHATSAPP_TO = os.getenv("TWILIO_WHATSAPP_TO")

client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

def send_twilio_sms(message):
    """Envoie un message WhatsApp via Twilio."""
    try:
        if not all([TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN, TWILIO_WHATSAPP_FROM, TWILIO_WHATSAPP_TO]):
            raise ValueError("❌ Variable(s) d'environnement manquante(s)")
        
        logging.info(f"📲 Envoi WhatsApp à {TWILIO_WHATSAPP_TO}")
        client.messages.create(
            body=message,
            from_=TWILIO_WHATSAPP_FROM,
            to=TWILIO_WHATSAPP_TO
        )
        logging.info("✅ Message WhatsApp envoyé via Twilio.")
    except Exception as e:
        logging.error(f"❌ Erreur lors de l'envoi du message WhatsApp : {e}")

def start_driver():
    chrome_options = Options()
    chrome_options.binary_location = "/opt/render/project/.render/chrome/opt/google/chrome/google-chrome"
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--window-size=1920x1080")

    driver = webdriver.Chrome(options=chrome_options)
    driver.maximize_window()
    return driver

def open_ticket_page(driver):
    url = "https://billetterie.rcstrasbourgalsace.fr/fr/acheter/billet-unite-feminines-tout-public-racing-le-havre-2024-qqgxq35d60wd/plan#bk3ff5275b-zone"
    driver.get(url)

def is_tickets_available(driver):
    try:
        logging.info("Checking for 'NORD' button...")
        button = driver.find_element(By.XPATH, f"//button[.//b[contains(text(), 'NORD')]]")

        send_twilio_sms("🎫 Billet NORD détecté ! Dépêche-toi vite!")
        time.sleep(180)
        logging.info("'NORD' ticket found!")
        return True

    except Exception as e:
        time.sleep(.1)
    return False

def attempt_booking(driver):
    while True:
        is_tickets_available(driver)
        driver.refresh()
        time.sleep(30)

def main():
    driver = start_driver()
    open_ticket_page(driver)
    attempt_booking(driver)

if __name__ == "__main__":
    send_twilio_sms("🚀 Test WhatsApp Render OK")
    main()
