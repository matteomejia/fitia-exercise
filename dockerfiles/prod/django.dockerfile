FROM python:3.10 as prod-base

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONFAULTHANDLER=1 \
    PYTHONHASHSEED=random \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100 \
    POETRY_HOME="/opt/poetry"

RUN curl -sSL https://install.python-poetry.org | python -

FROM prod-base as prod-builder

ENV POETRY_HOME="/opt/poetry" \ 
    PATH="${POETRY_HOME}/bin:$PATH"

WORKDIR /usr/src/app

COPY pyproject.toml poetry.lock ./

RUN poetry export --without-hashes --output requirements.txt

FROM node:16-slim as prod-tailwind

WORKDIR /usr/src/app

COPY package.json yarn.lock ./
RUN yarn

COPY . .

RUN yarn build


FROM python:3.10-slim-buster as production

RUN mkdir -p /home/app
RUN groupadd app && useradd -g app app

ENV HOME=/home/app
ENV APP_HOME=/home/app/django
RUN mkdir ${APP_HOME}
WORKDIR ${APP_HOME}

RUN apt-get update && apt-get install -y build-essential libpq-dev
COPY --from=prod-builder /usr/src/app/requirements.txt .
RUN pip install -r requirements.txt

COPY . ${APP_HOME}
COPY --from=prod-tailwind /usr/src/app/src/static/css/main.css ${APP_HOME}/src/static/css/main.css

RUN mkdir ${APP_HOME}/static

RUN chown -R app:app ${APP_HOME}

USER app