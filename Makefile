PIP := .venv/bin/pip

bootstrap: .venv
	$(PIP) install -e .
	$(PIP) install -r requirements.txt
ifneq ($(wildcard dev-requirements.txt),)
	$(PIP) install -r dev-requirements.txt
endif


.venv:
	python -m venv .venv
	$(PIP) install --upgrade pip
	$(PIP) install --upgrade setuptools
	$(PIP) install --upgrade wheel
