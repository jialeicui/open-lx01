

install-dev-dep:
	python -m pip install -r requirements-dev.txt

install-dep:
	python -m pip install -r requirements.txt

format:
	python -m isort .
	python -m ruff check --fix .
	python -m black .

lint:
	python -m mypy .
	python -m ruff check .

test:
	python -m pytest ./tests -n auto -vv
