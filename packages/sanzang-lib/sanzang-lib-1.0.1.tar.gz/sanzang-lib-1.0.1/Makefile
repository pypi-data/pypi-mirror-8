PYTHON3 = python3

.PHONY: all clean dist

all:

dist:
	$(PYTHON3) setup.py sdist

clean:
	rm -f -- *.pyc *.pyo */*.pyc */*.pyo
	rm -rf -- __pycache__ */__pycache__
	rm -f MANIFEST
	rm -f PKG-INFO
	rm -rf build
	rm -rf dist
