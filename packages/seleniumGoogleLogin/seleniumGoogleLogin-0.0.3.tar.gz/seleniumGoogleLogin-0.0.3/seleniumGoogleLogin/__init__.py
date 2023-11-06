from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def start(driver,email, password):
    driver.get('https://accounts.google.com/ServiceLogin')
    try:
        WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.NAME, 'identifier'))).send_keys(f'{email}\n')
        WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="password"]/div[1]/div/div[1]/input'))).send_keys(f'{password}\n')
        WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.ID, 'sdgBod')))
    except: print('over time!!');return False 
    return True
'''
def getBardToken(driver,waitTime=5):
    #check if already Auth with google account
    cookies = driver.get_cookies()
    isGoogleAuth = False
    for cookie in cookies:
        if("__Secure-3PSID" in cookie["name"]):
            isGoogleAuth=True;break
    if not isGoogleAuth:print('please run googleLogin(email,password) first...');return ""
    
    driver.get("https://bard.google.com")
    #e=driver.find_element(By.XPATH, '//*[@id="gb"]/div[2]/div[3]/div[1]/a');print(e.location['x'])
    #click login...
    try:WebDriverWait(driver, waitTime).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="gb"]/div[2]/div[3]/div[1]/a'))).click()
    except:pass
    try:
        #be sure to get into bard GUI
        WebDriverWait(driver, waitTime).until(EC.visibility_of_element_located((By.TAG_NAME, 'chat-app')))
        cookies = driver.get_cookies()
        for cookie in cookies:
            if cookie["name"] == "__Secure-1PSID":
                return cookie["value"]
    except:print("run out of time,while get in to Bard GUI")
    return ""
'''
if __name__ == '__main__':
    print("*******************************")
    email = 'your google account'
    password = 'your password'
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
    if start(driver,email, password):print('ok')
    '''
    if start(driver,email, password):
        token = getBardToken(driver)
        print(token)
    '''
    