FROM python:3.11.5-alpine

EXPOSE 8080/tcp
EXPOSE 8081/tcp
ENV PYTHONUNBUFFERED=1
ENV POETRY_VERSION="1.2.2"
ENV PIP_DISABLE_PIP_VERSION_CHECK=on
WORKDIR /usr/src/app

COPY poetry.lock pyproject.toml ./
RUN apk update \
 && apk add gcc musl-dev libffi-dev g++ openssl-dev rust cargo \
 && pip install --upgrade pip \
 && pip install "poetry==$POETRY_VERSION" \
 && POETRY_VIRTUALENVS_CREATE=false poetry install --no-dev \
 && pip uninstall -y poetry \
 && apk del gcc g++ rust cargo

COPY alerticular alerticular

CMD [ "python", "alerticular/cli.py" ]
