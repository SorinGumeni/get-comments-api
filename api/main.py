import logging
import os

from fastapi import FastAPI
from mangum import Mangum
from fastapi_paginate import add_pagination

from controllers import comments_controller
from logging_config import setup_logging

description = """
CommentsApi helps you do awesome stuff. 🚀
## Comments

You can **read comments**.

"""

app = FastAPI(
    title="CommentsApi",
    version="0.0.1"
    )

app.include_router(router=comments_controller.router, prefix="/api")

add_pagination(app)

setup_logging()

#Handler used by the lambda function
def handler(event, context):
    asgi_handler = Mangum(app=app)
    response = asgi_handler(event, context)

    return response
