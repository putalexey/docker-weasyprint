# docker-weasyprint

[![dockeri.co](http://dockeri.co/image/lgatica/weasyprint)](https://hub.docker.com/r/lgatica/weasyprint/)

[![Build Status](https://travis-ci.org/lgaticaq/docker-weasyprint.svg?branch=master)](https://travis-ci.org/lgaticaq/docker-weasyprint)

[Weasyprint](http://weasyprint.org/) as a microservice in a docker image.

# Usage

Run the docker image, exposing port 5001

```
docker run -d --name weasyprint -p 5001:5001 lgatica/weasyprint
```

A `POST` with json `{"data": "<h1>Hello world</h1>"}` to port `/pdf` on port 5001 with an html body with give a response containing a PDF. The filename may be set using a query parameter, e.g.:

```
http POST http://127.0.0.1:5001/pdf data="<h1>Hello world</h1>" > result.pdf
```

Or a `POST` with json `{"data": ["<h1>Hello world</h1>", "<h1>Hola mundo</h1>"]}` to port `/multiple` on port 5001 with an html body with give a response containing a PDF. The filename may be set using a query parameter, e.g.:

```
http POST http://127.0.0.1:5001/multiple data:='["<h1>Hello world</h1>", "<h1>Hola mundo</h1>"]' > result.pdf
```

This will use the file `source.html` and return a response with `Content-Type: application/pdf` and `Content-Disposition: inline; filename=result.pdf` headers.  The body of the response will be the PDF.

In addition `/health` is a health check endpoint and a `GET` returns 'ok'.
