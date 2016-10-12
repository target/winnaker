mkdir -p ./src/outputs
rm ./src/outputs/*
source src/config.sh
docker run -it --rm -e WINNAKER_USERNAME -e WINNAKER_PASSWORD -e WINNAKER_USERNAME -e WINNAKER_APP_NAME -e WINNAKER_PIPELINE_NAME -e WINNAKER_SPINNAKER_URL -e WINNAKER_HIPCHAT_POSTURL -e WINNAKER_MAX_WAIT_PIPELINE -it -v $(pwd)/src/:/app/ winnaker "$@"
