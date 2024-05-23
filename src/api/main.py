import json
import logging

from fastapi import FastAPI, Request

from src.msg import MsgIn, MsgOut

from .rabbit import push_message

logger = logging.getLogger(__name__)

app = FastAPI()


@app.get("/")
async def hello() -> dict:
    return {"msg": "Hello World"}


@app.get("/echo/{msg}")
async def echo(msg: str) -> dict:
    return {"msg": f"{msg}"}


async def prepare_answer(message: MsgIn) -> MsgOut | None:
    answer = MsgOut(
        chat_id=message.chat.id,
        text=f"your quest: {message.text}\nMy ans: {'go home'}",
        reply_to_message_id=(
            message.reply_to_message.message_id if message.reply_to_message else None
        ),
    )
    return answer


async def process_message(message: MsgIn) -> None:
    answer = await prepare_answer(message)
    if answer:
        await push_message(answer)


@app.post("/ask")
async def ask(request: Request) -> dict:
    data: dict = json.loads(await request.json())
    # TODO: try except
    await process_message(MsgIn(**data))
    return {"status": "ok"}
