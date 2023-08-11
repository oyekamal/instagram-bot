import random
import sys
import time
import os
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
import cookies_hadler
from cookies_hadler import check_status

def drver():
    chrome_options = webdriver.ChromeOptions()
    # chrome_options.add_argument('--headless')
    chrome_options.add_argument("--start-maximized")
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--disable-software-rasterizer')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option('useAutomationExtension', False)
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    prefs = {"credentials_enable_service": False,
             "profile.password_manager_enabled": False}
    chrome_options.add_experimental_option("prefs", prefs)
    # service = Service()
    driver = webdriver.Chrome(ChromeDriverManager().install(), options=chrome_options)
    driver.get("https://www.google.com")
    # driver.maximize_window()
    return driver


def login_insta(driver, username, paswd):
    try:
        driver.get("https://www.instagram.com/accounts/login/")
        email = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//input[@name='username']")))
        email.send_keys(username)
        password = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//input[@name='password']")))
        password.send_keys(paswd)
        password.send_keys(Keys.RETURN)
        time.sleep(5)
        soup = str(driver.page_source)
        if "Sorry, your password was incorrect. Please double-check your password." in soup or "The username you entered doesn't belong to an account. Please check your username and try again." in soup:
            print("incorrect username or pass")

    except Exception as e:
        # print(e)
        print("some error")
    return driver


def insta_dm(driver, link, message):
    driver.get(link)
    mc = False
    try:
        driver.find_element(By.XPATH, "//button[@class='sqdOP  L3NKy    _8A5w5    ']").click()
        mc = True
    except:
        # print("here")
        try:
            private = WebDriverWait(driver, 10).until \
                (EC.presence_of_element_located((By.CLASS_NAME, "rkEop")))
            private = private.text
            if private == "This Account is Private":
                driver.find_element(By.CSS_SELECTOR,
                                    "section > div.XBGH5 > div.qF0y9.Igw0E.IwRSH.eGOV_.ybXk5._4EzTm.bPdm3 > div > div > button").click()
                time.sleep(2)
                with open('private_profiles.txt', 'a') as f:
                    f.write(str(f"{link}") + "\n")
        except:
            # print('here2')
            try:
                follow_button = driver.find_element(By.CLASS_NAME, '_5f5mN')
                follow_button.click()
                time.sleep(2)
                driver.find_element(By.XPATH, "//button[@class='sqdOP  L3NKy    _8A5w5    ']").click()
                mc = True
            except:
                pass
    if mc:
        time.sleep(3)
        #--------------without emoji---------------
        # action = ActionChains(driver)
        # action.send_keys(message)
        # action.perform()
        # time.sleep(3)
        # send_btn = driver.find_element(By.CSS_SELECTOR, 'div.qF0y9.Igw0E.IwRSH.eGOV_._4EzTm.JI_ht > button')
        # send_btn.click()
        # time.sleep(random.randint(20,30))

        #-----------------emoji-----------------------------
        element = driver.find_element(By.XPATH,
                                      "/html/body/div[1]/section/div/div[2]/div/div/div[2]/div[2]/div/div[2]/div/div/div[2]/textarea")

        driver.execute_script(f"console.log(arguments[0].innerHTML = '{message}')", element)
        action = ActionChains(driver)
        action.click(element)
        action.send_keys("c")
        action.send_keys(Keys.BACKSPACE)
        action.perform()
        element.send_keys(Keys.RETURN)
        time.sleep(2)
    pass
def start_task(num):
    try:
        with open("accounts_creds.txt", "r") as file:
            accounts = (file.read())
        with open("message.txt", "r",encoding="utf-8") as file:
            message = (file.read())
        with open("profile_links.txt", "r") as file:
            p_links = (file.read())
        p_links = p_links.split("\n")
        accounts = accounts.split("\n")
        message=message.split("\n")
        message=random.choice(message)

        start = 0
        end = num
        print("Start....")
        for cred in accounts:
            try:
                data = cred.split(":")
                name = data[0]
                password = data[1]


                driver = drver()
                cookies_hadler.check_directory()
                # check if cookies exist
                if not cookies_hadler.check_cookies_exist(name):
                    # if not then login using credentials
                    driver = login_insta(driver, name, password)
                    # save the cookies after successful login
                    if check_status(driver):
                        cookies_hadler.cookies_create(name, driver.get_cookies())
                else:
                    # if cookies exist add the cookies
                    cookies_hadler.add_cookies(name, driver)
                    # if cookies are not working properly login again
                    if not cookies_hadler.check_status(driver):
                        # login again using credentials if cookies are not working
                        driver = login_insta(driver, name, password)
                        # if login is successful save the cookies
                        if check_status(driver):
                            cookies_hadler.cookies_create(name, driver.get_cookies())
                try:
                    notif = WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located((By.XPATH,"//button[@class='aOOlW   HoLwm ']")))
                    notif.click()

                except:

                    pass
                try:
                    for link in p_links[start:end]:
                        insta_dm(driver,link,message)
                    start=end
                    end+=num

                except Exception as e:
                    # print(e)
                    pass
            except:pass
            time.sleep(random.randint(10, 15))
            driver.quit()

    except Exception as e:
        # print(e)
        pass

if __name__ == '__main__':
    #num of messages send to profiles per account
    num=int(input("Enter message num you want to send from 1 account: "))
    start_task(num)
