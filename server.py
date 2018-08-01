#!/usr/bin/python
# -*- coding: UTF-8 -*-

from aliyunsdkcore.client import AcsClient
from aliyunsdkrtc.request.v20180111 import CreateChannelRequest

import aliyunsdkcore.profile.region_provider as rtc_user_config
import aliyunsdkcore.request as rtc_request
import aliyunsdkcore.http.protocol_type as rtc_protocol_type

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

regionID = "cn-hangzhou"
endpoint = "rtc.aliyuncs.com"
print "Listen=%s, AccessKeyID=%s, AccessKeySecret=%s, RegionID=%s, AppID=%s, GSLB=%s, endpoint=%s"%(
    listen, accessKeyID, accessKeySecret, regionID, appID, gslb, endpoint)

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

def create_channel(app_id, channel_id,
    access_key_id, access_key_secret, region_id, endpoint
):
    client = AcsClient(access_key_id, access_key_secret, region_id)
    request = CreateChannelRequest.CreateChannelRequest()
    request.set_AppId(app_id)
    request.set_ChannelId(channel_id)

    # Strongly recomment to set the RTC endpoint,
    # because the exception is not the "right" one if not set.
    # For example, if access-key-id is invalid:
    #      1. if endpoint is set, exception is InvalidAccessKeyId.NotFound
    #      2. if endpoint isn't set, exception is SDK.InvalidRegionId
    # that's caused by query endpoint failed.
    # @remark SDk will cache endpoints, however it will query endpoint for the first
    #      time, so it's good for performance to set the endpoint.
    if request.get_product() not in rtc_user_config.user_config_endpoints:
        rtc_user_config.modify_point(request.get_product(), region_id, endpoint)

    # Use HTTP, x3 times faster than HTTPS.
    rtc_request.set_default_protocol_type(rtc_protocol_type.HTTP)

    response = client.do_action_with_exception(request)
    obj = json.loads(response)
    return obj

# https://help.aliyun.com/document_detail/74890.html
def sign(channel_id, channel_key,
    app_id, user_id, session, nonce, timestamp
):
    h = hashlib.sha256()
    h.update(channel_id)
    h.update(channel_key)
    h.update(app_id)
    h.update(user_id)
    h.update(session)
    h.update(nonce)
    h.update(str(timestamp))
    token = h.hexdigest()
    return token

class RESTLogin(object):
    exposed = True
    def __login(self, channelID, user, passwd):
        global channels
        channelUrl = "%s/%s"%(appID, channelID)
        if channelUrl not in channels:
            obj = create_channel(appID, channelID, accessKeyID, accessKeySecret, regionID, endpoint)
            print "request: %s, response: %s"%((appID, channelID), obj)
            channels[channelUrl] = obj
        obj = channels[channelUrl]

        (userid, session) = (str(uuid.uuid1()), str(uuid.uuid1()))
        (requestId, nonce, timestamp, channelKey) = (obj["RequestId"], obj["Nonce"], obj["Timestamp"], obj["ChannelKey"])
        token = sign(channelID, channelKey, appID, userid, session, nonce, timestamp)
        print "url: %s, request: %s, response: %s, token: %s"%(channelUrl, (appID, channelID), (requestId, nonce, timestamp, channelKey), token)

        username = "%s?appid=%s&session=%s&channel=%s&nonce=%s&timestamp=%s"%(userid, appID, session, channelID, nonce, str(timestamp))
        ret = json.dumps({"code":0, "data":{
            "appid": appID, "userid":userid, "gslb":[gslb],
            "session": session, "token": token,
            "nonce": nonce, "timestamp": timestamp,
            "turn": {
                "username": username,
                "password": token
            }
        }})

        cherrypy.response.headers["Content-Type"] = "application/json"
        return ret
    def allow_cros(self):
        if "Origin" in cherrypy.request.headers:
            cherrypy.response.headers["Access-Control-Allow-Origin"] = "*"
            cherrypy.response.headers["Access-Control-Allow-Methods"] = "GET,POST,HEAD,PUT,DELETE,OPTIONS"
            cherrypy.response.headers["Access-Control-Expose-Headers"] = "Server,Range,Content-Length,Content-Range"
            cherrypy.response.headers["Access-Control-Allow-Headers"] = "Origin,Range,Accept-Encoding,Referer,Cache-Control,X-Proxy-Authorization,X-Requested-With,Content-Type"
    def GET(self, room, user, passwd):
        self.allow_cros()
        return self.__login(room, user, passwd)
    def POST(self, room, user, passwd):
        self.allow_cros()
        return self.__login(room, user, passwd)
    def OPTIONS(self, *args, **kwargs):
        self.allow_cros()
        return ""

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
