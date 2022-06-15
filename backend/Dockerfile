ARG COMPOSE_PROJECT_NAME
FROM ${COMPOSE_PROJECT_NAME}_frontend as frontend

FROM python:3.10-alpine

WORKDIR /usr/src/app

RUN apk add --no-cache build-base jpeg-dev zlib-dev
COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt

COPY --from=frontend /frontend/build/index.html /frontend/build/index.html

COPY . .

EXPOSE 8080
ENTRYPOINT ["gunicorn", "main:app"]
CMD ["-c", "gunicorn_config.py"]