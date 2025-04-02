#!/usr/bin/env bash

# Créer un dossier temporaire local
mkdir -p /opt/chrome
mkdir -p /opt/chromedriver

# Installer Chrome stable
apt-get update
apt-get install -y wget unzip curl gnupg ca-certificates fonts-liberation libappindicator3-1 libasound2 libatk-bridge2.0-0 \
  libatk1.0-0 libcups2 libdbus-1-3 libgdk-pixbuf2.0-0 libnspr4 libnss3 libx11-xcb1 libxcomposite1 libxdamage1 libxrandr2 \
  xdg-utils libu2f-udev libvulkan1

wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
apt install -y ./google-chrome-stable_current_amd64.deb

# Installer ChromeDriver dans /opt/chromedriver
wget -O /tmp/chromedriver.zip https://chromedriver.storage.googleapis.com/114.0.5735.90/chromedriver_linux64.zip
unzip /tmp/chromedriver.zip -d /opt/chromedriver
chmod +x /opt/chromedriver/chromedriver
