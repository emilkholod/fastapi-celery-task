import logging

from fastapi import FastAPI

import routers

logging.basicConfig(level=logging.INFO)

app = FastAPI()
app.include_router(routers.router)
