import atexit
from ProfileScraper import ProfileScraper
from selenium import webdriver
import json
import os

#================================================
# Config
#------------------------------------------------
# Linked in Login details instead of using LI_AT cookie
cookie = 'AQEDASfurQADPjbSAAABZSQtFdkAAAFlSDmZ2U4AZL-Dcf1UfuhABoNEiWUqwsZBk_BZYTdPARPEQAEXg7OZTqWc5QzxUn6fZikTw6JV43Ir8P4xSsdIl4AElUyRHOPUf7q28mw4hWV7LgTQYqFQ_Vaa'
#------------------------------------------------


chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-gpu')
chrome_options.add_argument('--window-size=1280x1696')
chrome_options.add_argument('--user-data-dir=/tmp/user-data')
chrome_options.add_argument('--hide-scrollbars')
chrome_options.add_argument('--enable-logging')
chrome_options.add_argument('--log-level=0')
chrome_options.add_argument('--v=99')
chrome_options.add_argument('--single-process')
chrome_options.add_argument('--data-path=/tmp/data-path')
chrome_options.add_argument('--ignore-certificate-errors')
chrome_options.add_argument('--homedir=/tmp')
chrome_options.add_argument('--disk-cache-dir=/tmp/cache-dir')
chrome_options.add_argument('user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36')
chrome_options.binary_location = os.getcwd() + "/bin/headless-chromium"
driver = webdriver.Chrome(chrome_options=chrome_options)

def closeDriver():
    global driver
    driver.close()
atexit.register(closeDriver)


def handler(params,context=''):
    global cookie
    if 'key' in params.keys():
        cookie = params['key']        
    if 'url' in params.keys():
        try:
            with ProfileScraper(driver=driver,cookie=cookie) as scraper:
                profile = scraper.scrape(url=params['url'])            
            return profile.to_dict()
        except Exception as e:
            return e