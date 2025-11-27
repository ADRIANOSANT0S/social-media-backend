.PHONY: run server migrate makemigrations startapp shell test

POETRY= poetry run
MANAGE= $(POETRY) python manage.py

dev:
	@echo "starting the Django development server..."
	$(MANAGE) runserver

migrate:
	@echo "applying database migrations"
	$(MANAGE) makemigrations
	$(MANAGE) migrate
	
makemigrations:
	@echo "createing migrations for the database..."
	$(MANAGE) makemigrations $(name)

startapp:
	@echo "Creating app named $(name)..."
	$(MANAGE) startapp $(name)
	@mkdir -p apps
	@mv $(name) apps/

lint:
	@echo "running linters..."
	$(POETRY) flake8 .
	$(POETRY) black --check .
	$(POETRY) isort --check .

format:
	@echo "Running black formatter..."
	$(POETRY) black . &&  $(POETRY) isort . && $(POETRY) isort .

shell:
	@echo "starting the Django shell"
	$(MANAGE) shell

tests:
	@echo "running the Django tests.."
	$(POETRY) pytest 

test: 
	@echo "running the Django test: $(TEST)..."
	$(POETRY) pytest $(TEST)

test-watch:
	@echo "starting the pytest watch mode..."
	$(POETRY) ptw

test-debug:
	@echo "starting the pytest debug mode..."
	$(POETRY) pytest --pdb --maxfail=1 -q