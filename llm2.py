from groq import Groq
import sys

# Гарантируем UTF‑8 вывод
sys.stdout.reconfigure(encoding='utf-8')

client = Groq()


def get_book_description(title: str, authors: str = "", description: str = "") -> str:
    prompt = f"""
Ты — система, которая пишет краткие, точные, нейтральные описания книг для карточек в каталоге.

Требования к описанию:
- 3-5 предложений.
- Никаких спойлеров, раскрытия концовки или ключевых сюжетных поворотов.
- Никаких оценочных суждений ("великая книга", "интересный роман").
- Никакой художественности, только информативный пересказ.
- Стиль: спокойный, нейтральный, как аннотация в книжном магазине.
- Не придумывай фактов, которых нет в общедоступных описаниях.
- Если информации мало, пиши максимально обобщённо.

Данные о книге:
Название: «{title}»
Автор: {authors}

Дополнительная структурная информация (используй только как контекст, не пересказывай её напрямую):
{description}

Сгенерируй итоговое описание (3-5 предложений).
"""

    try:
        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            # llama-3.3-70b-versatile
            # meta-llama/llama-4-scout-17b-16e-instruct
            # llama-3.1-8b-instant
            messages=[{"role": "user", "content": prompt}],
            temperature=0.1,
            max_completion_tokens=300,
            top_p=1,
            stream=False
        )

        text = completion.choices[0].message.content.strip()

        # нормализация
        if not text or len(text) < 10:
            return "Описание недоступно"

        if "описание недоступно" in text.lower():
            return "Описание недоступно"

        return text

    except Exception as e:
        # безопасный вывод ошибки
        print("LLM ERROR:", str(e).encode("utf-8", "ignore").decode("utf-8"))
        return "Описание недоступно"
