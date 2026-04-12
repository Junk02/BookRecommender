import React, { useState, useRef, useEffect } from "react";

const floatingBooks = [
  { id: 1, title: "Лабиринты слов", author: "И. Лермонов", short: "ЛС" },
  { id: 2, title: "Код для книжного клуба", author: "М. Соловьев", short: "КК" },
  { id: 3, title: "Сказки на ночь", author: "О. Ветрова", short: "СН" },
  { id: 4, title: "Путешествие по страницам", author: "А. Белова", short: "ПП" },
  { id: 5, title: "Фантазия и реальность", author: "Е. Холмова", short: "ФР" },
  { id: 6, title: "Тихие истории", author: "Н. Цветкова", short: "ТИ" },
  { id: 7, title: "Осенний читатель", author: "Р. Соловьева", short: "ОЧ" },
  { id: 8, title: "Магия страниц", author: "В. Ладыгин", short: "МП" },
  { id: 9, title: "Магия страниц", author: "В. Ладыгин", short: "МП" },
  { id: 10, title: "Магия страниц", author: "В. Ладыгин", short: "МП" },
  { id: 11, title: "Магия страниц", author: "В. Ладыгин", short: "МП" },
];

function App() {
  const [query, setQuery] = useState("");
  const textareaRef = useRef(null);

  const resizeTextarea = (textarea) => {
    if (!textarea) return;
    textarea.style.height = "auto";
    textarea.style.height = `${textarea.scrollHeight}px`;
  };

  useEffect(() => {
    resizeTextarea(textareaRef.current);
  }, [query]);

  const handleInput = (e) => {
    setQuery(e.target.value);
    resizeTextarea(e.target);
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    if (!query.trim()) return;

    console.log("Поиск:", query);
  };

  return (
    <div className="page">
      <div className="background-floating">
        {floatingBooks.map((book, index) => {
          const directionClass = index % 2 === 0 ? "book-float--down" : "book-float--up";
          return (
            <div
              key={book.id}
              className={`book-float ${directionClass}`}
              style={{
                "--x": `${12 + (index * 10) % 76}%`,
                "--delay": `${(index * 1.1) % 5}s`,
                "--duration": `${12 + (index * 2)}s`,
              }}
              title={`${book.title} — ${book.author}`}
            >
              <span className="book-cover">📘</span>
              <span className="book-tooltip">
                {book.title}
                <span className="book-author">{book.author}</span>
              </span>
            </div>
          );
        })}
      </div>

      <form className="search-container" onSubmit={handleSubmit}>
        <textarea
          ref={textareaRef}
          className="search-input"
          placeholder="Опиши, какие книги ты ищешь..."
          value={query}
          onChange={handleInput}
          rows={1}
        />

        <button className="search-button" type="submit">
          Найти
        </button>
      </form>
    </div>
  );
}

export default App;
