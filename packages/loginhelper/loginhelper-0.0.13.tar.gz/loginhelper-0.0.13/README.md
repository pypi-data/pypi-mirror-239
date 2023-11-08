# LoginHelper

The handle of the third login method for auto test.

such as: qq, wx(not implemented), ...

## Install

```bash
pip3 install -U loginhelper
```

## Usage

```python
import wda
import uiautomator2 as u2

from loginhelper import LoginHelper

if __name__ == '__main__':
    
    # ios
    deviceid = 'xxx'
    d = wda.USBClient(deviceid)
    
    # android
    # deviceid = 'xxx'
    # d = u2.connect(deviceid)
    
    lh = LoginHelper(d, deviceid, account='qq_acc', password='qq_pwd')
    lh.qqlogin()
```
