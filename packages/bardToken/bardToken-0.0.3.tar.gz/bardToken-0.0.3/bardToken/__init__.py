from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import seleniumGoogleLogin

def get(driver,waitTime=5):
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

if __name__ == '__main__':
    print("*******************************")
    email = 'your gmail'
    password = 'your password'
    #start chromedriver
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
    #google auth
    if seleniumGoogleLogin.start(driver,email, password):
        #get bard token
        token = get(driver)
        print(token)
    
    