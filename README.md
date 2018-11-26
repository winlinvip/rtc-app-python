# rtc-app-python

Python AppServer for AliRTC.

* [CentOS 6](#centos6)
* [MacPro](#macpro)
* [Windows](#windows)

You could also write AppServer by following languages:

* Golang: https://github.com/winlinvip/rtc-app-golang
* Java: https://github.com/winlinvip/rtc-app-java
* Python: https://github.com/winlinvip/rtc-app-python
* C#: https://github.com/winlinvip/rtc-app-csharp
* Nodejs: https://github.com/winlinvip/rtc-app-nodejs
* PHP: https://github.com/winlinvip/rtc-app-php

For RTC deverloper:

* RTC [workflow](https://help.aliyun.com/document_detail/74889.html).
* RTC [token generation](https://help.aliyun.com/document_detail/74890.html).

Use OpenAPI to create channel:

* Golang: https://help.aliyun.com/document_detail/74890.html#channel-golang
* Java: https://help.aliyun.com/document_detail/74890.html#channel-java
* Python: https://help.aliyun.com/document_detail/74890.html#channel-python
* C#: https://help.aliyun.com/document_detail/74890.html#channel-csharp
* Nodejs: https://help.aliyun.com/document_detail/74890.html#channel-nodejs
* PHP: https://help.aliyun.com/document_detail/74890.html#channel-php

Token generation algorithm:

* Golang: https://help.aliyun.com/document_detail/74890.html#token-golang
* Java: https://help.aliyun.com/document_detail/74890.html#token-java
* Python: https://help.aliyun.com/document_detail/74890.html#token-python
* C#: https://help.aliyun.com/document_detail/74890.html#token-csharp
* Nodejs: https://help.aliyun.com/document_detail/74890.html#token-nodejs
* PHP: https://help.aliyun.com/document_detail/74890.html#token-php

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

> Remark: There maybe some errors, please ignore them.

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

6. Verify  your AppServer by [here](http://ossrs.net/talks/ng_index.html#/rtc-check?schema=http&host=127.0.0.1&port=8080&path=/app/v1/login&room=1237&user=jzufp&password=12345678) or [verify token](http://ossrs.net/talks/ng_index.html#/token-check).

![AppServer Success](https://github.com/winlinvip/rtc-app-golang/raw/master/images/app-ok.png)

![AppServer Failed](https://github.com/winlinvip/rtc-app-golang/raw/master/images/app-failed.png)

![AppServer Error Recovered](https://github.com/winlinvip/rtc-app-golang/raw/master/images/app-recovered.png)

> Remark: You can setup client native SDK by `http://30.2.228.19:8080/app/v1`.

> Remark: Please use your AppServer IP instead by `ifconfig eth0`.

## MacPro

1. Install `pip` for Python:

```
pip --version 2>/dev/null || sudo easy_install pip
```

or

```
url='https://files.pythonhosted.org/packages/ae/e8/2340d46ecadb1692a1e455f13f75e596d4eab3d11a57446f08259dee8f02/pip-10.0.1.tar.gz#sha256=f2bd08e0cd1b06e10218feaf6fef299f473ba706582eb3bd9d52203fdbd7ee68' &&
pip --version 2>/dev/null || (wget $url -O pip-10.0.1.tar.gz
tar xf pip-10.0.1.tar.gz && cd pip-10.0.1 &&
sudo python setup.py install)
```

2. Setup Python:

```
git clone https://github.com/winlinvip/rtc-app-python.git && cd rtc-app-python &&
(rm -rf CherryPy-3.2.2 && unzip -q CherryPy-3.2.2.zip && cd CherryPy-3.2.2 && python setup.py install --user)
```

3. Install AliRTC OpenAPI SDK by:

```
sudo pip install aliyun-python-sdk-rtc
```

> Remark: There maybe some errors, please ignore them.

4. Generate AK from [here](https://usercenter.console.aliyun.com/#/manage/ak):

```
AccessKeyID: OGAEkdiL62AkwSgs
AccessKeySecret: 4JaIs4SG4dLwPsQSwGAHzeOQKxO6iw
```

5. Create APP from [here](https://rtc.console.aliyun.com/#/manage):

```
AppID: iwo5l81k
```

6. Start AppServer, **use your information**:

```
./server.py --listen=8080 --access-key-id=OGAEkdiL62AkwSgs \
	--access-key-secret=4JaIs4SG4dLwPsQSwGAHzeOQKxO6iw --appid=iwo5l81k \
	--gslb=https://rgslb.rtc.aliyuncs.com
```

7. Verify  your AppServer by [here](http://ossrs.net/talks/ng_index.html#/rtc-check?schema=http&host=127.0.0.1&port=8080&path=/app/v1/login&room=1237&user=jzufp&password=12345678) or [verify token](http://ossrs.net/talks/ng_index.html#/token-check).

![AppServer Success](https://github.com/winlinvip/rtc-app-golang/raw/master/images/app-ok.png)

![AppServer Failed](https://github.com/winlinvip/rtc-app-golang/raw/master/images/app-failed.png)

![AppServer Error Recovered](https://github.com/winlinvip/rtc-app-golang/raw/master/images/app-recovered.png)

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

11. Verify  your AppServer by [here](http://ossrs.net/talks/ng_index.html#/rtc-check?schema=http&host=127.0.0.1&port=8080&path=/app/v1/login&room=1237&user=jzufp&password=12345678) or [verify token](http://ossrs.net/talks/ng_index.html#/token-check).

![AppServer Success](https://github.com/winlinvip/rtc-app-golang/raw/master/images/app-ok.png)

![AppServer Failed](https://github.com/winlinvip/rtc-app-golang/raw/master/images/app-failed.png)

![AppServer Error Recovered](https://github.com/winlinvip/rtc-app-golang/raw/master/images/app-recovered.png)

> Remark: You can setup client native SDK by `http://30.2.228.19:8080/app/v1`.

> Remark: Please use your AppServer IP instead by `ipconfig`.

## Links

AliRTC python OpenAPI SDK is [here](https://develop.aliyun.com/tools/sdk#/python).

## History

* [08c35a1](https://github.com/winlinvip/rtc-app-python/commit/08c35a133f85149c72ecd63276d66e784a487c11), Update SessionID generation algorithm.
* [4dc6a0b](https://github.com/winlinvip/rtc-app-python/commit/4dc6a0b69bb053e0e641377baddd753cd37ffc4f), Support recover for some OpenAPI error.
* [04399bd](https://github.com/winlinvip/rtc-app-python/commit/04399bd0ba43ec66f30e176c8b732bf64a8b815d), Log the request id and cost in ms.
* [d41e5dd](https://github.com/winlinvip/rtc-app-python/commit/d41e5dd029d73c73ea5fe18016b3337bd5433778), Use HTTP, x3 times faster than HTTPS.
* [8ef1883](https://github.com/winlinvip/rtc-app-python/commit/8ef1883f438ed08dc1835cc8af100acb76f94608), Set endpoint to get correct error.
* Support create channel and sign user token.
