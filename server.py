#!/usr/bin/python
# -*- coding: UTF-8 -*-

from aliyunsdkcore.client import AcsClient
from aliyunsdkrtc.request.v20180111 import CreateChannelRequest

import sys, os, cherrypy, json, uuid, hashlib
from optparse import OptionParser

parser = OptionParser()
parser.add_option("-a", "--listen", dest="listen", help="Listen port")
parser.add_option("-b", "--access-key-id", dest="accessKeyID", help="ID of access key")
parser.add_option("-c", "--access-key-secret", dest="accessKeySecret", help="Secret of access key")
parser.add_option("-d", "--appid", dest="appID", help="ID of app")
parser.add_option("-e", "--gslb", dest="gslb", help="URL of GSLB")

(options, args) = parser.parse_args()
(listen, accessKeyID, accessKeySecret, appID, gslb) = (options.listen, options.accessKeyID, options.accessKeySecret, options.appID, options.gslb)

if None in (listen, accessKeyID, accessKeySecret, appID, gslb):
    print "Usage: %s <--listen=Listen> <--access-key-id=AccessKeyID> <--access-key-secret=AccessKeySecret> <--appid=AppID> <--gslb=GSLB>"%(sys.argv[0])
    print "     --listen              Server listen port"
    print "     --access-key-id       ID of access key"
    print "     --access-key-secret   Secret of access key"
    print "     --appid               ID of app"
    print "     --gslb                URL of GSLB"
    print "For example:"
    print "     %s --listen=8080 --access-key-id=OGAEkdiL62AkwSgs --access-key-secret=4JaIs4SG4dLwPsQSwGAHzeOQKxO6iw --appid=iwo5l81k --gslb=https://rgslb.rtc.aliyuncs.com"%(sys.argv[0])
    sys.exit(-1)

regionID= "cn-hangzhou"
print "Listen=%s, AccessKeyID=%s, AccessKeySecret=%s, RegionID=%s, AppID=%s, GSLB=%s"%(listen, accessKeyID, accessKeySecret, regionID, appID, gslb)

conf = {
    'global': {
        'server.socket_host': '0.0.0.0',
        'server.socket_port': int(listen)
    },
    '/': {
        'request.dispatch': cherrypy.dispatch.MethodDispatcher(),
    }
}

channels = {}

# https://help.aliyun.com/document_detail/74890.html
def sign(channelID, channelKey, appID, userID, session, nonce, timestamp):
    h = hashlib.sha256()
    h.update(channelID)
    h.update(channelKey)
    h.update(appID)
    h.update(userID)
    h.update(session)
    h.update(nonce)
    h.update(str(timestamp))
    return h.hexdigest()

class RESTLogin(object):
    exposed = True
    def __login(self, channelID, user, passwd):
        global channels
        channelUrl = "%s/%s"%(appID, channelID)
        if channelUrl not in channels:
            client = AcsClient(accessKeyID, accessKeySecret, regionID)
            request = CreateChannelRequest.CreateChannelRequest()
            request.set_AppId(appID)
            request.set_ChannelId(channelID)
            response = client.do_action_with_exception(request)
            print "request: %s, response: %s"%((appID, channelID), response)
            obj = json.loads(response)
            channels[channelUrl] = obj
        obj = channels[channelUrl]
        session = str(uuid.uuid1())
        (requestId, nonce, timestamp, channelKey) = (obj["RequestId"], obj["Nonce"], obj["Timestamp"], obj["ChannelKey"])
        token = sign(channelID, channelKey, appID, user, session, nonce, timestamp)
        print "url: %s, request: %s, response: %s, token: %s"%(channelUrl, (appID, channelID), (requestId, nonce, timestamp, channelKey), token)

        username = "%s?appid=%s&session=%s&channel=%s&nonce=%s&timestamp=%s"%(user, appID, session, channelID, nonce, str(timestamp))
        ret = json.dumps({"code":0, "data":{
            "appid": appID, "userid":user, "gslb":[gslb],
            "session": session, "token": token,
            "nonce": nonce, "timestamp": timestamp,
            "turn": {
                "username": username,
                "password": token
            }
        }})

        cherrypy.response.headers["Content-Type"] = "application/json"
        return ret
    def GET(self, room, user, passwd):
        return self.__login(room, user, passwd)
    def POST(self, room, user, passwd):
        return self.__login(room, user, passwd)
    def OPTIONS(self):
        cherrypy.response.headers["Access-Control-Allow-Origin"] = "*"
        cherrypy.response.headers["Access-Control-Allow-Methods"] = "GET, POST, HEAD, PUT, DELETE"
        allow_headers = ["Cache-Control", "X-Proxy-Authorization", "X-Requested-With", "Content-Type"]
        cherrypy.response.headers["Access-Control-Allow-Headers"] = ",".join(allow_headers)

class Root(object):
    exposed = True
    def GET(self):
        return "AppServer is OK"
class App(object):
    exposed = True
    def GET(self):
        return "AppServer is OK"
class V1(object):
    exposed = True
    def GET(self):
        return "AppServer is OK"

root = Root()
root.app = App()
root.app.v1 = V1()
root.app.v1.login = RESTLogin()
cherrypy.quickstart(root, '/', conf)
