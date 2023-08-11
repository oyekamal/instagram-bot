import random
import threading
import time
from tkinter import*
from tkinter.messagebox import showinfo

import requests
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager

import cookies_hadler
from cookies_hadler import check_status

# with open("comments.txt", "r",encoding="utf-8")as f:
#     f = f.read()
#     comments = f.split("\n")
def drver():

    chrome_options = webdriver.ChromeOptions()
    #chrome_options = webdriver.FirefoxOptions()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument("--start-maximized")
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--disable-software-rasterizer')
    chrome_options.add_argument('--no-sandbox')
    # chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    # chrome_options.add_experimental_option('useAutomationExtension', False)
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    prefs = {"credentials_enable_service": False,
             "profile.password_manager_enabled": False}
    # chrome_options.add_experimental_option("prefs", prefs)
    # service = Service()
    driver = webdriver.Chrome(ChromeDriverManager().install(), options=chrome_options)
    #driver = webdriver.Firefox( options=chrome_options)

    driver.get("https://www.google.com")
    # driver.maximize_window()
    return driver


def login_insta(driver, username, paswd):
    check = False
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
        # try:
        #     WebDriverWait(driver, 10).until(
        #         EC.presence_of_element_located((By.XPATH, "//span[@class='_2dbep qNELH']")))
        #     check=True
        # except Exception as e:
        #     print(e)
        #     print("not login")
        #     pass
    except Exception as e:
        print(e)
        print("some error")
    return driver


def like_post(driver, link):

    try:
        driver.get(link)
        like = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'section.ltpMr.Slqrh > span.fr66n > button')))
        like.click()
        time.sleep(5)

    except Exception as e:
        pass

        print(e)


def comment_post(driver, link, comnts):
    try:
        driver.get(link)
        try:
            comnt = random.choice(comnts)
            comment = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "textarea.Ypffh")))
            action = ActionChains(driver)
            action.click(on_element=comment)
            action.send_keys(comnt)
            action.perform()
            time.sleep(3)
            post_btn = driver.find_element(By.XPATH, '//button[@data-testid="post-comment-input-button"]')
            post_btn.click()
            time.sleep(3)

        except Exception as e:
            print(e)
            print("cant comment")

    except:
        pass

def like_comment(driver, link, comnts):
    try:
        driver.get(link)
        like = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'section.ltpMr.Slqrh > span.fr66n > button')))
        like.click()
        time.sleep(random.randint(2, 5))
        try:
            comnt=random.choice(comnts)
            comment = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "textarea.Ypffh")))
            action = ActionChains(driver)
            action.click(on_element=comment)
            action.send_keys(comnt)
            action.perform()
            time.sleep(3)
            post_btn = driver.find_element(By.XPATH, '//button[@data-testid="post-comment-input-button"]')
            post_btn.click()
            time.sleep(3)


        except Exception as e:
            print(e)
            print("cant comment")

    except:
        pass


def follow(driver, link):
    try:
        driver.get(link)
        try:
            follow_btn_public = driver.find_element(By.XPATH,
                                                    "//button[@class='_5f5mN       jIbKX  _6VtSN     yZn4P   ']")
            follow_btn_public.click()
        except:

            try:
                follow_btn_private = driver.find_element(By.XPATH,
                                                         "//button[@class='sqdOP  L3NKy   y3zKF     ']")
                follow_btn_private.click()
                time.sleep(5)

            except:
                pass
            pass

    except:
        pass


def startt():

    if (startButton['state'] == NORMAL):
        startButton["state"] = DISABLED
    try:
        file = 'insta_accounts.txt'
        with open(file, "r") as file:
            lines = (file.read())

        lines = lines.split("\n")
        print(lines)
        m_link = entri.get()
        var = var1.get()
        comnt = text_box.get("1.0", END)
        comnt=comnt.split("\n")
        comnts=[x for x in comnt if x]
        try:
            lower=int(start_entry.get())
            lower=lower-1
            if lower<0:
                lower=0
        except:
            lower=0
        try:
            upper = int(end_entry.get())
        except:
            upper=5


        try:
            lowerd=int(start_dentry.get())
        except:
            lowerd=15
        try:
            upperd = int(end_dentry.get())
        except:
            upperd=25
        index=1
        for cred in lines[lower:upper]:
            try:
                vn.set(index)
                root.update()
                index += 1
                data = cred.split(":")
                name = data[0]
                password = data[1]
            # except:
            #     print("ccc")
            #     pass

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
                    if var==1:
                        like_post(driver, m_link)
                    elif var==2:
                        comment_post(driver, m_link, comnts)
                    elif var==3:
                        follow(driver, m_link)
                    elif var==4:
                        like_comment(driver, m_link, comnts)

                except Exception as e:
                    print("n")
                    print(e)
                    pass
                driver.quit()
                time.sleep(random.randint(lowerd, upperd))
            except:pass

        showinfo("Info","Task Completed")
        startButton['state'] = NORMAL
    except Exception as e:
        print(e)
        startButton['state'] = NORMAL

