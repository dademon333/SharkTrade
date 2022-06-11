FROM python:3.10-alpine

WORKDIR /usr/src/app

RUN apk add --no-cache build-base jpeg-dev zlib-dev
COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt

RUN apk add --no-cache postgresql-client

COPY . .

ENTRYPOINT ["python3", "-m", "daemons.global_daemons.run_workers"]