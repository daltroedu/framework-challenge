FROM python:3.8.5-alpine

WORKDIR /usr/src/project
COPY . /usr/src/project

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apk add --update tzdata
ENV TZ=America/Sao_Paulo

RUN apk add gcc musl-dev postgresql-dev python3-dev libffi-dev openssl-dev bash

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

EXPOSE 5000

RUN chmod +x ./scripts/docker-entrypoint.sh

ENTRYPOINT ["./scripts/docker-entrypoint.sh"]