def m_start():
    try:
        t = threading.Thread(target=startt, )
        t.start()
    except:
        print("lmmm")
        startButton['state'] = NORMAL


if __name__ == '__main__':
    # if requests.get( "https://github.com/Gryffindor8/bot_checker/blob/main/Gohar").status_code == 200:
        root = Tk()
        root.title("Insta Bot")
        root.geometry('600x620')
        root.resizable(False, False)
        frame1 = Frame(root)
        frame1.grid(row=0, column=0, pady=15, padx=125)
        label = Label(frame1, text="Insta Like, Comment and Follow Bot", font=("Helvetica", 16))
        label.grid()
        frame2 = Frame(root)
        frame2.grid(row=1, column=0, pady=5)
        var1 = IntVar()
        R1 = Radiobutton(frame2, text="Like", variable=var1, value=1, font=("Helvetica", 12), )
        R1.grid(row=0, column=0, pady=5)

        R2 = Radiobutton(frame2, text="Comment", variable=var1, value=2, font=("Helvetica", 12))
        R2.grid(row=0, column=1, pady=5)

        R3 = Radiobutton(frame2, text="Follow", variable=var1, value=3, font=("Helvetica", 12))
        R3.grid(row=0, column=2, pady=5)

        R4 = Radiobutton(frame2, text="Both Like Comment", variable=var1, value=4, font=("Helvetica", 12))
        R4.grid(row=0, column=3, pady=5)
        # label = Label(frame2, text="Number", font=("Helvetica", 12))
        # label.grid(row=1, column=2, pady=5,)
        # ee = Entry(frame2, width=5, font=("Helvetica", 12))
        # ee.grid(row=2, column=2)
        frame21 = Frame(root)
        frame21.grid(row=2, column=0, pady=5)
        start_label = Label(frame21, text="Account Start: ", font=("Helvetica", 12))
        start_label.grid(row=1, column=0, pady=5)
        start_entry = Entry(frame21, takefocus=0, width=5, font=("Helvetica", 14))
        start_entry.grid(row=1, column=1, pady=5)
        start_entry.insert(END, 1)
        end_label = Label(frame21, text="  End: ", font=("Helvetica", 12))
        end_label.grid(row=1, column=2, pady=5)
        end_entry = Entry(frame21, takefocus=0, width=5, font=("Helvetica", 14))
        end_entry.grid(row=1, column=3, pady=5)
        end_entry.insert(END, 5)

        start_dlabel = Label(frame21, text="Delay From: ", font=("Helvetica", 12))
        start_dlabel.grid(row=2, column=0, pady=5)
        start_dentry = Entry(frame21, takefocus=0, width=5, font=("Helvetica", 14))
        start_dentry.grid(row=2, column=1, pady=5)
        start_dentry.insert(END, 15)
        end_dlabel = Label(frame21, text="  To: ", font=("Helvetica", 12))
        end_dlabel.grid(row=2, column=2, pady=5)
        end_dentry = Entry(frame21, takefocus=0, width=5, font=("Helvetica", 14))
        end_dentry.grid(row=2, column=3, pady=5)
        end_dentry.insert(END, 20)

        frame32 = Frame(root)
        frame32.grid(row=3, column=0, pady=5)

        label = Label(frame32, text="Enter Post or Profile Link", font=("Helvetica", 12))
        label.grid(row=0, column=2, pady=5)
        entri = Entry(frame32, width=40, font=("Helvetica", 14))
        entri.grid(row=1, column=2, pady=5)

        frame3 = Frame(root)
        frame3.grid(row=4, column=0, pady=5)
        label = Label(frame3, text="Enter Comment Below", font=("Helvetica", 12))
        label.grid(row=0, column=2, pady=5)
        text_box = Text(frame3, width=60, height=8, font=("Helvetica", 12))
        text_box.grid(row=1, column=2, pady=5)

        frame4 = Frame(root)
        frame4.grid(row=5, column=0, pady=10, )
        startButton = Button(frame4, text='Start', height=1, width=10, bg="lightgrey", disabledforeground="white",
                             font=("Helvetica", 14), command=m_start)
        startButton.grid(row=0, column=2, pady=5)

        frame5 = LabelFrame(root, text="Output", labelanchor="n", font=("Helvetica", 12))
        frame5.grid(row=6, column=0, pady=5, padx=40, )
        sucs_label = Label(frame5, text="Processing account num: ", font=("Helvetica", 12))
        sucs_label.grid(row=0, column=0, pady=10, padx=5)
        vn = IntVar()
        sucs_out = Label(frame5, text="0", textvariable=vn, font=("Helvetica", 12))
        sucs_out.grid(row=0, column=1, pady=10, padx=5)

        root.mainloop()

