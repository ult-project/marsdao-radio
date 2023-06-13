FROM python:alpine

COPY requirements.txt ./requirements.txt

RUN set -x; \
    apk update && apk upgrade && \
    apk add --no-cache ffmpeg logrotate && \
    mkdir /app

RUN set -x; \
    python -m pip install --no-cache-dir -U pip && \
    python -m pip install --no-cache-dir -r requirements.txt

COPY logrotate.conf /etc/logrotate.d

WORKDIR /app

CMD ["python", "-u", "main.py"]
