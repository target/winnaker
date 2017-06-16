FROM medyagh/selenium-alpine-python-xvfb:v0.1.0

COPY ./ /winnaker/

RUN pip install /winnaker/

ENTRYPOINT ["winnaker", "-hl"]
