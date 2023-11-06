# Author:KuoYuan Li 
auto login google account by selenium chrome driver 
##### installation Note 
Need selenium 4(or newer) and webdriver_manager to get the chromedriver automatically. 
if the version dose not matcch , please uninstall the selenium and install again. 

bardapi is used in sample code 
and should be installed to insure it work normaly 
```
pip install bardapi
```
##### Sample code
```
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from bardapi import Bard
import seleniumGoogleLogin
import bardToken
email = 'your gmail'
password = 'your password'
#start chromedriver
driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
#google auth
if seleniumGoogleLogin.start(driver,email, password):
    #get bard token
    token = bardToken.get(driver)
    print(token)
    bard = Bard(token=token)
    ans = bard.get_answer("is there any bard api?")['content']
    print(ans)
```



License
----

MIT
