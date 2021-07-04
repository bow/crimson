# Application name.
APP_NAME := crimson

# Virtualenv name.
VENV_NAME := $(APP_NAME)-dev

# Supported Python versions; latest listed first.
PYTHON_VERSIONS := 3.9.5 3.8.10 3.7.10

# Python version used for virtualenv.
PYTHON_VERSION := $(firstword $(PYTHON_VERSIONS))

# Dependencies installed via pip.
PIP_DEPS := poetry poetry-dynamic-versioning pre-commit tox


## Rules ##

# Build packages.
.PHONY: build
build:
	poetry build
	twine check dist/*


# Clean built packages.
.PHONY: clean
clean:
	rm -rf build/ dist/


# Clean pyenv virtualenv.
.PHONY: clean-pyenv
clean-pyenv:
	pyenv uninstall -f $(VENV_NAME) && rm -f .python-version


# Set up the development environment.
.PHONY: dev
dev:
	pip install $(PIP_DEPS)
	pre-commit install
	poetry install
	@pyenv rehash 2> /dev/null || true


# Set up pyenv for development.
.PHONY: dev-pyenv
dev-pyenv:
	@if command -v pyenv virtualenv 1>/dev/null 2>&1; then \
		for py_version in $(PYTHON_VERSIONS); do \
			printf "%s\n" "Installing Python $${py_version} with pyenv ..." 1>&2 \
				&& pyenv install -s "$${py_version}"; \
		done \
			&& printf "%s\n" "Setting up virtualenv $(VENV_NAME) in Python $(PYTHON_VERSION) ..." 1>&2 \
			&& pyenv virtualenv -f "$(PYTHON_VERSION)" "$(VENV_NAME)" \
			&& printf "%s\n" "$(VENV_NAME)" > .python-version \
			&& for py_version in $(PYTHON_VERSIONS); do \
				echo "$${py_version}" >> .python-version; \
			done \
			&& printf "%s\n" "Completed pyenv setup." 1>&2; \
	else \
		printf "pyenv not found" 1>&2 && exit 1; \
	fi


# Run the linter suite.
.PHONY: lint
lint:
	tox -qe security,style,types


# Run the test suite.
.PHONY: test
test:
	tox -qe py39,py38,py37
