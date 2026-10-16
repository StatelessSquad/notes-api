.PHONY: setup dev test lint
setup: ## install toolchain + hooks
	@command -v poetry >/dev/null || curl -sSL https://install.python-poetry.org | python3 -
	@poetry install --with dev
	@poetry run pre-commit install
dev: ## run locally
	@poetry run uvicorn src.notes_api.main:app --reload
test: ## run tests
	@poetry run pytest
lint: ## lint
	@poetry run pre-commit run -a
