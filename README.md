# rtc-app-python

Python AppServer for AliRTC.

## MacPro

1. Setup Python:

```
(pip --version 2>/dev/null || sudo easy_install pip) &&
(rm -rf CherryPy-3.2.2 && unzip -q CherryPy-3.2.2.zip && cd CherryPy-3.2.2 && python setup.py install --user)
```

2. Install AliRTC [OpenAPI SDK](https://develop.aliyun.com/tools/sdk#/python):

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
# ./server.py <Listen> <AccessKeyID> <AccessKeySecret> <AppID> <GSLB>
./server.py 8080 OGAEkdiL62AkwSgs 4JaIs4SG4dLwPsQSwGAHzeOQKxO6iw iwo5l81k https://rgslb.rtc.aliyuncs.com
```

6. Setup Client SDK:

```
http://30.2.228.19:8088/app/v1
```

> Remark: Please use your AppServer IP instead.
