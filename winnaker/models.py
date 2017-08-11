# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import os
import sys
import logging
from winnaker.helpers import *
from datetime import datetime
from tqdm import tqdm
from os.path import join
from winnaker.settings import *


ERROR_LIST = {
    "Whitelabel Error Page": "Check clouddriver",
    "No hosted service provider is configured": "Check Gate",
    "no alias was selected": "TBD",
    "This application has no explicit mapping for": "TBD",
    "so you are seeing this as a fallback.": "Check Gate",
    "Error Code: Throttling": "Check Edda/Cloud Provider",
    "Rate exceeded": "Check Edda",
    "This application has no explicit mapping for /error": "Check Deck"}


class Spinnaker():

    def __init__(self):
        chrome_options = Options()
        chrome_options.add_argument("--disable-extensions")
        chrome_options.add_argument("--no-sandbox")
        self.driver = webdriver.Chrome(chrome_options=chrome_options)
        # self.driver = webdriver.Firefox()
        time.sleep(1)
        self.driver.get(cfg_spinnaker_url)
        self.wait = WebDriverWait(self.driver, 10)
        if not os.path.exists(cfg_output_files_path):
            os.makedirs(cfg_output_files_path)

    def authorize(self):
        logging.debug("Authorizing OAuth Request")
        try:
            e = wait_for_xpath_presence(self.driver, cfg_oauth_authorize_xpath, stop_max_attempt=2)
            self.driver.save_screenshot(join(
                cfg_output_files_path, "authorize.png"))
            e.click()
        except:
            logging.debug("couldn't find authorize xpath. This is OK if the user has already been authorized, looked for: %s"
                % cfg_oauth_authorize_xpath)

    def login(self):
        self.check_page_contains_error()
        e = wait_for_xpath_presence(self.driver, cfg_usernamebox_xpath)
        logging.debug(
            "Logging in as: {}".format(
                cfg_spinnaker_username))
        e.send_keys(cfg_spinnaker_username)
        e = wait_for_xpath_presence(self.driver, cfg_passwordbox_xpath)
        self.driver.save_screenshot(join(
            cfg_output_files_path, "login.png"))
        e.send_keys(cfg_spinnaker_password)
        e = wait_for_xpath_presence(self.driver, cfg_signin_button_xpath)
        e.click()
        logging.info(
            "- Logged in to the spinnaker instance at {}".format(cfg_spinnaker_url))
        self.driver.save_screenshot(join(cfg_output_files_path, "login2.png"))
        time.sleep(3)

    def get_application(self, appname):
        self.check_page_contains_error()
        e = wait_for_xpath_presence(
            self.driver, cfg_applications_xpath, be_clickable=True)
        e.click()
        e = wait_for_xpath_presence(self.driver, cfg_searchbox_xpath)
        e.send_keys(appname)
        e.send_keys(Keys.RETURN)
        time.sleep(1)
        self.driver.save_screenshot(join(
            cfg_output_files_path,
            "applications.png"))
        app_xpath = "//a[contains (.,'" + appname + "')]"
        e = wait_for_xpath_presence(self.driver, app_xpath)
        e.click()
        time.sleep(1)
        logging.info("- Searched for application: {}".format(appname))

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
        self.driver.save_screenshot(
            join(cfg_output_files_path, "pipelines.png"))
        logging.info(
            "- Selected pipeline: {} successfully".format(pipelinename))

    def start_manual_execution(self, force_bake=False):
        self.check_page_contains_error()
        # starts the 1st pipeline which is currently on the page
        e = wait_for_xpath_presence(
            self.driver, cfg_start_manual_execution_xpath)
        click_stubborn(self.driver, e, cfg_start_manual_execution_xpath)
        time.sleep(2)
        if force_bake:
            e = wait_for_xpath_presence(
                self.driver, cfg_force_rebake_xpath, be_clickable=True)
            move_to_element(self.driver, e, click=True)
            time.sleep(2)
            if not e.get_attribute('checked'):
                e = wait_for_xpath_presence(
                    self.driver, cfg_froce_rebake_xpath, be_clickable=True)
                logging.info("Checking force bake option")
                e.click()
            self.driver.save_screenshot(
                join(cfg_output_files_path, "force_bake_check.png"))

        run_xpath = "//button[@type='submit' and contains(.,'Run')]/span[1]"
        e = wait_for_xpath_presence(self.driver, run_xpath, be_clickable=True)
        e.click()
        time.sleep(2)
        start_time = time.time()
        logging.info("- Starting Manual Execution")
        time.sleep(10)  # To give enough time for pipeleine kick off show up
        logging.info("\t Running ... (will wait up to {} minutes".format(
            int(cfg_max_wait_for_pipeline_run_mins / 60)))
        for i in tqdm(range(int(cfg_max_wait_for_pipeline_run_mins / 10))):
            if time.time() - start_time > cfg_max_wait_for_pipeline_run_mins:
                logging.error("The run is taking more than {} minutes".format(
                    int(cfg_max_wait_for_pipeline_run_mins / 60)))
                logging.error("Considering it as an error")
                sys.exit(1)
            status = self.get_last_build().status
            if "RUNNING" in status:
                time.sleep(10)
            elif "NOT_STARTED" in status:
                logging.info("Pipeline has not yet started.")
                time.sleep(10)
            elif "SUCCEEDED" in status:
                logging.info("Congratulations pipeline run was successful.")
                print_passed()
                self.get_stages(n=cfg_number_of_stages_to_check)
                return 0
            elif "TERMINAL" in status:
                logging.error(
                    "Pipeline stopped with terminal state. screenshot generated.")
                print_failed()
                sys.exit(1)
            else:
                logging.error("Error: something went wrong {}".format(status))
                sys.exit(2)

    def get_last_build(self):
        execution_summary = wait_for_xpath_presence(
            self.driver, cfg_execution_summary_xp)
        trigger_details = wait_for_xpath_presence(
            self.driver, cfg_trigger_details_xp)
        self.build = Build(trigger_details.text, execution_summary.text)
        time.sleep(1)
        e = wait_for_xpath_presence(self.driver, cfg_detail_xpath)
        self.driver.save_screenshot(join(
            cfg_output_files_path,
            "last_build_status.png"))
        return self.build

    # TODO Get all the stages automaticly
    def get_stages(
            self, n=cfg_number_of_stages_to_check):
        # n number of stages to get
        for i in range(1, n + 1):
            stage_xpath = "//execution-groups[1]//div[@class='stages']/div[" + str(
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
                    logging.info("- Stage Detail: \n\t" +
                                 e.text.replace("\n", "\n\t\n"))
                    for error in ERROR_LIST:
                        if error in e.text:
                            logging.error("\t Stage Failed: {}".format(e.text))
                            sys.exit(1)
                except TimeoutException:
                    continue
            self.driver.save_screenshot(
                join(
                    cfg_output_files_path,
                    "stage_" +
                    str(i) +
                    ".png"))

    def check_page_contains_error(self):
        for error in ERROR_LIST.keys():
            if error in get_body_text(self.driver):
                logging.error("- Failed for: {}".format(error))
                logging.info("- Suggestion: {}".format(ERROR_LIST[error]))
                print_failed()
                sys.exit(1)
                # TODO: Is this needed? It should never occur because of the
                # sys.exit(1)
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
            logging.debug("Username: {}".format(self.username))
            if " CDT" in trigger_details:
                self.datetime_started = datetime.strptime(
                    trigger_details.split("\n")[1].replace(
                        " CDT", ""), '%Y-%m-%d %H:%M:%S')
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
