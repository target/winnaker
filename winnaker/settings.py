import os
from dotenv import load_dotenv
from os.path import join, dirname
from dotenv import load_dotenv


def get_env(env_key, default):
    value = os.getenv(env_key)
    if value is None or len(value) == 0:
        print(
            "INFO: {} not set in environment, defaulting to {}".format(
                env_key, default))
        return default
    print("INFO: {} set from environment".format(env_key))
    return value


dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

cfg_app_name = os.environ.get("WINNAKER_APP_NAME")
cfg_number_of_stages_to_check = int(
    os.environ["WINNAKER_NUMBER_OF_STAGES_TO_CHECK"])
cfg_output_files_path = os.environ["WINNAKER_OUTPUTPATH"]
cfg_spinnaker_url = os.environ["WINNAKER_SPINNAKER_URL"]
cfg_spinnaker_username = os.environ["WINNAKER_USERNAME"]
cfg_spinnaker_password = os.environ['WINNAKER_PASSWORD']
cfg_max_wait_for_pipeline_run_mins = int(int(
    get_env("WINNAKER_MAX_WAIT_PIPELINE", 100)) * 60.00)

# Notification Settings
cfg_email_smtp = get_env("WINNAKER_EMAIL_SMTP", None)
cfg_email_from = get_env("WINNAKER_EMAIL_FROM", None)
cfg_email_to = get_env("WINNAKER_EMAIL_TO", None)
cfg_hipchat_posturl = get_env('WINNAKER_HIPCHAT_POSTURL', None)

# Retry settings
cfg_wait_exponential_multiplier = get_env(
    "WINNAKER_WAIT_EXPONENTIAL_MULTIPLIER",
    10)
cfg_wait_exponential_max= get_env(
    "WINNAKER_WAIT_EXPONENTIAL_MAX",
    5000)
cfg_retry_stop_max_attempt = get_env(
    "WINNAKER_RETRY_STOP_MAX_ATTEMPT",
    10)

# ---------------------------------------------
# Internal Configs
#
# ---------------------------------------------

cfg_usernamebox_xpath = get_env(
    "WINNAKER_XPATH_LOGIN_USERNAME",
    "//input[@id='username'][@name='pf.username']")
cfg_passwordbox_xpath = get_env(
    "WINNAKER_XPATH_LOGIN_PASSWORD",
    "//input[@id='password'][@name='pf.pass']")
cfg_signin_button_xpath = get_env(
    "WINNAKER_XPATH_LOGIN_SUBMIT",
    "//input[@type='submit']")
cfg_execution_summary_xp = get_env(
    "WINNAKER_XPATH_PIPELINE_EXECUTION_SUMMARY",
    "//execution-groups[1]//div[@class='execution-summary']")
cfg_trigger_details_xp = get_env(
    "WINNAKER_XPATH_PIPLELINE_TRIGGER_DETAILS",
    "//execution-groups[1]//ul[@class='trigger-details']")
cfg_detail_xpath = get_env(
    "WINNAKER_XPATH_PIPLELINE_DETAILS_LINK",
    "//execution-groups[1]//execution-status//div/a[contains(., 'Details')]")
cfg_applications_xpath = get_env(
    "WINNAKER_XPATH_APPLICATIONS_TAB",
    "//a[@href='#/applications' and contains(.,'Applications')]")
cfg_searchbox_xpath = get_env(
    "WINNAKER_XPATH_SEARCH_APPLICATIONS",
    "//input[@placeholder='Search applications']")
cfg_start_manual_execution_xpath = get_env(
    "WINNAKER_XPATH_START_MANUAL_EXECUTION",
    "//div[contains(@class, 'execution-group-actions')]/h4[2]/a/span")
cfg_force_rebake_xpath = get_env(
    "WINNAKER_XPATH_FORCE_REBAKE",
    "//input[@type='checkbox' and @ng-model='vm.command.trigger.rebake']")

cfg_oauth_authorize_xpath= get_env(
    "WINNAKER_XPATH_OAUTH_AUTHORIZE",
    "//*[@id='js-oauth-authorize-btn']")
