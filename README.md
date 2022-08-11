# Fitia Exercise

Repo for the exercise part of Fitia's application process

## Installation

The project can be used with Docker Compose for both development and production.

For development
```bash
docker compose build
docker compose --rm run django python src/manage.py migrate
docker compose --rm run django python src/manage.py get_food
```

For production
```bash
docker compose -f production.yml build
docker compose -f production.yml --rm run django python src/manage.py migrate
docker compose -f production.yml --rm run django python src/manage.py collectstatic
docker compose -f production.yml --rm run django python src/manage.py get_food
```

## Usage

```
docker compose up
```

If in development, project is hosted at `localhost:8000`

If in production, project is hosted at `localhost`