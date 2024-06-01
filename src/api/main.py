import json
import logging

from aiogram.utils.formatting import Bold, as_line, as_list, as_section
from fastapi import BackgroundTasks, Depends, FastAPI, Request
from sqlalchemy.ext.asyncio import AsyncSession

from src import models
from src.api.rabbit import push_message_to_forward, push_message_to_send
from src.db.async_db import get_async_db
from src.db.crud import create_obj, get_parent_message
from src.schemas import MsgForward, MsgIn, MsgOut, user_name
from src.settings import settings

logger = logging.getLogger(__name__)

app = FastAPI()


@app.get("/")
async def hello() -> dict:
    return {"msg": "Hello World"}


@app.get("/echo/{msg}")
async def echo(msg: str) -> dict:
    return {"msg": f"{msg}"}


async def robo_answer(message: MsgIn) -> MsgOut | None:
    answer = MsgOut(
        chat_id=message.chat.id,
        text=as_list(
            Bold("ROBO ANSWER:"),
            as_section(
                as_line("go home!"),
            ),
        ).as_html(),
    )
    return answer


async def push_query_to_operator(operator_id: int, message: MsgIn) -> None:
    answer = MsgForward(
        chat_id=operator_id,
        from_chat_id=message.chat.id,
        message_id=message.message_id,
    )
    logger.debug(f"push_query_to_operator: {message.message_id}")
    await push_message_to_forward(answer)


async def send_answer(user_id: int, text: str) -> None:
    answer = MsgOut(
        chat_id=user_id,
        text=text,
    )
    logger.debug(f"send answer to {user_id}, text: {text[:20] + '...'}")
    await push_message_to_send(answer)


async def is_operator(user_id: int) -> bool:
    logger.debug(f"is_user({user_id})")
    # TODO
    return user_id == 5378942534


async def is_communication_with_operator(user_id: int) -> bool:
    logger.debug(f"is_communication_with_operator({user_id})")
    # TODO
    return True


async def is_operator_need(text: str) -> bool:
    logger.debug(f"is_operator_need({text[:20]})")
    # TODO
    return False


async def find_operator_for_user(user_id: int) -> int | None:
    logger.debug(f"find_operator_for_user {user_id}")
    # TODO ищем оператора в редисе, если нет, то пустышку
    # 5378942534 - я +7 960 741 0939
    # 7055278609 - планшет +7 960 747 4570
    return 5378942534  # my id


async def process_question(
    message: MsgIn,
    session: AsyncSession,
) -> None:
    if message.from_user is None:
        raise Exception("wrong message: message.from_user is None")
    if not message.text:
        raise Exception("wrong message: message.text is empty")

    # write question to DB
    _: models.Question = await create_obj(
        session=session,
        model=models.Question,
        id=message.db_id,
        message_id=message.message_id,
        user_id=message.from_user.id,
        user_name=user_name(message.from_user),
        text=message.text,
    )

    msg_out: MsgOut | None = None

    if await is_communication_with_operator(message.from_user.id):
        # TODO отправляем запрос оператору
        oper_id: int | None = await find_operator_for_user(message.from_user.id)
        logger.debug(
            f"oper = {oper_id}",
        )
        if oper_id is None:
            # TODO следующий раунд выбора оператора
            pass
        else:
            await push_query_to_operator(oper_id, message)
    elif await is_operator_need(message.text):
        pass
    else:
        msg_out = await robo_answer(message)

    if msg_out:
        await push_message_to_send(msg_out)


async def process_answer(
    message: MsgIn,
    session: AsyncSession,
) -> None:
    if not message.text:
        raise Exception("wrong message: message.text is empty")
    if message.from_user is None:
        raise Exception("wrong message: message.from_user is None")
    if not message.reply_to_message:
        raise Exception("wrong message: message.reply_to_message is None")

    db_forward: models.Message | None = await get_parent_message(
        session=session,
        original_parent_id=message.reply_to_message.message_id,
    )
    if not db_forward:
        raise Exception("can't find forwarded message")

    db_question: models.Message | None = await get_parent_message(
        session=session,
        original_parent_id=db_forward.original_parent_id,
    )
    if not db_question:
        raise Exception("can't find question")

    logger.debug(
        f"message from operator {message.from_user.id} to user {db_question.user_id}",
    )

    _: models.Answer = await create_obj(
        session=session,
        model=models.Answer,
        id=message.db_id,
        question_id=db_question.id,
        operator_id=message.from_user.id,
        operator_name=user_name(message.from_user),
        text=message.text,
    )

    await send_answer(db_question.user_id, message.text)


def is_answer(message: MsgIn) -> bool:
    # Ответ, если выполняются все требования:
    #  - сообщение является ответом;
    #  - сам ответ является пересылкой;
    #  - сообщение получено от бота;
    # TODO:
    #  - проверить сценарий один оператор отвечает на сообщение другого;
    return (
        message.from_user is not None
        and message.reply_to_message is not None
        and message.reply_to_message.forward_origin is not None
        and message.reply_to_message.from_user is not None
        and message.reply_to_message.from_user.id == settings.TG_BOT_ID
    )


def is_question(message: MsgIn) -> bool:
    #  Вопрос если выполняется хотя бы одно требование:
    #   - не пересылка, т.е. любое прямое сообщение - вопрос (в т.ч. и оператор может задать вопрос);
    #   - любой не ответ;
    #   - если ответ, то только на сообщение бота или свое собственное;
    # TODO проверить сценарий:
    #  - пользователь уточняет ответ оператора используя reply;
    #  - оператор задает вопрос боту;
    #  - оператор задает вопрос боту используя ;
    # TODO реализовать сценарий:
    #  - пользователь пересылает чужое сообщение с вопросом боту;
    return message.from_user is not None and (
        message.forward_from is None
        or message.reply_to_message is None
        or (
            message.reply_to_message.from_user is not None
            and message.reply_to_message.from_user.id
            in (
                message.from_user.id,
                settings.TG_BOT_ID,
            )
        )
    )


@app.post("/message")
async def ask(
    request: Request,
    background_tasks: BackgroundTasks,
    session: AsyncSession = Depends(get_async_db),
) -> dict:
    data: dict = json.loads(await request.json())
    logger.debug(f"call ask with data: {data}")

    # TODO: try except
    message = MsgIn(**data)

    if is_answer(message):
        logger.debug(f"message with id {message.message_id} marked as answer.")
        background_tasks.add_task(process_answer, message, session)
    elif is_question(message):
        logger.debug(f"message with id {message.message_id} marked as question.")
        background_tasks.add_task(process_question, message, session)
    else:
        logger.debug(f"message with id {message.message_id} skipped.")

    return {
        "status": "ok",
        "id": 111,  # db_message.id,
    }
