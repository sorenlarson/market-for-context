PYTHON ?= python3
BASE_PYTHON ?= python3
RUFF ?= ruff

.PHONY: bootstrap install test figures examples reproduce audit

bootstrap:
	$(BASE_PYTHON) -m venv .venv
	.venv/bin/python -m pip install --upgrade pip
	.venv/bin/python -m pip install -r requirements-lock.txt
	.venv/bin/python -m pip install -e . --no-deps
	$(MAKE) audit PYTHON=.venv/bin/python RUFF=.venv/bin/ruff

install:
	$(PYTHON) -m pip install -r requirements-lock.txt
	$(PYTHON) -m pip install -e . --no-deps

test:
	$(PYTHON) -m pytest

figures:
	$(PYTHON) scripts/generate_figures.py
	$(PYTHON) scripts/generate_pledgeability.py
	$(PYTHON) scripts/generate_firm_size.py
	$(PYTHON) scripts/generate_ownership_access.py
	$(PYTHON) scripts/generate_appropriation.py

examples:
	$(PYTHON) scripts/generate_examples.py

reproduce: test figures examples

audit: reproduce
	$(PYTHON) -m compileall -q src scripts tests
	$(RUFF) format --check src scripts tests
	$(RUFF) check src scripts tests
	$(PYTHON) scripts/check_package.py
