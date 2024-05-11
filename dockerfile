FROM python:3.8.12-alpine3.15
WORKDIR /app
RUN apk update && apk add gcc g++

RUN apk add --no-cache tzdata
ENV TZ America/Los_Angeles

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

CMD [ "python3", "main.py" ]