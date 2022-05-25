FROM python:3.10-alpine

WORKDIR /usr/src/app

RUN apk add --no-cache build-base postgresql-client
COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt

COPY . .

ENTRYPOINT ["python3", "-m", "background_workers.run_workers"]