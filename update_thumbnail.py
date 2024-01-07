from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import geckodriver_autoinstaller

import time

import pickle

from selenium.webdriver.firefox.options import Options

COOKIES_PATH = "data/cookies"
URL = "https://studio.youtube.com/video/Xr3nGd1AqpA/edit"


def is_logged_in(driver) -> bool:
    driver.get(URL)
    return driver.title != "YouTube"


def save_cookies(driver):
    cookies = driver.get_cookies()
    pickle.dump(cookies, open(COOKIES_PATH, "wb"))

def load_cookies(driver):
    try:
        cookies = pickle.load(open(COOKIES_PATH, "rb"))
    except FileNotFoundError:
        print("No cookies generated yet")
        return

    driver.get("studio.youtube.com")
    for cookie in cookies:
        driver.add_cookie(cookie)
    driver.refresh()

def set_thumbnail(file_location):
    geckodriver_autoinstaller.install()
    print("gecko driver installed")

    profile = webdriver.FirefoxProfile(
        "/home/weasel/.mozilla/firefox/eczhy77c.default-release")

    opts = Options()
    opts.set_preference("dom.webdriver.enabled", False)
    opts.set_preference("useAutomationExtension", False)
    print("options set")
    opts.profile = profile
    print("profile created")

    driver = webdriver.Firefox(opts)
    print("driver created")
    try:

        if is_logged_in(driver):
            print("Already logged in")
        else:
            print("Not logged in. Login")
            #login()
            input()

        #save_cookies(driver)

        time.sleep(2)

        elem = driver.find_element(By.XPATH, "//input[@type='file']")
        elem.send_keys(file_location)
        print("sending keys")
        time.sleep(2)
        driver.find_element(By.ID, "save").click()
        print("it should now be uploading")
        time.sleep(8)
    except Exception as e:
        print(e)
    finally:
        driver.quit()
