""" FastApi Main module """

import sys
import time
import traceback
import logging
import logging.handlers
import uvicorn
# from settings import settings
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
import json_logging
from utils.settings import settings
from api.debug.router import router as debug

# from db import SessionLocal


app = FastAPI()

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
log_handler = logging.handlers.RotatingFileHandler(filename=settings.log_path + '/x-ljson.log', maxBytes=5000000, backupCount=10)
logger.addHandler(log_handler)
json_logging.init_fastapi(enable_json=True)
json_logging.init_request_instrument(app)
logger.info("Starting")


@app.middleware("http")
async def middle(request: Request, call_next):
    """ Wrapper function to manage errors and logging """
    start_time = time.time()
    if "key" in request.query_params and "xyz" == request.query_params['key']:
        try:
            response = await call_next(request)
        except:
            stack = []
            ex = sys.exc_info()[1]
            if ex:
                for frame, lineno in traceback.walk_tb(ex.__traceback__):
                    # Exclude log entries inside python libraries
                    if "site-packages" not in frame.f_code.co_filename:
                        stack.append({'file': frame.f_code.co_filename, 'function': frame.f_code.co_name, 'line': lineno})
                logger.error(str(ex), extra={'props': {'stack': stack}})
            response = JSONResponse(status_code=500, content={"status": "failed", "error": {"code": 99, "message": "internal error"}})
    else:
        response = JSONResponse(status_code=400, content={'status': 'failed', 'error': {'code': 100, 'message': 'invalid'}})
    response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'
    logger.info("Processed", extra={'props': {
                "duration": 1000 * (time.time() - start_time),
                'verb': request.method,
                'path': str(request.url.path),
                'http_status': response.status_code}})
    return response


@app.get("/")
async def root():
    """ Sample / dummy root response """
    return {"Hello": "World"}

app.include_router(debug, prefix='/debug')

# @app.get("/items/{item_id}")
# async def read_item(item_id: int, q: Optional[str] = None):
#    return {"item_id": item_id, "q": q}


if __name__ == "__main__":
    # uvicorn.run("main:app", reload=True)
    uvicorn.run(app, host=settings.listening_host, port=settings.listening_port)
