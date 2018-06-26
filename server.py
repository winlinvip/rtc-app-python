#!/usr/bin/python
# -*- coding: UTF-8 -*-

from aliyunsdkcore.client import AcsClient
from aliyunsdkrtc.request.v20180111 import CreateChannelRequest

import sys, os, cherrypy, json, uuid, hashlib

if len(sys.argv) < 6:
    print "Usage: %s <Listen> <AccessKeyID> <AccessKeySecret> <AppID> <GSLB>"%(sys.argv[0])
    print "For example:"
    print "     %s 8080 OGAEkdiL62AkwSgs 4JaIs4SG4dLwPsQSwGAHzeOQKxO6iw iwo5l81k https://rgslb.rtc.aliyuncs.com"%(sys.argv[0])
    sys.exit(-1)

(listen, accessKeyID, accessKeySecret, appID, gslb) = sys.argv[1:]
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
        if channelID not in channels:
            client = AcsClient(accessKeyID, accessKeySecret, regionID)
            request = CreateChannelRequest.CreateChannelRequest()
            request.set_AppId(appID)
            request.set_ChannelId(channelID)
            response = client.do_action_with_exception(request)
            print "request: %s, response: %s"%((appID, channelID), response)
            obj = json.loads(response)
            channels[channelID] = obj
        obj = channels[channelID]
        session = str(uuid.uuid1())
        (requestId, nonce, timestamp, channelKey) = (obj["RequestId"], obj["Nonce"], obj["Timestamp"], obj["ChannelKey"])
        token = sign(channelID, channelKey, appID, user, session, nonce, timestamp)
        print "request: %s, response: %s, token: %s"%((appID, channelID), (requestId, nonce, timestamp, channelKey), token)

        ret = json.dumps({"code":0, "data":{
            "appid": appID, "userid":user, "gslb":[gslb],
            "session": session, "token": token,
            "nonce": nonce, "timestamp": timestamp
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
class App(object):
    exposed = True
class V1(object):
    exposed = True

root = Root()
root.app = App()
root.app.v1 = V1()
root.app.v1.login = RESTLogin()
cherrypy.quickstart(root, '/', conf)
