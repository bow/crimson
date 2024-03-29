# Makefile for common development tasks.
#
# Copyright (c) 2015-2022 Wibowo Arindrarto <contact@arindrarto.dev>
# SPDX-License-Identifier: BSD-3-Clause
#
# This file is part of crimson <https://github.com/bow/crimson>.

# Cross-platform adjustments.
SYS := $(shell uname 2> /dev/null)
ifeq ($(SYS),Linux)
GREP_EXE := grep
DATE_EXE := date
else ifeq ($(SYS),Darwin)
GREP_EXE := ggrep
DATE_EXE := gdate
else
$(error Unsupported development platform)
endif

# Application name.
APP_NAME := crimson

# Supported Python versions; latest listed first.
PYTHON_VERSIONS := 3.12.0 3.11.6 3.10.13 3.9.18 3.8.18

# Primary Python version used for virtualenv.
PYTHON_VERSION := $(firstword $(PYTHON_VERSIONS))

# Virtualenv name.
VENV_NAME := $(APP_NAME)-dev

# Non-pyproject.toml dependencies.
PIP_DEPS := poetry==1.7.1 poetry-dynamic-versioning==1.2.0

# Non-pyproject.toml dev dependencies.
PIP_DEV_DEPS := pre-commit tox==4.4.12

# Various build info.
GIT_TAG    := $(shell git describe --tags --always --dirty 2> /dev/null || echo "untagged")
GIT_COMMIT := $(shell git rev-parse --quiet --verify HEAD || echo "?")
GIT_DIRTY  := $(shell test -n "$(shell git status --porcelain)" && echo "-dirty" || true)
BUILD_TIME := $(shell $(DATE_EXE) -u '+%Y-%m-%dT%H:%M:%SZ')
IS_RELEASE := $(shell ((echo "${GIT_TAG}" | $(GREP_EXE) -qE "^v?[0-9]+\.[0-9]+\.[0-9]+$$") && echo '1') || true)

IMG_NAME   := ghcr.io/bow/$(APP_NAME)
ifeq ($(IS_RELEASE),1)
IMG_TAG    := $(GIT_TAG)
else
IMG_TAG    := latest
endif

WHEEL_DEPS_DIR ?= $(CURDIR)/wheels/deps

## Rules ##

all: help


.PHONY: build
build: build-deps  ## Build wheel and source dist.
	poetry build

.PHONY: build-deps
build-deps: | $(WHEEL_DEPS_DIR)  ## Build wheels of dependencies.
	poetry export --without dev --without-hashes -f requirements.txt -o /dev/stdout | \
		pip wheel -r /dev/stdin --wheel-dir=$(WHEEL_DEPS_DIR)

$(WHEEL_DEPS_DIR):
	mkdir -p $@


.PHONY: clean
clean:  ## Remove build and test artifacts, including built Docker images.
	rm -rf build/ dist/ wheels/ \
			.coverage .coverage.xml .junit.xml .tox/ .cache/ .mypy_cache/ .pytest_cache/ \
		&& (docker rmi $(IMG_NAME) 2> /dev/null || true)


.PHONY: clean-pyenv
clean-pyenv:  ## Remove the created pyenv virtualenv.
	pyenv virtualenv-delete -f $(VENV_NAME) && rm -f .python-version


.PHONY: dev
dev:  ## Configure a local development setup.
	@if command -v pyenv virtualenv > /dev/null 2>&1; then \
		printf "Configuring a local dev environment using pyenv ...\n" >&2 \
			&& echo $(PYTHON_VERSIONS) | tr ' ' '\n' | xargs -P 4 -I '{}' pyenv install -s '{}' \
			&& printf "%s\n" "Setting up virtualenv '$(VENV_NAME)' in Python $(PYTHON_VERSION)..." 1>&2 \
			&& pyenv virtualenv -f "$(PYTHON_VERSION)" "$(VENV_NAME)" \
			&& printf "%s\n" "$(VENV_NAME)" > .python-version \
			&& for py_version in $(PYTHON_VERSIONS); do \
				echo "$${py_version}" >> .python-version; \
			done \
			&& source "$(shell pyenv root)/versions/$(VENV_NAME)/bin/activate" \
			&& pip install --upgrade pip && pyenv rehash \
			&& pip install $(PIP_DEPS) $(PIP_DEV_DEPS) && pyenv rehash \
			&& poetry config virtualenvs.create false \
			&& poetry install && pyenv rehash \
			&& pre-commit install && pyenv rehash \
			&& printf "Done.\n" 1>&2; \
	else \
		printf "Error: pyenv not found.\n" 1>&2 && exit 1; \
	fi


.PHONY: fmt
fmt:  ## Apply Black.
	poetry run black -t py312 .


.PHONY: help
help:  ## Show this help.
	$(eval PADLEN=$(shell $(GREP_EXE) -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) \
		| cut -d':' -f1 \
		| awk '{cur = length($$0); lengths[cur] = lengths[cur] $$0 ORS; max=(cur > max ? cur : max)} END {printf "%s", max}' \
		|| (true && echo 0)))
	@($(GREP_EXE) --version > /dev/null 2>&1 || (>&2 "error: GNU grep not installed"; exit 1)) \
		&& printf "\033[36m◉ %s dev console\033[0m\n" "$(APP_NAME)" >&2 \
		&& $(GREP_EXE) -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) \
			| awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m» \033[33m%*-s\033[0m \033[36m· \033[0m%s\n", $(PADLEN), $$1, $$2}' \
			| sort


.PHONY: img
img:  ## Build and tag the Docker container.
	docker build --build-arg REVISION=$(GIT_COMMIT)$(GIT_DIRTY) --build-arg BUILD_TIME=$(BUILD_TIME) --tag $(IMG_NAME):$(IMG_TAG) .


.PHONY: install-build
install-build:  ## Install dependencies required only for building.
	pip install $(PIP_DEPS)


.PHONY: lint
lint:  lint-types lint-style lint-metrics  ## Run the linter suite.


.PHONY: lint-types
lint-types:  ## Lint the type hints.
	poetry run mypy crimson tests


.PHONY: lint-style
lint-style:  ## Lint style conventions.
	poetry run flake8 --statistics crimson tests && poetry run black -t py312 --check .


.PHONY: lint-metrics
lint-metrics:  ## Lint other metrics.
	poetry run radon cc --total-average --show-closures --show-complexity --min C crimson


.PHONY: scan-sec
scan-sec: scan-sec-ast scan-sec-deps  ## Perform all security analyses.


.PHONY: scan-sec-ast
scan-sec-ast:  ## Perform static security analysis on the AST.
	poetry run bandit -r crimson


.PHONY: scan-sec-deps
scan-sec-deps:  ## Scan dependencies for reported vulnerabilities.
	poetry export --without-hashes -f requirements.txt -o /dev/stdout | poetry run safety check --full-report --stdin


.PHONY: test
test:  ## Run the test suite.
	poetry run py.test --junitxml=.junit.xml --cov=crimson --cov-report=term-missing --cov-report=xml:.coverage.xml crimson tests


.PHONY: tox
tox:  ## Run the test suite and all linters under all supported Python versions.
	tox --parallel auto
