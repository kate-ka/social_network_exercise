install:
	pip install -r requirements.txt
	python manage.py migrate

install-bot:
	pip install -r bot/requirements.txt

test:
	pytest --cov=apps --cov=api tests/

test-docker:
	docker-compose exec api pytest --cov=apps --cov=api tests/


