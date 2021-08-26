AWS_REGION = eu-west-3
STACK_NAME = helloworld
STAGE_NAME = develop
CICD_BUCKET = cicd-bucket-eu-west-3

PIP = .venv/bin/pip

stack-build:
	sam build --region $(AWS_REGION) --use-container

stack-deploy: stack-build
	aws s3 cp spec/api-spec.yaml s3://$(CICD_BUCKET)/spec/api-spec.yaml
	sam package --s3-bucket $(CICD_BUCKET) --output-template-file packaged.yaml
	sam deploy packaged.yaml --capabilities CAPABILITY_IAM --parameter-overrides StageName=$(STAGE_NAME) --s3-bucket $(CICD_BUCKET) --stack-name $(STACK_NAME) --region $(AWS_REGION)

stack-delete:
	aws cloudformation delete-stack --stack-name $(STACK_NAME) --region $(AWS_REGION)

test:
	pytest tests

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
