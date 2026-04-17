from flask import Flask, request, jsonify
from flask_cors import CORS
import csv
from pathlib import Path

from get_query_embedding_description import get_query_description
from get_embedding import get_embedding
from find_similar import find_similar_books


app = Flask(__name__)
CORS(app)

books_data = []


def load_books_csv():
    """Загружает данные книг из CSV файла"""
    global books_data
    csv_path = Path(__file__).parent / "books_clean_stage3.csv"

    try:
        with open(csv_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            books_data = list(reader)
            print(f"Загружено книг: {len(books_data)}")
    except Exception as e:
        print(f"Ошибка загрузки CSV: {e}")
        books_data = []


@app.route('/api/search', methods=['POST'])
def api_search():
    """API endpoint для поиска книг"""
    try:
        data = request.get_json()
        query = data.get('query', '').strip()

        if not query:
            return jsonify({'error': 'Запрос пуст'}), 400

        # --- НОВОЕ: получаем структурированное описание запроса ---
        structured = get_query_description(query)
        embedding = get_embedding(structured)

        print("\n=== Структурированное описание запроса ===")
        print(structured)
        print("==========================================\n")

        print("=== Эмбеддинг запроса ===")
        print(embedding[:10], "...")  # первые 10 чисел
        print("Размер:", len(embedding))
        print("==========================")

        top_ids = find_similar_books("books.csv", embedding, top_k=10)
        print("ids: ", top_ids)

        return jsonify({
            "query": query,
            "structured_query": structured,
            "ids": top_ids
        })

    except Exception as e:
        print(f"Ошибка в api_search: {e}")
        return jsonify({'error': str(e)}), 500


@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({
        'status': 'ok',
        'books_loaded': len(books_data)
    })


if __name__ == '__main__':
    print("Запуск backend...")
    load_books_csv()
    app.run(debug=True, port=5000)
