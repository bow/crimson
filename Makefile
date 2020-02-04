.PHONY: build clean

build:
	python setup.py sdist bdist_wheel
	twine check dist/*

clean:
	rm -rf build/ dist/
