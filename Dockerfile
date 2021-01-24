FROM python:3.9.1-alpine3.12

EXPOSE 8080/tcp
EXPOSE 8081/tcp
ENV PYTHONUNBUFFERED=1
ENV POETRY_VERSION="1.1.4"
ENV PIP_DISABLE_PIP_VERSION_CHECK=on
WORKDIR /usr/src/app

RUN apk update
RUN apk add gcc musl-dev libffi-dev g++ openssl-dev

RUN pip install "poetry==$POETRY_VERSION"
COPY poetry.lock pyproject.toml ./
RUN POETRY_VIRTUALENVS_CREATE=false poetry install \
 && pip uninstall -y poetry

COPY alerticular alerticular

CMD [ "python", "alerticular/cli.py" ]
