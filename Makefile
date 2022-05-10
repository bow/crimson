# Application name.
APP_NAME := crimson

# Virtualenv name.
VENV_NAME := $(APP_NAME)-dev

# Supported Python versions; latest listed first.
PYTHON_VERSIONS := 3.10.4 3.9.12 3.8.13 3.7.13

# Primary Python version used for virtualenv.
PYTHON_VERSION := $(firstword $(PYTHON_VERSIONS))

# Dependencies installed via pip.
PIP_DEPS := poetry poetry-dynamic-versioning pre-commit tox

# Cross-platform adjustments.
SYS := $(shell uname 2> /dev/null)
ifeq ($(SYS),Linux)
GREP_EXE := grep
else ifeq ($(SYS),Darwin)
GREP_EXE := ggrep
else
$(error Unsupported development platform)
endif

# Docker image name.
GIT_TAG    := $(shell git describe --tags --always --dirty 2> /dev/null || echo "untagged")
GIT_COMMIT := $(shell git rev-parse --quiet --verify HEAD || echo "?")
GIT_DIRTY  := $(shell test -n "`git status --porcelain`" && echo "-dirty" || true)
BUILD_TIME := $(shell date -u '+%Y-%m-%dT%H:%M:%SZ')
IMG_NAME   := ghcr.io/bow/$(APP_NAME)

IS_RELEASE := $(shell ((echo "${GIT_TAG}" | $(GREP_EXE) -qE "^v?[0-9]+\.[0-9]+\.[0-9]+$$") && echo '1') || true)
ifeq ($(IS_RELEASE),1)
IMG_TAG    := $(GIT_TAG)
else
IMG_TAG    := latest
endif

## Rules ##

all: help


.PHONY: build
build:  ## Build wheel and source dist.
	poetry build
	twine check dist/*


.PHONY: clean
clean:  ## Remove build artifacts, including built Docker images.
	rm -rf build/ dist/ && (docker rmi $(IMG_NAME) 2> /dev/null || true)


.PHONY: clean-pyenv
clean-pyenv:  ## Remove the created pyenv virtualenv.
	pyenv uninstall -f $(VENV_NAME) && rm -f .python-version


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
	docker build --build-arg GIT_COMMIT=$(GIT_COMMIT)$(GIT_DIRTY) --build-arg BUILD_TIME=$(BUILD_TIME) --tag $(IMG_NAME):$(IMG_TAG) .


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
lint:  lint-types lint-style lint-metrics lint-sec  ## Run the linter suite.


.PHONY: lint-types
lint-types:  ## Lint the type hints.
	poetry run mypy crimson tests


.PHONY: lint-style
lint-style:  ## Lint style conventions.
	poetry run flake8 --statistics crimson tests && poetry run black -t py310 --check .


.PHONY: lint-metrics
lint-metrics:  ## Lint other metrics.
	poetry run radon cc --total-average --show-closures --show-complexity --min C crimson


.PHONY: lint-sec
lint-sec:  ## Lint security.
	poetry run bandit -r crimson


.PHONY: test
test:  ## Run the test suite.
	poetry run py.test --cov=crimson --cov-config=.coveragerc --cov-report=term-missing --cov-report=xml:.coverage.xml crimson tests


.PHONY: tox
tox:  ## Run the test suite and all linters under all supported Python versions.
	tox --parallel auto
