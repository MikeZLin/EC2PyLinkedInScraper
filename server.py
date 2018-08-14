import cherrypy
import json
from lm import handler


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
            res = handler(params)     
            result['status'] = 200
            result['data'] = res
            cherrypy.response.status = result["status"]
            return jsonout (result).encode('utf8')
        except:
            result['status'] = 400
            result['data'] = "Error"
            cherrypy.response.status = result["status"]
            return jsonout (result).encode('utf8')
        
server2 = cherrypy._cpserver.Server()
server2.socket_port = 80
server2._socket_host = '0.0.0.0'
server2.thread_pool = 30
server2.subscribe ()


cherrypy.quickstart(server(), config="config.txt")
cherrypy.config["tools.encode.on"] = True
cherrypy.config["tools.encode.encoding"] = "utf-8"
