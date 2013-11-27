
DJANGO_ENV=debug
VIRTUALENV=
STATIC=science_qa/static_serve

all: help

deploy: deps migrate static

deps:
	# install new deps
	$(VIRTUALENV)/bin/pip install -r deps.txt

migrate:
	# migrate db if needed
	$(VIRTUALENV)/bin/python manage.py migrate

static: compress
	# collect staticfiles
	echo yes | $(VIRTUALENV)/bin/python manage.py collectstatic

compress:
	# compress css/js
	$(VIRTUALENV)/bin/python manage.py compress


clean:
	rm -rf $(STATIC)/*
	rm -rf */*.pyc

help:
	@echo ""
	@echo "Usage:"
	@echo "  make deploy        - make site deployable"
	@echo "  make deps          - install dependencies"
	@echo "  make migrate       - Update db migrations"
	@echo "  make static        - collec staticfiles"
	@echo "  make compress      - compress css and js"

.PHONY: all clean help
.PHONY: deploy
.PHONY: migrate static compress deps
