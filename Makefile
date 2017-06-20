developer-setup:
	pip install autopep8
	ln -s $(CURDIR)/hooks/pre-commit .git/hooks/pre-commit

install-locally:
	pip install -e .

build-docker-nocache:
	docker build --no-cache -t local/winnaker:latest .

build-docker:
	docker build -t local/winnaker:latest .

format-code:
	autopep8 --in-place --aggressive --aggressive winnaker/*.py

clean-output:
	rm winnaker-screenshots/*.png || true

clean:
	rm *.pyc
	rm winnaker/*.pyc

clean-kube:
	kubectl config use-context minikube
	kubectl delete cronjobs --all
	kubectl delete jobs --all
	kubectl delete pods --all

run-docker:
	docker run --env-file .env -it -v $(CURDIR)/winnaker-screenshots:/winnaker-screenshots/ local/winnaker


.PHONY: build
