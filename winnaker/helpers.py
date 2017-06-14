# -*- coding: utf-8 -*-
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import WebDriverException
import time
from datetime import datetime

# from selenium.common.exceptions import ElementNotVisibleException


def get_env(env_key, default):
    import os
    value = os.getenv(env_key)
    if value is None or len(value) == 0:
        return default
    return value

def post_to_hipchat(message, alert=False):
    import requests
    import os
    import json
    if alert:
        color = "red"
        notify = "true"
    else:
        color = "green"
        notify = "false"

    data = {
        "color": color,
        "message": message,
        "notify": notify,
        "message_format": "text"
    }

    post_url = os.environ['WINNAKER_HIPCHAT_POSTURL']
    headers = {'content-type': 'application/json', 'Accept-Charset': 'UTF-8'}
    r = requests.post(post_url, data=json.dumps(data), headers=headers)


def a_nice_refresh(driver):
    time.sleep(1)
    driver.refresh()
    print("Refreshing the browser ...")
    time.sleep(1)


def wait_for_xpath_presence(driver, xpath, be_clickable=False, TRY_UP_TO=10):
    wait = WebDriverWait(driver, 10)
    for try_count in range(TRY_UP_TO):
        try:
            if be_clickable:
                e = wait.until(EC.element_to_be_clickable((By.XPATH, xpath)))
            else:
                e = wait.until(
                    EC.presence_of_element_located((By.XPATH, xpath)))
            move_to_element(driver, e)
            return e
        except TimeoutException:
            print("Error: Could not find " + xpath)
            driver.save_screenshot("./outputs/debug" + now() + ".png")
            a_nice_refresh(driver)
        except StaleElementReferenceException:
            driver.save_screenshot("./outputs/debug" + now() + ".png")
            a_nice_refresh(driver)
    driver.save_screenshot("./outputs/error_driver_" + now() + ".png")


def move_to_element(driver, e, click=False):
    from selenium.webdriver.common.action_chains import ActionChains
    actions = ActionChains(driver)
    if click:
        actions.move_to_element(e).click().perform()
    else:
        actions.move_to_element(e).perform()


def get_body_text(driver):
    for i in range(5):
        try:
            e = wait_for_xpath_presence(driver, "//body")
            break
        except StaleElementReferenceException:
            a_nice_refresh(driver)
            e = wait_for_xpath_presence(driver, "//*")
            break
    return e.get_attribute("outerHTML")


# Subbornly clicks on the elements which run away from the DOM
def click_stubborn(driver, e, xpath):
    MAX_ATTEMPT = 6
    attempt = 0
    while attempt < MAX_ATTEMPT:
        try:
            for i in range(10):
                attempt += 1
                e.click()
                break
            # breaks if no exception happens
            break
        except StaleElementReferenceException:
            a_nice_refresh(driver)
            e = wait_for_xpath_presence(driver, xpath)
        except WebDriverException:
            break
    return e

def print_passed():
    print("""
    ******************
        PASSED
    ******************
    """)

def print_failed():
    print ("""
    !!!!!!!!!!!!!!!!!!
        FAILED
    !!!!!!!!!!!!!!!!!!
    """)

def now():
    return str(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
