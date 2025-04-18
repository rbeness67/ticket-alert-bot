import time
import logging
import smtplib
from email.mime.text import MIMEText
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

# Email credentials
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
SENDER_EMAIL = "rayane@may.fr"
SENDER_PASSWORD = "csxs zgqj noeu zmsu"
TO_EMAIL = "tickrcsa@gmail.com"

# URLs to monitor
URLS = [
    ("BILLET UNITE SAINT ETIENNE", "https://billetterie.rcstrasbourgalsace.fr/fr/acheter/billet-unite-tout-public-rcsa-as-saint-etienne-2024-jhmyrk2cizgu"),
    ("REVENTE SAINT ETIENNE", "https://billetterie.rcstrasbourgalsace.fr/fr/second/match-rcsa-as-saint-etienne/#bk879b632e-zone")  # Replace with actual second URL
]

def send_email_notification(subject, message):
    """Send an email using SMTP."""
    msg = MIMEText(message)
    msg['Subject'] = subject
    msg['From'] = SENDER_EMAIL
    msg['To'] = TO_EMAIL

    try:
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(SENDER_EMAIL, SENDER_PASSWORD)
            server.send_message(msg)
            print("📧 Email sent!")
    except Exception as e:
        print(f"Error sending email: {e}")

def start_driver():
    logging.info("Starting WebDriver...")
    chrome_options = Options()
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--window-size=1920x1080")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    logging.info("WebDriver started.")
    return driver

def open_ticket_page(driver, url):
    driver.get(url)

def is_tickets_available(driver, match_name):
    sections = ["NORD", "OUEST", "EST"]
    
    for section in sections:
        try:
            button = driver.find_element(By.XPATH, f"//button[.//b[contains(text(), '{section}')]]")
            button.click()
            subject = f"🎫 Billets disponibles pour {match_name} !"
            message = f"Tickets trouvés dans la section {section} pour {match_name} !"
            send_email_notification(subject, message)
            return True
        except:
            continue
    return False

def monitor_once(match_name, url):
    subject = f"🎯 Watch lancé pour {match_name}"
    message = f"Recherche de billets pour {match_name}..."
    send_email_notification(subject, message)

    driver = start_driver()
    try:
        open_ticket_page(driver, url)
        if is_tickets_available(driver, match_name):
            print(f"✅ Tickets found for {match_name}!")
        else:
            print(f"❌ No tickets for {match_name}.")
    except Exception as e:
        print(f"Error during monitoring {match_name}: {e}")
    finally:
        driver.quit()

def main():
    while True:
        for match_name, url in URLS:
            print(f"🔍 Checking {match_name}...")
            monitor_once(match_name, url)
            print("⏱️ Waiting 30 seconds before next match...")
            time.sleep(30)

if __name__ == "__main__":
    main()
