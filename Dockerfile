FROM python:3.9.1-alpine3.12
RUN apk update
RUN apk add gcc musl-dev libffi-dev g++

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY setup.py .
COPY alerticular alerticular
RUN pip install .


CMD [ "alerticular" ]
