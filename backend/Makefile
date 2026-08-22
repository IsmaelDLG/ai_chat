.PHONY: install run test add freeze

install:
	pip install -r requirements.txt

run:
	uvicorn app.main:app --reload

test:
	pytest

add:
	pip install $(package)
	pip freeze > requirements.txt

freeze:
	pip freeze > requirements.txt