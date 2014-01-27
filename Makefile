
DJANGO_ENV=debug
VIRTUALENV_BIN=
STATIC=science_qa/static_serve

all: help

deploy: clean deps migrate static locale

deps:
	# install new deps
	$(VIRTUALENV_BIN)pip install -r deps.txt

deps-upgrade:
	# upgrade deps
	$(VIRTUALENV_BIN)pip install --upgrade -r deps.txt

migrate:
	# migrate db if needed
	$(VIRTUALENV_BIN)python manage.py migrate

static: compress
	# collect staticfiles
	echo yes | $(VIRTUALENV_BIN)python manage.py collectstatic

compress:
	# compress css/js
	$(VIRTUALENV_BIN)python manage.py compress

locale:
	# compile translations
	$(VIRTUALENV_BIN)django-admin.py compilemessages

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
	@echo "  make locale        - compile translations"

.PHONY: all clean help
.PHONY: deploy
.PHONY: migrate static compress deps locale
