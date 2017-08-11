# -*- coding: utf-8 -*-
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import WebDriverException
import time
import logging
import os
import glob
from datetime import datetime
from retrying import retry
from os import listdir
from os.path import isfile, join
from os.path import basename
from winnaker.settings import *


# from selenium.common.exceptions import ElementNotVisibleException


def getScreenshotFiles():
    logging.debug("Getting the screenshot files in side " +
                  cfg_output_files_path)
    files = glob.glob("{}/*.png".format(cfg_output_files_path))
    logging.debug(files)
    return files


def post_to_hipchat(message, alert=False):
    import requests
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

    headers = {'content-type': 'application/json', 'Accept-Charset': 'UTF-8'}
    r = requests.post(
        cfg_hipchat_posturl,
        data=json.dumps(data),
        headers=headers)


def a_nice_refresh(driver):
    driver.refresh()
    logging.info("Refreshing the browser ...")
    time.sleep(1)

def wait_for_xpath_presence(driver,
        xpath,
        be_clickable=False,
        exponential_multiplier=cfg_wait_exponential_multiplier,
        exponential_max=cfg_wait_exponential_max,
        stop_max_attempt=cfg_retry_stop_max_attempt):
    @retry(
        wait_exponential_multiplier=exponential_multiplier,
        wait_exponential_max=exponential_max,
        stop_max_attempt_number=stop_max_attempt)
    def _wait_for_xpath_presence(driver, xpath, be_clickable):
        logging.debug("Waiting for XPATH: {}".format(xpath))
        wait = WebDriverWait(driver, 5)
        try:
            if be_clickable:
                e = wait.until(EC.element_to_be_clickable((By.XPATH, xpath)))
            else:
                e = wait.until(
                    EC.presence_of_element_located((By.XPATH, xpath)))
            move_to_element(driver, e)
            return e
        except TimeoutException:
            logging.error("Error: Could not find {}".format(xpath))
            driver.save_screenshot(
                join(
                    cfg_output_files_path,
                    "debug_" +
                    now() +
                    ".png"))
            a_nice_refresh(driver)
            raise TimeoutException
        except StaleElementReferenceException:
            driver.save_screenshot(
                join(
                    cfg_output_files_path,
                    "debug_" +
                    now() +
                    ".png"))
            a_nice_refresh(driver)
            raise StaleElementReferenceException
        driver.save_screenshot(
            join(
                cfg_output_files_path,
                "error_driver_" +
                now() +
                ".png"))
    return _wait_for_xpath_presence(driver, xpath, be_clickable)

def move_to_element(driver, e, click=False):
    from selenium.webdriver.common.action_chains import ActionChains
    actions = ActionChains(driver)
    if click:
        actions.move_to_element(e).click().perform()
    else:
        actions.move_to_element(e).perform()


def get_body_text(driver,
        exponential_multiplier=cfg_wait_exponential_multiplier,
        exponential_max=cfg_wait_exponential_max,
        stop_max_attempt=cfg_retry_stop_max_attempt):
    @retry(
        wait_exponential_multiplier=exponential_multiplier,
        wait_exponential_max=exponential_max,
        stop_max_attempt_number=stop_max_attempt)
    def _get_body_text(driver):
        try:
            e = wait_for_xpath_presence(driver, "//body")
        except StaleElementReferenceException:
            a_nice_refresh(driver)
            e = wait_for_xpath_presence(driver, "//*")
            raise StaleElementReferenceException
        return e.get_attribute("outerHTML")
    return _get_body_text(driver)


# Subbornly clicks on the elements which run away from the DOM
def click_stubborn(driver, e, xpath):
    logging.debug("Starting stubborn clicks")
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
    logging.info("""
    ******************
        PASSED
    ******************
    """)


def print_failed():
    logging.error("""
    !!!!!!!!!!!!!!!!!!
        FAILED
    !!!!!!!!!!!!!!!!!!
    """)


def now():
    return str(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
