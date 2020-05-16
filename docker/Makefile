help:
	@cat Makefile

DATA?="${HOME}/Data"
DOCKER_FILE=Dockerfile
DOCKER=docker-compose
TEST=tests/
HOST_PORT=8888
SRC?=$(shell dirname `pwd`)
EXAMPLES_PATH=$(SRC)/examples

build:
	$(DOCKER) build pyguitar

bash: build
	$(DOCKER) run -v $(SRC):/src/workspace -v $(DATA):/data pyguitar bash

ipython: build
	$(DOCKER) run -v $(SRC):/src/workspace -v $(DATA):/data pyguitar ipython

notebook: build
	$(DOCKER) run -v $(SRC):/src/workspace -v $(DATA):/data pyguitar

examples: build
	$(DOCKER) run -p $(HOST_PORT):8888 -v $(SRC):/src/workspace -v $(EXAMPLES_PATH):/data/pyguitar_examples pyguitar

rebuild:
	$(DOCKER) build --no-cache pyguitar
