# Makefile for PyDitz.

PYTHON = python$(VER)
SETUP  = $(PYTHON) setup.py
ISSUES = doc/issues
STATIC = build/sphinx/html/_static

.DEFAULT:;	@ $(SETUP) $@
.PHONY:		build doc

all:		build

build:;		@ $(SETUP) $@

doc:		issues
		@ $(SETUP) $@

issues:;	@ touch doc/index.rst
		@ rm -rf $(ISSUES) $(STATIC)
		@ $(PYTHON) ditz/console.py html $(ISSUES)

tags:;		find . -name '*.py' | xargs etags

clean:;		$(SETUP) $@
		rm -rf $(MANIFEST) build dist *.egg-info
