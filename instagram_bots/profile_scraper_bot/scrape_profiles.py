import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
import time
import cookies_hadler
from cookies_hadler import check_status
import zipfile

import unicodedata

main_already=[]
#keyword
with open("filters/keywords.txt","r")as f:
    f=f.read()
    keywords=f.split(":")

#follower_count
with open("filters/min_follower_num.txt","r")as f:
    f=f.read()
    f=f.split(":")
    follower_num=int(f[0])
    following_num=int(f[1])

#depth
with open("filters/min_request_send.txt","r")as f:
    f=f.read()
    depth=int(f)

def del_link():
    with open("filters/initial_links.txt", 'r+') as fp:
        lines = fp.readlines()
        fp.seek(0)
        fp.truncate()
        fp.writelines(lines[1:])

def filter_data(link,driver):
    # link="https://www.instagram.com/bobby_f_shaddy/"
    try:
        if link not in main_already:
            driver.get(link)
            time.sleep(4)
            fnum = driver.find_elements(By.XPATH, "//span[@class='g47SY ']")
            fdata = []
            fcheck=[]
            check=False
            for n in fnum:
                fdata.append(n)
                fcheck.append(n.text)

            followers = fdata[1].get_attribute("title")
            followers = int(followers.replace(",",""))
            # print("fo: ",followers)
            followings = fdata[2].text
            followings = int(followings.replace(",",""))
            # print("fo: ", followings)

            if followers >= follower_num and followings >= following_num:
                try:
                    # bio = driver.find_element(By.CSS_SELECTOR, "section > div.QGPIr > div")
                    bio = driver.find_element(By.CSS_SELECTOR,
                                              "section > div.QGPIr > div._7UhW9.vy6Bb.MMzan.KV-D4.uL8Hv.T0kll")

                    bio = bio.text
                    bio = (unicodedata.normalize('NFKC', bio), bio)
                    bio = ((bio)[0])
                    bio = bio.lower()
                    # print(bio)
                    for keyword in keywords:
                        if keyword in bio:
                            # print("Output scrape this")
                            check=True
                            pass
                    if check:
                        with open('output/output_data.txt', 'a') as f:
                            f.write(str(f"{link}:{followers}:{followings}") + "\n")


                    else:
                        # print("waste link: ",link)
                        with open("output/waste_links.txt", "a")as fp:
                            fp.write(str(link) + "\n")

                except Exception as e:
                    # print(e)
                    with open("output/waste_links.txt", "a")as fp:
                        fp.write(str(link) + "\n")
    except:
        pass


def scrape_followers_profiles(link, driver):
    try:
        driver.get(link)
        time.sleep(4)
        username = link.split("/")[-2]
        try:
            follower = driver.find_element(By.XPATH, f"//a[@href='/{username}/following/']")
            follower.click()
            time.sleep(3)

            scr = driver.find_element(By.CLASS_NAME, "isgrP")
            profile_list = []
            scrolling = []
            while True:
                try:
                    value = driver.execute_script('return arguments[0].scrollTop = arguments[0].scrollHeight', scr)
                    # print(value)
                    if value in scrolling:
                        # print("break")
                        break
                    scrolling.append(value)
                    time.sleep(5)
                    plinks = driver.find_elements(By.XPATH, "//a[@class='notranslate _0imsa ']")

                except Exception as e:
                    # print(e)
                    break
            for p in plinks:
                link = p.get_attribute("href")
                profile_list.append(link)

            return profile_list
        except Exception as e:
            pass
            # print(e)
    except:
        pass

def main_function(initial_links,ldriver):
    change=1
    change_check=False
    try:
        # if len(initial_links)<100:
        #     print("less")
            for i in initial_links:
               try:
                    if not len(i) <= 1:
                        try:
                            sp=scrape_followers_profiles(i,ldriver)
                        except:

                            continue

                        #first del link
                        del_link()
                        #add its followers
                        with open("filters/initial_links.txt", "a")as fp:
                            for line in sp:
                                fp.write(str(line) + "\n")

                        for j in sp:
                            if len(j) < 1:
                                continue
                            filter_data(j,ldriver)
                            if change==depth:
                                change_check=True
                                break
                            change+=1
                        if change_check:
                            break
                    else:
                        del_link()
               except:
                   continue

        #
        # # elif len(initial_links)>100:
        #     print("gretaer")
        #     for i in initial_links:
        #         if not len(i) <= 1:
        #             filter_data(i,ldriver)
        #             del_link()
        #             if change == depth:
        #                 break
        #             change += 1
        #         else:
        #            del_link()

    except Exception as e:
        # print(e)
        pass

    pass

