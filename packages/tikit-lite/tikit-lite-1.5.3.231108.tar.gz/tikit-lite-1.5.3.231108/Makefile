.PHONY: test

dev_install:
	pip install -e .
	pip install -e .[test]

test:
	pytest -W ignore

publish:
	twine upload -r pypi dist/*
build:
	python3 setup.py sdist bdist_wheel
build_wheel: clean
	python3 setup.py bdist_wheel
build_dust:
	python3 setup.py sdist
clean:
	rm -rf dist build *.egg-info
install: clean
	pip uninstall -y tikit
	python3 setup.py install
	rm -rf dist build *.egg-info
install_cloud:
	pip uninstall -y tikit
	pip install tikit --upgrade 

help:
	echo "build clean install install_cloud publish"
