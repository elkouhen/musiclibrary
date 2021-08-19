AWS_REGION = eu-west-3
STACK_NAME = bookshelf
STAGE = develop

PIP = .venv/bin/pip

stack-build:
	sam build --region $(AWS_REGION)

stack-deploy: stack-build
	sam package --s3-bucket cicd-bucket-2020 --output-template-file packaged.yaml
	sam deploy packaged.yaml --stack-name $(STACK_NAME) --region $(AWS_REGION)

stack-delete:
	aws cloudformation delete-stack --stack-name $(STACK_NAME) --region $(AWS_REGION)

invoke-local-create-book: stack-build
	sam local invoke CreateBookFunction -e events/create_book.json

invoke-local-delete-book: stack-build
	sam local invoke DeleteBookFunction -e events/delete_book.json

test:
	AWS_ENDPOINT_URL=http://172.17.0.1:8080; pytest tests

dynamo-create-table:
	aws dynamodb create-table --endpoint-url http://localhost:8080 --table-name books --key-schema AttributeName=author,KeyType=HASH AttributeName=title,KeyType=RANGE --attribute-definitions AttributeName=author,AttributeType=S AttributeName=title,AttributeType=S --billing-mode PAY_PER_REQUEST

dynamodb-start:
	docker run --name dynamodb-shared -p 8080:8000 -d amazon/dynamodb-local -jar DynamoDBLocal.jar -sharedDb -dbPath .

dynamodb-stop:
	docker rm -f dynamodb-shared

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
