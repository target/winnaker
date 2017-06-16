install-locally:
	pip install -e .

build-docker-nocache:
	docker build --no-cache -t winnaker .

build-docker:
	docker build -t winnaker .

clean-output:
	rm winnaker-screenshots/*.png || true

run-docker:
	docker run --env-file .env -it -v $(CURDIR)/winnaker-screenshots:/winnaker-screenshots/ winnaker


.PHONY: build
