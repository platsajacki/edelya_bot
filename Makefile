install-hooks:
	@$(if $(wildcard .git/hooks/pre-commit), \
			echo pre-commit hook already exists, \
			pre-commit install && echo pre-commit hooks installed)

dev-install:
	pip install -r src/requirements.txt
	pip install -r src/requirements-dev.txt
	make install-hooks

prod-install:
	pip install -r requirements.txt

fmt:
	ruff format src --check || true && ruff format src

lint:
	ruff check src --show-fixes

fmt+lint:
	make fmt
	make lint

lint-unsafe:
	ruff check src --show-fixes --unsafe-fixes

mypy:
	mypy src

check:
	make install-hooks
	ruff check src --no-fix
	make mypy

tag:
	make check
	make test
	./tags-pretty.sh

test:
	make install-hooks
	pytest $(TEST) --create-db $(COVERAGE) $(F)

load-start-data:
	python src/manage.py load_start_data

run:
	python src/main.py