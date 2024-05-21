import openai
from openai.types.chat import ChatCompletionUserMessageParam

from settings import settings

openai.api_key = settings.OPENAI_API_KEY
openai.base_url = "https://api.vsegpt.ru/v1/"

prompt = """
Определи, содержит ли фрагмент текста требование продолжить общение только с оператором/человеком,
а не ботом или искусственным интеллектом.
Фрагмент: 'Подскажи к кому мне обратиться за помощью?'.
Ответ сформулируй в виде да или нет.
"""

messages = [
    ChatCompletionUserMessageParam(role="user", content=prompt),
]

response_big = openai.chat.completions.create(
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

print("Response BIG:", response_big)
response = response_big.choices[0].message.content
print("Response:", response)
