FROM python:3.7.7-alpine3.12 as base

WORKDIR /usr/src/app

ENV PYTHONFAULTHANDLER=1 \
  PYTHONUNBUFFERED=1 \
  PYTHONHASHSEED=random \
  PIP_NO_CACHE_DIR=off \
  PIP_DISABLE_PIP_VERSION_CHECK=on \
  PIP_DEFAULT_TIMEOUT=100 \
  POETRY_VERSION=1.1.5

RUN apk add python3-dev postgresql-dev

FROM base as builder

RUN apk add --no-cache libffi-dev g++ gcc make libffi-dev  musl-dev openssl-dev cargo

RUN pip install --upgrade pip wheel&& \
    pip install "poetry==$POETRY_VERSION"

RUN python -m venv /venv
 
COPY poetry.lock pyproject.toml ./
COPY app ./app

RUN . /venv/bin/activate && poetry install --no-root --no-dev
RUN . /venv/bin/activate && poetry build
 
FROM base as final

COPY --from=builder /venv /venv
COPY --from=builder /usr/src/app/dist .
COPY wsgi.py ./wsgi.py
COPY docker/entrypoint.sh ./entrypoint.sh

ENV PATH="/venv/bin:${PATH}"
RUN . /venv/bin/activate && pip install *.whl

EXPOSE 5000
ENTRYPOINT ["./entrypoint.sh"]
