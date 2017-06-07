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
