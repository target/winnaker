developer-setup:
	ln -s $(CURDIR)/hooks/pre-commit .git/hooks/pre-commit 

install-locally:
	pip install -e .

build-docker-nocache:
	docker build --no-cache -t winnaker .

build-docker:
	docker build -t winnaker .

format-code:
	autopep8 --in-place --aggressive --aggressive winnaker/*

clean-output:
	rm winnaker-screenshots/*.png || true

clean:
	rm *.pyc
	rm winnaker/*.pyc


run-docker:
	docker run --env-file .env -it -v $(CURDIR)/winnaker-screenshots:/winnaker-screenshots/ winnaker


.PHONY: build
