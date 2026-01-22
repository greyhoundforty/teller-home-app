# AGENTS.md

## Tooling
- Python 3.10+
- uv / venv / pip
- docker
- mise as main task runner

## setup
- python3 -m venv .venv
- source .venv/bin/activate
- uv pip install --upgrade pip
- uv pip install -r requirements.txt
- cp .env.example .env

## test
- pytest tests/ --verbose
- coverage run -m pytest
- coverage report --show-missing

## lint
- black src/ --check --diff
- isort src/ --check-only
- flake8 src/
- mypy src/

## build
- python setup.py clean --all
- python setup.py build
- python setup.py bdist_wheel

<!-- ## deploy
- python manage.py collectstatic --noinput
- python manage.py migrate
- gunicorn --workers=4 app.wsgi:application -->