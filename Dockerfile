FROM lgatica/python-alpine:3.6-onbuild

ARG NUM_WORKERS=3
ARG TIMEOUT=120
ENV NUM_WORKERS=$NUM_WORKERS TIMEOUT=$TIMEOUT LANG=en_US.UTF-8

RUN apk add --no-cache libffi-dev gdk-pixbuf-dev py3-lxml shared-mime-info \
    msttcorefonts-installer pango-dev cairo-dev fontconfig && \
    apk add --no-cache \
    --repository http://dl-4.alpinelinux.org/alpine/edge/testing/ \
    ttf-font-awesome && update-ms-fonts && fc-cache -f

EXPOSE 5001

CMD gunicorn --bind 0.0.0.0:5001 --timeout $TIMEOUT --workers $NUM_WORKERS wsgi:app
