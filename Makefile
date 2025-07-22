.PHONY: run server migrate makemigrations startapp shell test

MANAGE=poetry run python manage.py

dev:
	@echo "starting the Django development server..."
	$(MANAGE) runserver

migrate:
	@echo "applying database migrations"
	$(MANAGE) makemigrations
	$(MANAGE) migrate
	
makemigrations:
	@echo "createing migrations for the database..."
	$(MANAGE) makemigrations

startapp:
	@echo "Creating app named $(name)..."
	$(MANAGE) startapp $(name)
	@mkdir -p apps
	@mv $(name) apps/

lint:
	@echo "running linters..."
	poetry run flake8 .
	poetry run black --check .
	poetry run isort --check .

format:
	@echo "Running black formatter..."
	poetry run black . &&  poetry run isort . && poetry run isort .

shell:
	@echo "starting the Django shell"
	$(MANAGE) shell

test:
	@echo "running the Django tests.."
	$(MANAGE) test