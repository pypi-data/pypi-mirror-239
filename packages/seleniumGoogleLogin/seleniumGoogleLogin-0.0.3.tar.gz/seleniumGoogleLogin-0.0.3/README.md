# Author:KuoYuan Li 
auto login google account by selenium chrome driver 
##### installation Note 
Need selenium 4(above) and webdriver_manager to get the chromedriver automatically. 
if the version is not correction , please uninstall the selenium and install again. 
##### Sample code
```
import sleniumGoogleLogin
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager

driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
eamil = "your g-mail"
password = "your password"
if sleniumGoogleLogin.start(driver,email, password):print('ok')
```



License
----

MIT
