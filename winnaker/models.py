# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import os
from winnaker.helpers import *
from datetime import datetime
import sys
from tqdm import tqdm

ERROR_LIST = {"Whitelabel Error Page": "Check clouddriver",
              "No hosted service provider is configured": "Check Gate",
              "no alias was selected": "TBD",
              "This application has no explicit mapping for": "TBD",
              "so you are seeing this as a fallback.": "Check Gate",
              "Error Code: Throttling": "Check Edda/Cloud Provider",
              "Rate exceeded": "Check Edda",
              "This application has no explicit mapping for /error": "Check Deck"
              }


class Spinnaker():

    def __init__(self):
        chrome_options = Options()
        chrome_options.add_argument("--disable-extensions")
        chrome_options.add_argument("--no-sandbox")
        self.driver = webdriver.Chrome(chrome_options=chrome_options)
        # self.driver = webdriver.Firefox()
        time.sleep(1)
        self.driver.get(os.environ["WINNAKER_SPINNAKER_URL"])
        self.wait = WebDriverWait(self.driver, 10)
        if not os.path.exists(os.environ["WINNAKER_OUTPUTPATH"]):
            os.makedirs(os.environ["WINNAKER_OUTPUTPATH"])

    def login(self):
        self.check_page_contains_error()
        usernamebox = "//input[@id='username'][@name='pf.username']"
        passwordbox = "//input[@id='password'][@name='pf.pass']"
        signinbutton = "//input[@type='submit']"
        e = wait_for_xpath_presence(self.driver, usernamebox)
        e.send_keys(os.environ['WINNAKER_USERNAME'])
        e = wait_for_xpath_presence(self.driver, passwordbox)
        self.driver.save_screenshot(os.environ["WINNAKER_OUTPUTPATH"]+"/login.png")
        e.send_keys(os.environ['WINNAKER_PASSWORD'])
        e = wait_for_xpath_presence(self.driver, signinbutton)
        e.click()
        print("- Logged in to the spinnaker")

    def get_application(self, appname):
        self.check_page_contains_error()
        applications_xpath = "//a[@href='#/applications' and contains(.,'Applications')]"
        e = wait_for_xpath_presence(
            self.driver, applications_xpath, be_clickable=True)
        e.click()
        searchbox = "//input[@placeholder='Search applications']"
        e = wait_for_xpath_presence(self.driver, searchbox)
        e.send_keys(appname)
        e.send_keys(Keys.RETURN)
        time.sleep(1)
        self.driver.save_screenshot(os.environ["WINNAKER_OUTPUTPATH"]+"/applications.png")
        app_xpath = "//a[contains (.,'" + appname + "')]"
        e = wait_for_xpath_presence(self.driver, app_xpath)
        e.click()
        time.sleep(1)
        print("- Searched for application " + appname)

    def get_pipelines(self, appname):
        self.get_application(appname)
        pipelines_xpath = "//a[@href='#/applications/" + \
            appname + "/executions']"
        e = wait_for_xpath_presence(self.driver, pipelines_xpath)
        e.click()

    def get_pipeline(self, appname, pipelinename):
        self.check_page_contains_error()
        self.get_pipelines(appname)
        time.sleep(0.5)
        checkbox = "//div[@class='nav']//execution-filters//label[contains(.,'  %s')]/input[@type='checkbox']" % pipelinename
        e = wait_for_xpath_presence(
            self.driver, checkbox, be_clickable=True)
        move_to_element(self.driver, e, click=True)
        time.sleep(2)
        if not e.get_attribute('checked'):
            e = wait_for_xpath_presence(
                self.driver, checkbox, be_clickable=True)
            e.click()
        time.sleep(2)
        self.driver.save_screenshot(os.environ["WINNAKER_OUTPUTPATH"]+"/pipelines.png")
        print("- Selected pipeline " + pipelinename + " successfully")

    def start_manual_execution(self, force_bake=False):
        self.check_page_contains_error()
        # starts the 1st pipeline which is currently on the page
        start_xpath = "//div[contains(@class, 'execution-group-actions')]/h4[2]/a/span"
        e = wait_for_xpath_presence(self.driver, start_xpath)
        click_stubborn(self.driver, e, start_xpath)
        time.sleep(3)
        if force_bake:
            fbake_xpath = "//input[@type='checkbox' and @ng-model='vm.command.trigger.rebake']"
            e = wait_for_xpath_presence(
                self.driver, start_xpath, be_clickable=True)
            move_to_element(self.driver, e, click=True)
            time.sleep(2)
            if not e.get_attribute('checked'):
                xpath = "//input[@type='checkbox' and @ng-model='vm.command.trigger.rebake']"
                e = wait_for_xpath_presence(
                    self.driver, xpath, be_clickable=True)
                print("Checking force bake option")
                e.click()
            self.driver.save_screenshot(os.environ["WINNAKER_OUTPUTPATH"]+"/force_bake_check.png")

        run_xpath = "//button[@type='submit' and contains(.,'Run')]/span[1]"
        e = wait_for_xpath_presence(self.driver, run_xpath, be_clickable=True)
        e.click()
        time.sleep(2)
        MAX_WAIT_FOR_RUN = int(
            os.environ["WINNAKER_MAX_WAIT_PIPELINE"]) * 60.00
        start_time = time.time()
        print("- Starting Manual Execution")
        time.sleep(10)  # To give enough time for pipeleine kick off show up
        print("\t Running ... (will wait up to " +
              str(int(MAX_WAIT_FOR_RUN / 60)) + ") minutes")
        for i in tqdm(range(int(MAX_WAIT_FOR_RUN / 10))):
            if time.time() - start_time > MAX_WAIT_FOR_RUN:
                print("The run is taking more than " +
                      str(MAX_WAIT_FOR_RUN / 60) + " minutes")
                print("Considering it as an error")
                sys.exit(1)
            status = self.get_last_build().status
            if "RUNNING" in status:
                time.sleep(10)
            elif "NOT_STARTED" in status:
                print("Pipeline has not yet started.")
                time.sleep(10)
            elif "SUCCEEDED" in status:
                print("\nCongratulations pipleline run was successful.")
                print_passed()
                self.get_stages(n=2)
                return 0
            elif "TERMINAL" in status:
                print("Pipleline stopped with terminal state. screenshot generated.")
                print_failed()
                sys.exit(1)
            else:
                print("Error: something went wrong " + status)
                sys.exit(2)

    def get_last_build(self):
        execution_summary_xp = "//execution[1]//div[@class='execution-summary']"
        execution_summary = wait_for_xpath_presence(
            self.driver, execution_summary_xp)

        trigger_details_xp = "//execution[1]//ul[@class='trigger-details']"
        trigger_details = wait_for_xpath_presence(
            self.driver, trigger_details_xp)
        self.build = Build(trigger_details.text, execution_summary.text)
        time.sleep(1)
        detail_xpath = "//execution[1]//execution-status//div/a[contains(., 'Details')]"
        e = wait_for_xpath_presence(self.driver, detail_xpath)
        self.driver.save_screenshot(os.environ["WINNAKER_OUTPUTPATH"]+"/last_build_status.png")
        return self.build

    def get_stages(self, n=2):
        # n number of stages to get
        for i in range(1, n + 1):
            stage_xpath = "//execution[1]//div[@class='stages']/div[" + str(
                i) + "]"
            e = wait_for_xpath_presence(
                self.driver, stage_xpath, be_clickable=True)
            move_to_element(self.driver, e)
            e.click()
            alert_box_xps = ["//div[@class='alert alert-danger']",
                             "//div[@class='well alert alert-info']",
                             "//div[@class='alert alert-info']"]
            for xpath in alert_box_xps:
                try:
                    e = self.wait.until(
                        EC.presence_of_element_located((By.XPATH, xpath)))
                    print("- Stage Detail: \n\t" +
                          e.text.replace("\n", "\n\t"))
                    for error in ERROR_LIST:
                        if error in e.text:
                            print("\t Stage Failed: " + e.text)
                            sys.exit(1)
                except TimeoutException:
                    continue
            self.driver.save_screenshot(os.environ["WINNAKER_OUTPUTPATH"]+"/stage_" + str(i) + ".png")

    def check_page_contains_error(self):
        for error in ERROR_LIST.keys():
            if error in get_body_text(self.driver):
                print("- Failed for : " + error)
                print("- Suggestion : " + ERROR_LIST[error])
                print_failed()
                sys.exit(1)
                return True
            assert error not in get_body_text(self.driver)


# Represents a build of a pipeline
class Build():

    def __init__(self, trigger_details, execution_summary):
        try:
            self.status = execution_summary.split(
                "\n")[0].replace("Status: ", "")
            self.duration = execution_summary.split(
                "\n")[1].replace("Duration: ", "")
            self.type_of_start = ""
            self.username = trigger_details.split("\n")[0]
            print(self.username)
            if " CDT" in trigger_details:
                self.datetime_started = datetime.strptime(trigger_details.split(
                    "\n")[1].replace(" CDT", ""), '%Y-%m-%d %H:%M:%S')
            # TO DO: convert ago to UTC time
            if " ago" in trigger_details:
                self.datetime_started = trigger_details.split("\n")[1]
            self.detail = trigger_details.split("\n")[2]
            self.stack = trigger_details.split("\n")[3]
        except (ValueError, IndexError):
            pass

    def status_is_valid(self):
        if self.status in ["RUNNING", "SUCCEEDED", "TERMINAL", "CANCELED"]:
            return True
        return False
