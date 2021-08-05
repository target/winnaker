## Winnaker
[![](https://images.microbadger.com/badges/image/medyagh/winnaker.svg)](https://microbadger.com/images/medyagh/winnaker "Get your own image badge on microbadger.com")


```
____    __    ____  __  .__   __. .__   __.      ___       __  ___  _______ .______
\   \  /  \  /   / |  | |  \ |  | |  \ |  |     /   \     |  |/  / |   ____||   _  \
 \   \/    \/   /  |  | |   \|  | |   \|  |    /  ^  \    |  '  /  |  |__   |  |_)  |
  \            /   |  | |  . `  | |  . `  |   /  /_\  \   |    <   |   __|  |      /
   \    /\    /    |  | |  |\   | |  |\   |  /  _____  \  |  .  \  |  |____ |  |\  \----.
    \__/  \__/     |__| |__| \__| |__| \__| /__/     \__\ |__|\__\ |_______|| _| `._____|


```

## Archive notice

In August of 2021, this project was archived. 

## What is Winnaker?
Winnaker is an auditing tool for Spinnaker. Real testing in a real browser!

## What do you need on your work station?
1. python 2.7
2. a copy of [ChromeDriver](https://sites.google.com/a/chromium.org/chromedriver/home) in your PATH

## What do you need in your system under test?
1. a spinnaker url
2. a sample app
3. a sample pipeline

## Run headlessly in Docker
1. Build Docker:


	```
	docker build -t winnaker .
	```



2. Config : copy the sample env file and edit it.


	```
	cp winnaker/.env-sample .env

	```

3. Run :
	```
	docker run --env-file .env -it -v $(pwd)/winnaker-screenshots:/winnaker-screenshots/ winnaker
	```

4. Add [options](#options) as needed.


## Run GUI mode

1. run
```
./run.sh
```
1. Add [options](#options) as needed.



## What does the default run do?
- Logs in to `spinnaker` through chromium browser
- Searches for `sampleapp` app
- Searches for `samplepipeline` the pipeline
- Gets the last build status
- Generates screenshot :
	- `./applications.png`
	- `./pipelines.png`
	- `./last_build_status.png`
	- `./login.png`
	- `./stage1.png`
- Any error will result in a non-zero code to the system.
- Error screenshots will be timestamped.


## Screenshots

- screenshot folder by default is winnaker-screenshots


## Options
The config file is located at ./src/config.sh but you can simply add any of the options below to your run.sh command.

```
optional arguments:
  -h, --help            show this help message and exit
  -s, --start           starts manual execution of the pipeline
  -fb, --forcebake      force bake, to be used wth --start
  -a APP, --app APP     the name of application to look for
  -p PIPELINE, --pipeline PIPELINE
                        the name of pipeline to test
  -nl, --nologin        will not attempt to login
  -hl, --headless       will run in an xvfb display
```


## Examples:
##### Example 1: Gets the last build status of the default pipeline
`./run.sh`


##### Example 2: Starts default pipeline execution

`./run.sh -s`

##### Example 3: Start the pipeline with force rebake

`./run.sh -s -fb`

##### Example 4: Start build execution on different pipeline than config file

`./run.sh -s -p "deploy to npe"`

##### Example 5: override default app specified in the config file

use with --caution--, will override the sample app.

`./run.sh -a "differentapp" -p "different pipeline"`


## How tos



#### How to setup a Winnaker Hipchat bot
- create a hipchat bot
- grab the post url
it should look like
`https://INSERT_HIPCHAT_BASE_URL.com/v2/room/INSERT_ROOM_ID/notification?auth_token=INSERT_TOKEN`


#### How to import the Winnaker python package
- `pip install git+git://github.com/target/winnaker`
- Then in your python script you can import the Winnaker modules. For example you can import the `models` module via `from winnaker import models`

#### How to deploy to minikube
- Start minikube

	```
	minikube start
	```

- Activate minikube docker in your bash

	```
	eval $(minikube docker-env)
	```
- build docker

	```
	make build-docker-nocache
	```
- Fill out secret and configmaps and change default 5 minute cronjob to your needs. (edit configmap and secret inside kube folder)

- apply kube files

	```
	kubectl apply -f kube
	```
