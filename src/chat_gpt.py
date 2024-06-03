import logging

import openai
from openai import APIError
from openai.types.chat import ChatCompletionUserMessageParam

from settings import settings

openai.api_key = settings.OPENAI_API_KEY
openai.base_url = "https://api.vsegpt.ru/v1/"

logger = logging.getLogger(__name__)


def is_call_to_operator(text: str) -> bool:
    prompt = f"""
    Определи, содержит ли фрагмент текста требование продолжить общение только с оператором/человеком,
    а не ботом или искусственным интеллектом.
    Фрагмент: '{text}'.
    Ответ сформулируй в виде да или нет.
    """

    messages = [
        ChatCompletionUserMessageParam(role="user", content=prompt),
    ]

    logger.info(f"Send query to gpt: {prompt}")
    try:
        response = openai.chat.completions.create(
            # id модели из списка моделей - можно использовать OpenAI, Anthropic и пр.
            model="anthropic/claude-instant-v1",
            messages=messages,
            temperature=0.7,
            n=1,
            # Максимальное число ВЫХОДНЫХ токенов. Для большинства моделей не должно превышать 4096
            max_tokens=3000,
            # опционально - передача информация об источнике API-вызова
            extra_headers={"X-Title": "python RTNO task"},
        )

        logger.debug(f"Response: {response}")
        result = response.choices[0].message.content
        logger.info(f"Result: {result}")
        return result == "да"
    except APIError:
        return False
