import cherrypy
import argparse
import atexit
from ProfileScraper import ProfileScraper
from selenium import webdriver
import json


#================================================
# Config
#------------------------------------------------
# Linked in Login details instead of using LI_AT cookie
login_opts = {'dologin':True, 'usr':'', 'p':''} # Todo: Modify from launch parameters or Post Request
#------------------------------------------------
parser = argparse.ArgumentParser(description='Launch Scraping Server')
parser.add_argument('--passkey', dest='apikey', nargs='?',default='', help='passkey to make the the scraper only respond private requests')
args = parser.parse_args()

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
        body = cherrypy.request.body.read().decode()
        params = json.loads(body)
        result = {}
        cherrypy.response.headers['Content-type'] = "application/json"
        try:
            print('request key',params['key'] )
        except:
            params['key'] = ''
        if args.apikey == params['key']:
            if params['url']:
                with ProfileScraper(driver=driver,login=login_opts) as scraper:
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
