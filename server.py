import cherrypy
import atexit
from ProfileScraper import ProfileScraper
from selenium import webdriver
import json


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
chrome_options.add_argument('user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36')
driver = webdriver.Chrome(chrome_options=chrome_options)

def closeDriver():
    global driver
    driver.close()
atexit.register(closeDriver)

def jsonout (res):
    cherrypy.response.headers['Content-type'] = "application/json"
    #return json.dumps(res, indent=3)
    #Make the output as small as possible by using short separators
    return json.dumps(res, separators=(',',':'))
class server(object):
    @cherrypy.expose
    def default(self,*args,**kwargs):
        """Return the emails sent to/from the candidate that fulfill certain conditions"""
        global cookie
        body = cherrypy.request.body.read().decode()
        params = json.loads(body)
        result = {}
        cherrypy.response.headers['Content-type'] = "application/json"
        if 'key' in params.keys():
            cookie = params['key']        
        if 'url' in params.keys():
            with ProfileScraper(driver=driver,cookie=cookie) as scraper:
                profile = scraper.scrape(url=params['url'])            
            result['status'] = 200
            result['data'] = profile.to_dict() 
            cherrypy.response.status = result["status"]
            return jsonout (result)
    
        result['status'] = 400
        result['data'] = "Error"
        result['status'] = 200
        result['data'] = profile.to_dict() 
        cherrypy.response.status = result["status"]
        return jsonout (result)


server2 = cherrypy._cpserver.Server()
server2.socket_port = 80
server2._socket_host = '0.0.0.0'
server2.thread_pool = 30
server2.subscribe ()


cherrypy.quickstart(server(), config="config.txt")
cherrypy.config["tools.encode.on"] = True
cherrypy.config["tools.encode.encoding"] = "utf-8"