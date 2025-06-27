import os
import sys
import logging
from aiohttp import web
from multidict import MultiDict
from weasyprint import HTML
from functions import parse_size_string

# Get Gunicorn's error logger if running within Gunicorn
if __name__ != '__main__':
    gunicorn_logger = logging.getLogger('gunicorn.error')
    app_logger = logging.getLogger(__name__)
    app_logger.handlers = gunicorn_logger.handlers
    app_logger.setLevel(gunicorn_logger.level)
else:
    # Fallback for local testing or non-Gunicorn environments
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    app_logger = logging.getLogger(__name__)

config = {
    "client_max_size": 1024**2 * 10
}

if os.environ.get('REQUEST_MAX_SIZE'):
    try:
        config["client_max_size"] = parse_size_string(os.environ.get('REQUEST_MAX_SIZE'))
    except ValueError as e:
        app_logger.error(f"Warning: Failed to parse REQUEST_MAX_SIZE, using default value: {e}", file=sys.stderr)

app_logger.info(f"INFO: Running app with client_max_size={config['client_max_size']}")

app = web.Application(client_max_size=config["client_max_size"])
routes = web.RouteTableDef()

@routes.get('/health')
async def index(request):
    return web.Response(text='ok')

@routes.get('/')
async def home(request):
    body = '''
        <h1>PDF Generator</h1>
        <p>The following endpoints are available:</p>
        <ul>
            <li>POST to <code>/pdf?filename=myfile.pdf</code>. The body should
                contain html</li>
            <li>POST to <code>/multiple?filename=myfile.pdf</code>. The body
                should contain a JSON list of html strings. They will each
                be rendered and combined into a single pdf</li>
        </ul>
    '''
    headers = MultiDict({'Content-Type': 'text/html'})
    return web.Response(body=body, headers=headers)


@routes.post('/pdf')
async def generate(request):
    name = request.query.get('filename', 'unnamed.pdf')
    data = await request.json()
    html = HTML(string=data.get('data', ''))
    pdf = html.write_pdf()
    headers = MultiDict({
        'Content-Type': 'application/pdf',
        'Content-Disposition': 'inline;filename=%s' % name
    })
    return web.Response(body=pdf, headers=headers)

@routes.post('/multiple')
async def multiple(request):
    name = request.query.get('filename', 'unnamed.pdf')
    data = await request.json()
    htmls = data.get('data')
    documents = [HTML(string=html).render() for html in htmls]
    pdf = documents[0].copy(
        [page for doc in documents for page in doc.pages]
    ).write_pdf()
    headers = MultiDict({
        'Content-Type': 'application/pdf',
        'Content-Disposition': 'inline;filename=%s' % name
    })
    return web.Response(body=pdf, headers=headers)

app.router.add_routes(routes)
