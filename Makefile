# Common development tasks.

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
PYTHON_VERSIONS := 3.10.4 3.9.12 3.8.13 3.7.13

# Primary Python version used for virtualenv.
PYTHON_VERSION := $(firstword $(PYTHON_VERSIONS))

# Virtualenv name.
VENV_NAME := $(APP_NAME)-dev

# Dependencies installed via pip.
PIP_DEPS := poetry poetry-dynamic-versioning pre-commit tox

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
build:  ## Build wheel and source dist.
	poetry build
	twine check dist/*

.PHONY: build-deps
build-deps: | $(WHEEL_DEPS_DIR)  ## Build wheels of dependencies.
	poetry export --without-hashes -f requirements.txt -o /dev/stdout | \
		pip wheel -r /dev/stdin --wheel-dir=$(WHEEL_DEPS_DIR)

$(WHEEL_DEPS_DIR):
	mkdir -p $@


.PHONY: clean
clean:  ## Remove build artifacts, including built Docker images.
	rm -rf build/ dist/ && (docker rmi $(IMG_NAME) 2> /dev/null || true)


.PHONY: clean-venv
clean-venv:  ## Remove the created pyenv virtualenv.
	pyenv virtualenv-delete -f $(VENV_NAME) && rm -f .python-version


.PHONY: fmt
fmt:  ## Apply Black.
	poetry run black -t py310 .


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


.PHONY: install-dev
install-dev:  ## Configure a local development setup.
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
			&& pip install $(PIP_DEPS) && pyenv rehash \
			&& poetry config experimental.new-installer false \
			&& poetry config virtualenvs.create false \
			&& poetry install && pyenv rehash \
			&& pre-commit install && pyenv rehash \
			&& printf "Done.\n" 1>&2; \
	else \
		printf "Error: pyenv not found.\n" 1>&2 && exit 1; \
	fi


.PHONY: lint
lint:  lint-types lint-style lint-metrics  ## Run the linter suite.


.PHONY: lint-types
lint-types:  ## Lint the type hints.
	poetry run mypy crimson tests


.PHONY: lint-style
lint-style:  ## Lint style conventions.
	poetry run flake8 --statistics crimson tests && poetry run black -t py310 --check .


.PHONY: lint-metrics
lint-metrics:  ## Lint other metrics.
	poetry run radon cc --total-average --show-closures --show-complexity --min C crimson


.PHONY: scan-security
scan-security: scan-security-ast scan-security-deps  ## Perform all security analyses.


.PHONY: scan-security-ast
scan-security-ast:  ## Perform static security analysis on the AST.
	poetry run bandit -r crimson


.PHONY: scan-security-deps
scan-security-deps:  ## Scan dependencies for reported vulnerabilities.
	poetry export --without-hashes -f requirements.txt -o /dev/stdout | poetry run safety check --full-report --stdin


.PHONY: test
test:  ## Run the test suite.
	poetry run py.test --junitxml=.junit.xml --cov=crimson --cov-config=.coveragerc --cov-report=term-missing --cov-report=xml:.coverage.xml crimson tests


.PHONY: tox
tox:  ## Run the test suite and all linters under all supported Python versions.
	tox --parallel auto
