# Makefile for common development tasks.
#
# Copyright (c) 2015-2022 Wibowo Arindrarto <contact@arindrarto.dev>
# SPDX-License-Identifier: BSD-3-Clause
#
# This file is part of crimson <https://github.com/bow/crimson>.

# Application name.
APP_NAME := crimson


all: help


.PHONY: build
build:  ## Build wheel and source dist.
	poetry build


.PHONY: clean
clean:  ## Remove build and test artifacts, including built Docker images.
	rm -rf build/ dist/ wheels/ \
			.coverage .coverage.xml .junit.xml .tox/ .cache/ .mypy_cache/ .pytest_cache/ \
		&& (docker rmi ghcr.io/bow/$(APP_NAME) 2> /dev/null || true)


.PHONY: clean-pyenv
clean-pyenv:  ## Remove the created pyenv virtualenv.
	pyenv virtualenv-delete -f $(VENV_NAME) && rm -f .python-version


.PHONY: dev
dev:  ## Configure a local development setup.
	@if command -v nix-env > /dev/null && command -v direnv > /dev/null; then \
		printf "Configuring a local dev environment and setting up git pre-commit hooks...\n" >&2 \
			&& direnv allow . > /dev/null \
			&& DIRENV_LOG_FORMAT="" direnv exec $(CURDIR) pre-commit install \
			&& printf "Done.\n" >&2; \
	elif command -v nix-env > /dev/null; then \
		printf "Error: direnv seems to be unconfigured or missing\n" >&2 && exit 1; \
	elif command -v direnv > /dev/null; then \
		printf "Error: nix seems to be unconfigured or missing\n" >&2 && exit 1; \
	else \
		printf "Error: both direnv and nix seem to be unconfigured and/or missing" >&2 && exit 1; \
	fi


.PHONY: dev-reset
dev-reset:  ## Resets the local development environment.
	rm -rf .venv .direnv && direnv reload


.PHONY: fmt
fmt:  ## Apply Black.
	black -t py312 .


.PHONY: help
help:  ## Show this help.
	$(eval PADLEN=$(shell grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) \
		| cut -d':' -f1 \
		| awk '{cur = length($$0); lengths[cur] = lengths[cur] $$0 ORS; max=(cur > max ? cur : max)} END {printf "%s", max}' \
		|| (true && echo 0)))
	@(grep --version > /dev/null 2>&1 || (>&2 "error: GNU grep not installed"; exit 1)) \
		&& printf "\033[36m◉ %s dev console\033[0m\n" "$(APP_NAME)" >&2 \
		&& grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) \
			| awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m» \033[33m%-*s\033[0m \033[36m· \033[0m%s\n", $(PADLEN), $$1, $$2}' \
			| sort


.PHONY: img
img:  ## Build a docker image and load it into a running daemon.
	nix build .#dockerArchiveStreamer && ./result | docker image load


.PHONY: lint
lint:  lint-types lint-style lint-metrics  ## Run the linter suite.


.PHONY: lint-types
lint-types:  ## Lint the type hints.
	run mypy crimson tests


.PHONY: lint-style
lint-style:  ## Lint style conventions.
	flake8 --statistics crimson tests && black -t py312 --check .


.PHONY: lint-metrics
lint-metrics:  ## Lint other metrics.
	python -m radon cc --total-average --show-closures --show-complexity --min C crimson


.PHONY: scan-sec
scan-sec: scan-sec-ast scan-sec-deps  ## Perform all security analyses.


.PHONY: scan-sec-ast
scan-sec-ast:  ## Perform static security analysis on the AST.
	bandit -r crimson


.PHONY: scan-sec-deps
scan-sec-deps:  ## Scan dependencies for reported vulnerabilities.
	poetry export --without-hashes -f requirements.txt -o /dev/stdout | safety check --full-report --stdin


.PHONY: test
test:  ## Run the test suite.
	py.test --junitxml=.junit.xml --cov=crimson --cov-report=term-missing --cov-report=xml:.coverage.xml crimson tests


.PHONY: tox
tox:  ## Run the test suite and all linters under all supported Python versions.
	tox --parallel auto
