# Define the shell to use for running commands
SHELL := /bin/bash

# Define the path to the virtual environment
VENV := /tmp/.venv
REQS := requirements.txt
PYLINT_RC := .pylintrc
PYCODECOVERAGE_RC := .coveragerc

# Define colors
BLACK := $$(tput setaf 0)
RED := $$(tput setaf 1)
GREEN := $$(tput setaf 2)
YELLOW := $$(tput setaf 3)
BLUE := $$(tput setaf 4)
MAGENTA := $$(tput setaf 5)
CYAN := $$(tput setaf 6)
GRAY := $$(tput setaf 7)
RESET := $$(tput sgr0)

# This declaration tells make that list is not a file but a 
# label for a set of commands to execute.
.PHONY: list

.DEFAULT_GOAL := list

list:
	@echo "$(BLUE)Available targets:$(RESET)"
	@awk '/^[a-zA-Z_-]+:/ {print $$1}' $(MAKEFILE_LIST) | sed 's/://' | grep -vE '^\.PHONY|list' | sort

init:
	@( \
		echo "$(GREEN)Creating virtual environment...$(RESET)" ; \
		python3 -m venv $(VENV) ; \
		echo "$(GREEN)Activating virtual environment...$(RESET)" ; \
		source $(VENV)/bin/activate && \
		python3 -m pip install -r $(REQS) ; \
		echo "$(GREEN)Environment setup complete.$(RESET)" ; \
	)

test:
	# Check if the virtual environment exists, run 'lint' if it does not
	@if [ ! -d "$(VENV)" ]; then \
		echo "$(YELLOW)Virtual environment not found. Running 'init' target...$(RESET)"; \
		make init; \
	fi
	# Run commands in a subshell instance
	@( \
		# Activate the virtual environment ; \
		source $(VENV)/bin/activate ; \
		# Run pylint ; \
		echo "$(GREEN)Running linting with pylint $(RESET)" ; \
		find . -name "*.py" ! -path "./venv/*" -exec pylint --rcfile $(PYLINT_RC) --verbose {} + ; \
		# Run prospector ; \
		echo "$(GREEN)Running static analysis with prospector $(RESET)" ; \
		prospector --strictness low ; \
		# Run bandit ; \
		echo "$(GREEN)Running security tests with bandit $(RESET)" ; \
		bandit -r . -ll -x ./venv ; \
		# Run unittest ; \
		echo "$(GREEN)Running unit tests $(RESET)" ; \
		python3 -m unittest discover -s tests ; \
		# Run coverage ; \
		coverage run --rcfile $(PYCODECOVERAGE_RC) -m unittest discover -s tests ; \
		coverage report --rcfile $(PYCODECOVERAGE_RC) ; \
	)

build:
	@echo "$(GREEN)Building with docker...$(RESET)"
	docker-compose build

up:
	@echo "$(GREEN)Starting containers with docker...$(RESET)"
	docker-compose up --build -d

logs:
	@echo "$(YELLOW)Tailing logs with docker...$(RESET)"
	docker-compose logs -f

teardown:
	@echo "$(RED)Deleting containers...$(RESET)"
	docker-compose down

requests-create:
	@echo "$(GREEN)Making HTTP POST Requests...$(RESET)"
	bash _scripts/http/create.sh

requests-retrieve:
	@echo "$(GREEN)Making HTTP GET Requests...$(RESET)"
	bash _scripts/http/get.sh

clean:
	@echo "$(RED)Deleting pycache directories$(RESET)"
	find . -type d -name '__pycache__' -exec rm -rf {} +
