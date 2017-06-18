## Required
export WINNAKER_USERNAME="REPLACE_DEFAULT"
export WINNAKER_PASSWORD="REPLACE_DEFAULT"
export WINNAKER_SPINNAKER_URL="REPLACE_DEFAULT"
export WINNAKER_APP_NAME="REPLACE_DEFAULT"
export WINNAKER_PIPELINE_NAME="REPLACE_DEFAULT"
export WINNAKER_OUTPUTPATH="./winnaker-screenshots"

## Not Required
export WINNAKER_MAX_WAIT_PIPELINE="100"
export WINNAKER_HIPCHAT_POSTURL="REPLACE_DEFAULT"
export WINNAKER_NUMBER_OF_STAGES_TO_CHECK="2"

# Internal Config
# only change if you know what you are doing

### XPATH Configurations, Future Proofing it, In case deck changes.
### if you find ever change this values, please make an issue in
### https://github.com/target/winnaker/issues/new

export WINNAKER_XPATH_LOGIN_USERNAME="//input[@id='username'][@name='pf.username']"
export WINNAKER_XPATH_LOGIN_PASSWORD="//input[@id='password'][@name='pf.pass']"
export WINNAKER_XPATH_LOGIN_SUBMIT="//input[@type='submit']"
export WINNAKER_XPATH_APPLICATIONS_TAB="//a[@href='#/applications' and contains(.,'Applications')]"
export WINNAKER_XPATH_SEARCH_APPLICATIONS="//input[@placeholder='Search applications']"
export WINNAKER_XPATH_START_MANUAL_EXECUTION="//div[contains(@class, 'execution-group-actions')]/h4[2]/a/span"
# TODO Try this later
# //label[contains(.,'Force')]
export WINNAKER_XPATH_FORCE_REBAKE="//input[@type='checkbox' and @ng-model='vm.command.trigger.rebake']"
export WINNAKER_XPATH_PIPELINE_EXECUTION_SUMMARY="//execution-groups[1]//div[@class='execution-summary']"
export WINNAKER_XPATH_PIPLELINE_TRIGGER_DETAILS="//execution-groups[1]//ul[@class='trigger-details']"
export WINNAKER_XPATH_PIPLELINE_DETAILS_LINK="//execution-groups[1]//execution-status//div/a[contains(., 'Details')]"




echo "-------------------------------------------------------"
echo " The config file location:  winnaker/config.sh     "
echo "-------------------------------------------------------"

for config_parameter in WINNAKER_USERNAME WINNAKER_PASSWORD WINNAKER_SPINNAKER_URL WINNAKER_APP_NAME WINNAKER_PIPELINE_NAME WINNAKER_HIPCHAT_POSTURL WINNAKER_MAX_WAIT_PIPELINE WINNAKER_WINNAKER_OUTPUTPATH
do
    if [[  ${!config_parameter} = "REPLACE_DEFAULT" ]]; then
        if [[  $config_parameter = "WINNAKER_PASSWORD" ]]; then
          read -sp "$config_parameter: " "$config_parameter"
          echo ""
        else
          read -p "$config_parameter: " "$config_parameter"
        fi
    else
         echo "$config_parameter set ✓"
     fi
done
