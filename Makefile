AWS_REGION = eu-west-3
STACK_NAME = bookshelf
STAGE = develop

PIP = .venv/bin/pip

stack-build:
	sam build --debug
	sam package --s3-bucket cicd-bucket-2020 --output-template-file packaged.yaml

stack-deploy: build
	sam deploy packaged.yaml --stack-name $(STACK_NAME)

stack-delete:
	aws cloudformation delete-stack --stack-name $(STACK_NAME)

invoke-local-create-book:
	sam local invoke CreateBookFunction -e events/create_book.json

invoke-local-delete-book:
	sam local invoke DeleteBookFunction -e events/delete_book.json

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
