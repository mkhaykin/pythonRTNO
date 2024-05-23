from aiogram.types import (
    ForceReply,
    InlineKeyboardMarkup,
    LinkPreviewOptions,
    Message,
    MessageEntity,
    ReplyKeyboardMarkup,
    ReplyKeyboardRemove,
    ReplyParameters,
)
from pydantic import BaseModel


class MsgIn(Message):
    pass


class MsgOut(BaseModel):
    chat_id: int | str
    text: str
    message_thread_id: int | None = None
    parse_mode: str | None = "HTML"
    entities: list[MessageEntity] | None = None
    link_preview_options: LinkPreviewOptions | None = None
    disable_notification: bool | None = None
    protect_content: bool | None = False
    reply_parameters: ReplyParameters | None = None
    reply_markup: None | (
        InlineKeyboardMarkup | ReplyKeyboardMarkup | ReplyKeyboardRemove | ForceReply
    ) = None
    allow_sending_without_reply: bool | None = None
    disable_web_page_preview: bool | None = None
    reply_to_message_id: int | None = None
    request_timeout: int | None = None
