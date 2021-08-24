AWS_REGION = eu-west-3
STACK_NAME = bookshelf
CICD_BUCKET = cicd-bucket-eu-west-3

PIP = .venv/bin/pip

stack-build:
	sam build --region $(AWS_REGION) --use-container

stack-deploy: stack-build
	aws s3 cp spec/api-spec.yaml s3://$(CICD_BUCKET)/spec/api-spec.yaml
	sam package --s3-bucket $(CICD_BUCKET) --output-template-file packaged.yaml
	sam deploy packaged.yaml --capabilities CAPABILITY_IAM --s3-bucket $(CICD_BUCKET) --stack-name $(STACK_NAME) --region $(AWS_REGION)

stack-delete:
	aws cloudformation delete-stack --stack-name $(STACK_NAME) --region $(AWS_REGION)

invoke-local-create-book: stack-build
	sam local invoke CreateBookFunction -e events/create_book.json --env-vars events/environment.json

invoke-local-delete-book: stack-build
	sam local invoke DeleteBookFunction -e events/delete_book.json

test:
	UNIT_TEST=True; pytest tests

test-remote:
	pytest tests

dynamodb-create-table:
	aws dynamodb create-table --endpoint-url http://localhost:8080 --table-name books \
		--key-schema AttributeName=author,KeyType=HASH AttributeName=title,KeyType=RANGE \
		--attribute-definitions AttributeName=author,AttributeType=S AttributeName=title,AttributeType=S AttributeName=genre,AttributeType=S AttributeName=publication_date,AttributeType=S \
		--local-secondary-indexes "[{\"IndexName\":\"author-genre\",\"KeySchema\":[{\"AttributeName\":\"author\",\"KeyType\":\"HASH\"},{\"AttributeName\":\"genre\",\"KeyType\":\"RANGE\"}],\"Projection\":{\"ProjectionType\":\"ALL\"}}]" \
		--global-secondary-indexes "[{\"IndexName\":\"genre-publication\",\"KeySchema\":[{\"AttributeName\":\"genre\",\"KeyType\":\"HASH\"},{\"AttributeName\":\"publication_date\",\"KeyType\":\"RANGE\"}],\"Projection\":{\"ProjectionType\":\"ALL\"}}]" \
		--billing-mode PAY_PER_REQUEST

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
