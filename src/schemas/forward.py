from pydantic import BaseModel


class MsgForward(BaseModel):
    chat_id: int | str
    # Unique identifier for the target chat or username of the target channel (in the format @channelusername)
    from_chat_id: int | str
    # Unique identifier for the chat where the original message was sent
    # (or channel username in the format @channelusername)
    message_id: int
    # Message identifier in the chat specified in from_chat_id
    message_thread_id: int | None = None
    # Unique identifier for the target message thread (topic) of the forum; for forum supergroups only
    disable_notification: bool | None = None
    # Sends the message silently. Users will receive a notification with no sound.
    protect_content: bool | None = None
    # Protects the contents of the forwarded message from forwarding and saving
