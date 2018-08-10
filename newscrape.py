
def lambda_handler(event, context=''):
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--window-size=1280x1696')
    chrome_options.add_argument('user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36')
    driver = webdriver.Chrome(chrome_options=chrome_options)
    with ProfileScraper(driver=driver) as scraper:
        profile = scraper.scrape(url="https://www.linkedin.com/in/julienhofer/")
    print(profile.to_dict())
    return(profile.to_dict()) 