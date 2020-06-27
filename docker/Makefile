help:
	@cat Makefile

DATA?="${HOME}/Data"
DOCKER_FILE=Dockerfile
DOCKER=docker-compose
TEST=tests/
HOST_PORT=8888
SRC?=$(shell dirname `pwd`)
EXAMPLES_DIR=$(SRC)/examples
PROGRAM_DIR=$(SRC)/program
FONT_DIR=$(SRC)/font/IPAfont00303
URL=""

build:
	$(DOCKER) build pyguitar

bash: build
	$(DOCKER) run -v $(SRC):/src/workspace -v $(DATA):/data -v $(FONT_DIR):/font -v $(PROGRAM_DIR):/program pyguitar bash

ipython: build
	$(DOCKER) run -v $(SRC):/src/workspace -v $(DATA):/data -v $(FONT_DIR):/font -v $(PROGRAM_DIR):/program pyguitar ipython

notebook: build
	$(DOCKER) run -p $(HOST_PORT):8888 -v $(SRC):/src/workspace -v $(DATA):/data -v $(FONT_DIR):/font pyguitar

examples: build
	$(DOCKER) run -p $(HOST_PORT):8888 -v $(SRC):/src/workspace -v $(EXAMPLES_DIR):/data/pyguitar_examples -v $(FONT_DIR):/font pyguitar

rebuild:
	$(DOCKER) build --no-cache pyguitar

ufret:
	$(DOCKER) run -v $(DATA):/data -v $(FONT_DIR):/font -v $(PROGRAM_DIR):/src/program  pyguitar python3 /src/program/ufret.py --url ${URL} --format json