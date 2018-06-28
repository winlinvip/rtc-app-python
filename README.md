# rtc-app-python

Python AppServer for AliRTC.

* [CentOS 6](#centos6)
* [MacPro](#macpro)
* [Windows](#windows)

## CentOS6

1. Setup Python:

```
(pip --version 2>/dev/null || sudo yum install -y python-pip) &&
git clone https://github.com/winlinvip/rtc-app-python.git && cd rtc-app-python &&
(rm -rf CherryPy-3.2.2 && unzip -q CherryPy-3.2.2.zip && cd CherryPy-3.2.2 && python setup.py install --user)
```

2. Install AliRTC OpenAPI SDK by:

```
pip install aliyun-python-sdk-rtc --user
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

6. Verify AppServer by [here](http://localhost:8080/app/v1/login?room=5678&user=nvivy&passwd=12345678).

> Remark: You can setup client native SDK by `http://30.2.228.19:8080/app/v1`.

> Remark: Please use your AppServer IP instead by `ifconfig eth0`.

## MacPro

1. Setup Python:

```
(pip --version 2>/dev/null || sudo easy_install pip) &&
git clone https://github.com/winlinvip/rtc-app-python.git && cd rtc-app-python &&
(rm -rf CherryPy-3.2.2 && unzip -q CherryPy-3.2.2.zip && cd CherryPy-3.2.2 && python setup.py install --user)
```

2. Install AliRTC OpenAPI SDK by:

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

6. Verify AppServer by [here](http://localhost:8080/app/v1/login?room=5678&user=nvivy&passwd=12345678).

> Remark: You can setup client native SDK by `http://30.2.228.19:8080/app/v1`.

> Remark: Please use your AppServer IP instead by `ifconfig en0`.

## Windows

1. Install Python from [here](https://www.python.org/downloads/release/python-2715/)

2. Download code `rtc-app-python-master.zip` from [here](https://github.com/winlinvip/rtc-app-python/archive/master.zip)

3. Unzip `rtc-app-python-master.zip` to directory `rtc-app-python-master`.

4. Unzip `CherryPy-3.2.2.zip` from `rtc-app-python-master`, then install by:

```
cd CherryPy-3.2.2
python setup.py install --user
```

5. Download `pycryptodome` from [here](https://pypi.org/project/pycryptodome/#files), then unzip and install by:

```
cd pycryptodome-*
python setup.py install --user
```

6. Download Core SDK from [here](https://pypi.org/project/aliyun-python-sdk-core/#files), then unzip and install by:

```
cd aliyun-python-sdk-core-*
python setup.py install --user
```

7. Download RTC SDK from [here](https://pypi.org/project/aliyun-python-sdk-rtc/#files), then unzip and install by:

```
cd aliyun-python-sdk-rtc-*
python setup.py install --user
```


8. Generate AK from [here](https://usercenter.console.aliyun.com/#/manage/ak):

```
AccessKeyID: OGAEkdiL62AkwSgs
AccessKeySecret: 4JaIs4SG4dLwPsQSwGAHzeOQKxO6iw
```

9. Create APP from [here](https://rtc.console.aliyun.com/#/manage):

```
AppID: iwo5l81k
```

10. Start AppServer, **use your information**:

```
python server.py --listen=8080 --access-key-id=OGAEkdiL62AkwSgs \
	--access-key-secret=4JaIs4SG4dLwPsQSwGAHzeOQKxO6iw --appid=iwo5l81k \
	--gslb=https://rgslb.rtc.aliyuncs.com
```

11. Verify AppServer by [here](http://localhost:8080/app/v1/login?room=5678&user=nvivy&passwd=12345678).

> Remark: You can setup client native SDK by `http://30.2.228.19:8080/app/v1`.

> Remark: Please use your AppServer IP instead by `ipconfig`.

## Links

AliRTC python OpenAPI SDK is [here](https://develop.aliyun.com/tools/sdk#/python).
