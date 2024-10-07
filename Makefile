# Automated tasks

SHELL := /bin/bash  # override default /bin/sh
TAG ?= $(shell git describe --tags)

# Put first so that "make" without argument is like "make help".
help:
	echo "See Makefile for recipe list"

.PHONY: help

# ----
# Docs
# ----

DOCS_DIR = docs
DOCS_BUILD_DIR = docs/_build

doc8:
	doc8 docs

nb-format-check:
	ruff format --check docs/**/*.ipynb

# Note must be kept in sync with
# `make nb-clean-check`
nb-clean:
	nb-clean clean docs/**/*.ipynb \
        --remove-empty-cells \
		--preserve-cell-metadata tags \
		--preserve-cell-outputs \
		--preserve-execution-counts

nb-clean-check:
	nb-clean check docs/**/*.ipynb \
        --remove-empty-cells \
		--preserve-cell-metadata tags \
		--preserve-cell-outputs \
		--preserve-execution-counts

# Check for broken links in notebooks
# https://github.com/jupyterlab/pytest-check-links
nb-check-links:
	python -m pytest --check-links \
		docs/notebooks/*.ipynb

# Execute all notebooks in docs
# Add `skip-execution` cell tag if you want to skip a cell
# Add `raises-exception` cell tag if you know the cell raises exception
nb-execute: nb-format-check nb-check-links
	jupyter nbconvert --inplace \
		--to notebook \
		--execute \
		docs/notebooks/*.ipynb

	# clean notebooks after execution
	make nb-clean

docs-build: doc8
	sphinx-build -b html $(DOCS_DIR) $(DOCS_BUILD_DIR)/html

docs-clean:
	rm -rf $(DOCS_BUILD_DIR)

docs-serve: doc8
	sphinx-autobuild \
		--re-ignore _build\/.* \
		-b html \
		$(DOCS_DIR) $(DOCS_BUILD_DIR)/html

docs-pdf: doc8
	sphinx-build -b latex $(DOCS_DIR) $(DOCS_BUILD_DIR)/latex

	# this needs to get run twice
	cd $(DOCS_BUILD_DIR)/latex && make
	cd $(DOCS_BUILD_DIR)/latex && make

	echo "PDF exported to $(DOCS_BUILD_DIR)/latex/contrails-forecast.pdf"
