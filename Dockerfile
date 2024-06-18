FROM python:3.10-alpine

WORKDIR /app

COPY . .

RUN apk add --no-cache ffmpeg && \
    pip install -r requirements.txt

ENTRYPOINT [ "python", "main.py" ]

CMD [ "--help" ]