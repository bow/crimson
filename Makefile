.PHONY: build clean

build:
	python setup.py sdist bdist_wheel

clean:
	rm -rf build/ dist/
