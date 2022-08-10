FROM python:3.10 as python-base

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONFAULTHANDLER=1 \
    PYTHONHASHSEED=random \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100 \
    POETRY_HOME="/opt/poetry"

RUN curl -sSL https://install.python-poetry.org | python -

FROM python-base as staging

ENV POETRY_HOME="/opt/poetry" \ 
    PATH="${POETRY_HOME}/bin:$PATH"

WORKDIR /code

COPY pyproject.toml poetry.lock /code/

RUN poetry export --dev --without-hashes --output requirements.txt
RUN pip install -r requirements.txt

FROM staging as development

WORKDIR /code

COPY . .