def derver(PROXY_HOST, PROXY_PORT, PROXY_USER, PROXY_PASS):
    # def zip_creator(PROXY_HOST, PROXY_PORT, PROXY_USER, PROXY_PASS):


    manifest_json = """
    {
        "version": "1.0.0",
        "manifest_version": 2,
        "name": "Chrome Proxy",
        "permissions": [
            "proxy",
            "tabs",
            "unlimitedStorage",
            "storage",
            "<all_urls>",
            "webRequest",
            "webRequestBlocking"
        ],
        "background": {
            "scripts": ["background.js"]
        },
        "minimum_chrome_version":"22.0.0"
    }
    """

    background_js = """
    var config = {
            mode: "fixed_servers",
            rules: {
            singleProxy: {
                scheme: "http",
                host: "%s",
                port: parseInt(%s)
            },
            bypassList: ["localhost"]
            }
        };

    chrome.proxy.settings.set({value: config, scope: "regular"}, function() {});

    function callbackFn(details) {
        return {
            authCredentials: {
                username: "%s",
                password: "%s"
            }
        };
    }

    chrome.webRequest.onAuthRequired.addListener(
                callbackFn,
                {urls: ["<all_urls>"]},
                ['blocking']
    );
    """ % (PROXY_HOST, PROXY_PORT, PROXY_USER, PROXY_PASS)
    return manifest_json, background_js


def drivers(plug, user_agent=None):
    chrome_options = webdriver.ChromeOptions()
    # chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--disable-software-rasterizer')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option('useAutomationExtension', False)
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    prefs = {"credentials_enable_service": False,
             "profile.password_manager_enabled": False}
    chrome_options.add_experimental_option("prefs", prefs)
    chrome_options.add_extension(plug)
    if user_agent:
        chrome_options.add_argument('--user-agent=%s' % user_agent)
    driver = webdriver.Chrome(ChromeDriverManager().install(), options=chrome_options)
    driver.maximize_window()
    return driver
def login_insta(driver,uname,paswd):
    try:
        driver.get("https://www.instagram.com/accounts/login/")
        email = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//input[@name='username']")))
        email.send_keys(uname)
        password = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//input[@name='password']")))
        password.send_keys(paswd)
        password.send_keys(Keys.RETURN)
        time.sleep(10)
        soup = str(driver.page_source)
        if "Sorry, your password was incorrect. Please double-check your password." in soup or "The username you entered doesn't belong to an account. Please check your username and try again." in soup:
            print("incorrect username or pass")
    except Exception as e:
        # print(e)
        pass
        # print("some error")
    return driver

def credentials():
    with open("accounts_creds.txt", "r")as f:
        f = f.read()
        accs = f.split("\n")
    account_break = False
    while True:
        for a in accs:
            if not len(a)<=0:
                creds=a.split(":")
                uname=creds[0]
                paswd=creds[1]
                PROXY_HOST = creds[2]
                PROXY_PORT = int(creds[3])
                PROXY_USER = creds[4]
                PROXY_PASS = creds[5]

                proxies = {
                    "http": f"http://{PROXY_USER}:{PROXY_PASS}@{PROXY_HOST}:{PROXY_PORT}/",
                    "https": f"http://{PROXY_USER}:{PROXY_PASS}@{PROXY_HOST}:{PROXY_PORT}/"
                }

                url = 'https://api.ipify.org'

                try:
                    response = requests.get(url, proxies=proxies)
                    assert response.text == PROXY_HOST
                    pluginfile = 'proxy_auth_plugin.zip'
                    manifest_json, background_js = derver(PROXY_HOST, PROXY_PORT, PROXY_USER, PROXY_PASS)
                    with zipfile.ZipFile(pluginfile, 'w') as zp:
                        zp.writestr("manifest.json", manifest_json)
                        zp.writestr("background.js", background_js)
                    driver = drivers(pluginfile)
                    # driver=derver(proxxy,porrt)
                    cookies_hadler.check_directory()
                    # check if cookies exist
                    if not cookies_hadler.check_cookies_exist(uname):
                        # if not then login using credentials
                        driver = login_insta(driver, uname, paswd)
                        # save the cookies after successful login
                        if check_status(driver):
                            cookies_hadler.cookies_create(uname, driver.get_cookies())
                    else:
                        # if cookies exist add the cookies
                        cookies_hadler.add_cookies(uname, driver)
                        # if cookies are not working properly login again
                        if not cookies_hadler.check_status(driver):
                            # login again using credentials if cookies are not working
                            driver = login_insta(driver, uname, paswd)
                            # if login is successful save the cookies
                            if check_status(driver):
                                cookies_hadler.cookies_create(uname, driver.get_cookies())
                    # ldriver=login(driver,uname,paswd)
                    while True:
                        with open("filters/initial_links.txt", "r")as f:
                            f = f.read()
                            initial_links = f.split("\n")

                        if len(initial_links) <= 1:

                            account_break = True
                            break
                        else:
                            main_function(initial_links, driver)
                            driver.quit()
                            break
                    if account_break:
                        driver.quit()
                        break
                except Exception as e:
                    # print(e)

                    with open("output/waste_proxies.txt", "a")as fp:
                        fp.write(str(a) + "\n")
                    continue
            else:
                break

        if account_break:
            break


    pass
if __name__ == '__main__':
    zz=input("Press enter to start")

    credentials()
    pass

