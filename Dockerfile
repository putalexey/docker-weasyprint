FROM python:3.10.3-alpine3.15

ENV TERM=xterm

RUN apk add --no-cache --virtual build-dependencies make gcc \
  g++ ca-certificates zlib-dev jpeg-dev tiff-dev freetype-dev lcms2-dev \
  libwebp-dev tcl-dev tk-dev libxml2-dev libxslt-dev libffi-dev

RUN apk add --no-cache libffi-dev gdk-pixbuf-dev py3-lxml shared-mime-info \
    msttcorefonts-installer pango-dev cairo-dev fontconfig && \
    apk add --no-cache \
    --repository http://dl-4.alpinelinux.org/alpine/edge/testing/ \
    ttf-font-awesome && update-ms-fonts && fc-cache -f

RUN mkdir -p /usr/src/app/
WORKDIR /usr/src/app/

COPY requirements.txt /usr/src/app/
RUN pip install --no-cache-dir -r requirements.txt

COPY Dockerfile /usr/src/app/
COPY app.py /usr/src/app/
COPY functions.py /usr/src/app/

ARG NUM_WORKERS=3
ARG TIMEOUT=120

ENV NUM_WORKERS=$NUM_WORKERS \
    TIMEOUT=$TIMEOUT \
    LANG=en_US.UTF-8

EXPOSE 5001

COPY --chmod=755 <<EOT /entrypoint.sh
#!/usr/bin/env sh
set -e
exec gunicorn --bind 0.0.0.0:5001 \\
  --timeout $TIMEOUT \\
  --worker-class aiohttp.GunicornWebWorker \\
  --workers $NUM_WORKERS \\
  --access-logfile - \\
  app:app
EOT
ENTRYPOINT ["/entrypoint.sh"]
