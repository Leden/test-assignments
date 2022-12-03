PROJECT = lunchvote

BACKEND_SERVICE = $(PROJECT)-django

COMPOSE_BASE = docker-compose -f docker-compose.yaml
COMPOSE = $(COMPOSE_BASE) -f docker-compose.dev.yaml

TEST_OPTS =
TEST_RUN_OPTS =
TEST_FILES =


bootstrap:
	sh scripts/bootstrap.sh

release:
	sh scripts/release.sh

release/patch:
	sh scripts/release.sh --patch

release/minor:
	sh scripts/release.sh --minor

release/major:
	sh scripts/release.sh --major

changelog:
	sh scripts/changelog.sh

bash:
	$(COMPOSE) run $(BACKEND_SERVICE) docker-start bash

shell:
	$(COMPOSE) run $(BACKEND_SERVICE) docker-start manage.py shell_plus

dbshell:
	$(COMPOSE) run $(BACKEND_SERVICE) docker-start manage.py dbshell

update-initial-data-fixtures:
	$(COMPOSE) run $(BACKEND_SERVICE) docker-start bash /scripts/update-initial-data-fixtures.sh

reset-db:
	$(COMPOSE) run $(BACKEND_SERVICE) docker-start bash /scripts/reset-db.sh

test:
	$(COMPOSE) run $(TEST_RUN_OPTS) $(BACKEND_SERVICE) docker-start pytest $(TEST_OPTS) $(TEST_FILES)

test-migrations:
	$(COMPOSE) run $(BACKEND_SERVICE) docker-start manage.py makemigrations --check --noinput --dry-run

start:
	$(COMPOSE) up -d --remove-orphans && docker attach $(BACKEND_SERVICE)

stop:
	$(COMPOSE) down

build: stop
	$(COMPOSE) build

restart: stop start


.PHONY: bash shell dbshell test test-migrations start stop build restart update-initial-data-fixtures release release/patch release/minor release/major changelog reset-db
