import os
import pickle
import time

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


def check_directory():
    if not os.path.exists("cookies"):
        os.mkdir("cookies")


def check_cookies_exist(name):
    if os.path.exists("cookies/{}.pkl".format(name)):
        return True
    else:
        return False


def cookies_create(name, cookies1):
    file_name = "cookies/" + name + ".pkl"
    with open(file_name, "wb") as f:
        pickle.dump(cookies1, f)


def get_cookies(name):
    file_name = "cookies/" + name + ".pkl"
    if os.path.exists(file_name):
        with open(file_name, "rb") as f:
            cooki = pickle.load(f)
        return cooki
    else:
        return None


def check_status(driver):
    check = False
    url = "https://www.instagram.com/"
    driver.get(url)
    time.sleep(3)
    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//span[@class='_2dbep qNELH']")))
        check = True
    except Exception as e:
        print(e)
        print("not login")
        pass


    if check == True:
        return True
    else:
        return False


def add_cookies(name, driver):
    cook = get_cookies(name)
    if cook:
        driver.get("https://www.instagram.com")
        for k in cook:
            try:
                driver.add_cookie(k)
            except:
                pass
