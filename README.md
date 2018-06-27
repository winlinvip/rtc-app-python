# rtc-app-python

Python AppServer for AliRTC.

## MacPro

1. Setup Python:

```
git clone https://github.com/winlinvip/rtc-app-python.git && cd rtc-app-python &&
(pip --version 2>/dev/null || sudo easy_install pip) &&
(rm -rf CherryPy-3.2.2 && unzip -q CherryPy-3.2.2.zip && cd CherryPy-3.2.2 && python setup.py install --user)
```

2. Install AliRTC OpenAPI SDK:

```
sudo pip install aliyun-python-sdk-rtc
```

3. Generate AK from [here](https://usercenter.console.aliyun.com/#/manage/ak):

```
AccessKeyID: OGAEkdiL62AkwSgs
AccessKeySecret: 4JaIs4SG4dLwPsQSwGAHzeOQKxO6iw
```

4. Create APP from [here](https://rtc.console.aliyun.com/#/manage):

```
AppID: iwo5l81k
```

5. Start AppServer, **use your information**:

```
./server.py --listen=8080 --access-key-id=OGAEkdiL62AkwSgs \
	--access-key-secret=4JaIs4SG4dLwPsQSwGAHzeOQKxO6iw --appid=iwo5l81k \
	--gslb=https://rgslb.rtc.aliyuncs.com
```

6. Verify AppServer:

http://localhost:8088/app/v1/login?room=5678&user=nvivy&passwd=12345678

> Remark: You can setup client SDK `http://30.2.228.19:8080/app/v1`.

> Remark: Please use your AppServer IP instead by `ifconfig en0`.

## Links

AliRTC python OpenAPI SDK is [here](https://develop.aliyun.com/tools/sdk#/python).
