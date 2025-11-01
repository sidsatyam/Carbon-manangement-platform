APP_NAME = carbon-iot-service
VERSION = 1.0.0

.PHONY: test build docker

test:
	pip install -r device-service/requirements.txt
	pytest device-service/tests

build:
	docker compose build

docker-up:
	docker compose up --build -d

docker-down:
	docker compose down
