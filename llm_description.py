import os
import requests
import json

API_KEY = os.getenv("OPENROUTER_API_KEY")
print("API KEY:", API_KEY)


def ask_model(prompt: str):
    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json",
    }
    data = {
        "model": "stepfun/step-3.5-flash:free",
                 "messages": [
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.1
    }

    resp = requests.post(url, headers=headers, data=json.dumps(data))
    resp.raise_for_status()
    j = resp.json()
    print("DEBUG RAW RESPONSE:", j)
    return j["choices"][0]["message"]

def get_description(name, author):
    msg = ask_model(f"""Сделай краткую аннотацию к книге «{name}» автора {author}.
                        Пиши строго на русском языке.
                        Аннотация должна состоять из 3–5 предложений и начинаться сразу с сути произведения.
                        Не добавляй вводных фраз, пояснений, справочной информации или комментариев о существовании книги.
                        Не выдумывай факты и не придумывай сюжет.
                        Если книга неизвестна — напиши строго: «Описание недоступно».
                        Не используй другие формулировки.
                        Не используй художественные детали, спойлеры и оценочные суждения.
                        Сосредоточься только на жанре, ключевых темах, конфликте и общем смысле произведения.
                        Стиль — нейтральный, энциклопедический.
                        """)
    return msg["content"]

if __name__ == "__main__":
    print(get_description("Посторонний", "Альбер Камю"))
