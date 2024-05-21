import logging

from fastapi import FastAPI

logger = logging.getLogger(__name__)

app = FastAPI()


@app.get("/")
async def hello() -> dict:
    return {"msg": "Hello World"}


@app.get("/echo/{msg}")
async def echo(msg: str) -> dict:
    return {"msg": f"{msg}"}
