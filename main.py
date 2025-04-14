

import time
import logging
import smtplib
from email.mime.text import MIMEText
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

# Email credentials (use an app password if using Gmail)
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
SENDER_EMAIL = "rayane@may.fr"
SENDER_PASSWORD = "csxs zgqj noeu zmsu"  # Use an app-specific password if 2FA is enabled
TO_EMAIL = "tickrcsa@gmail.com"

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
    time.sleep(30)

def start_driver():
    logging.info("Starting WebDriver...")
    chrome_options = Options()
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--window-size=1920x1080")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    driver.maximize_window()
    logging.info("WebDriver started and window maximized.")
    return driver

def open_ticket_page(driver):
    url = "https://billetterie.rcstrasbourgalsace.fr/fr/acheter/billet-unite-tout-public-rcsa-as-saint-etienne-2024-jhmyrk2cizgu"
    driver.get(url)

def is_tickets_available(driver):
    sections = ["NORD", "OUEST", "EST"]
    
    for section in sections:
        try:
            button = driver.find_element(By.XPATH, f"//button[.//b[contains(text(), '{section}')]]")
            button.click()
            subject = "🎫 Billets disponibles !"
            message = f"Tickets trouvés dans la section {section} !"
            send_email_notification(subject, message)
            return False
        except:
            continue

def attempt_booking(driver):
    while True:
        is_tickets_available(driver)
        time.sleep(10)

        driver.refresh()



def main():
    subject = "LANCEMENT SAINT ETIENNE !"
    message = f"Début du watch des tickets de saint etienne !"
    send_email_notification(subject, message)
    driver = start_driver()
    open_ticket_page(driver)
    attempt_booking(driver)

if __name__ == "__main__":
    main()
