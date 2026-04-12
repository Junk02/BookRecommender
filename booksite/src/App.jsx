import React, { useState, useRef, useEffect } from "react";

const floatingBooks = [
  {
    id: 1,
    title: "Лабиринты слов",
    author: "И. Лермонов",
    coverUrl: "/covers/book1.png",
    width: 84,
    height: 110,
  },
  { id: 2, title: "Код для книжного клуба", author: "М. Соловьев", coverUrl: "/covers/book1.png", width: 84, height: 110 },
  { id: 3, title: "Сказки на ночь", author: "О. Ветрова", coverUrl: "/covers/book1.png", width: 84, height: 110 },
  { id: 4, title: "Путешествие по страницам", author: "А. Белова", coverUrl: "/covers/book1.png", width: 84, height: 110 },
  { id: 5, title: "Фантазия и реальность", author: "Е. Холмова", coverUrl: "/covers/book1.png", width: 84, height: 110 },
  { id: 6, title: "Тихие истории", author: "Н. Цветкова", coverUrl: "/covers/book1.png", width: 84, height: 110 },
  { id: 7, title: "Осенний читатель", author: "Р. Соловьева", coverUrl: "/covers/book1.png", width: 84, height: 110 },
  { id: 8, title: "Магия страниц", author: "В. Ладыгин", coverUrl: "/covers/book1.png", width: 84, height: 110 },
  { id: 9, title: "Заколдованный том", author: "С. Орлова", coverUrl: "/covers/book1.png", width: 84, height: 110 },
  { id: 10, title: "Новые горизонты", author: "Т. Иванов", coverUrl: "/covers/book1.png", width: 84, height: 110 },
  { id: 11, title: "Вечерние рассказы", author: "Л. Иванова", coverUrl: "/covers/book1.png", width: 84, height: 110 },
  { id: 12, title: "Путеводитель по мирам", author: "С. Мороз", coverUrl: "/covers/book1.png", width: 84, height: 110 },
  { id: 13, title: "Тайна древних страниц", author: "К. Зорькин", coverUrl: "/covers/book1.png", width: 84, height: 110 },
  { id: 14, title: "Читающий город", author: "Е. Дворова", coverUrl: "/covers/book1.png", width: 84, height: 110 },
  { id: 15, title: "Ночное перо", author: "Р. Петухов", coverUrl: "/covers/book1.png", width: 84, height: 110 },
];

const randomBetween = (min, max) => Math.random() * (max - min) + min;
const clamp = (value, min, max) => Math.min(Math.max(value, min), max);

const floatingBookItems = floatingBooks.map((book, index) => {
  const direction = index % 2 === 0 ? "book-float--down" : "book-float--up";
  const minX = 6;
  const maxX = 88;
  const baseX = minX + (index / (floatingBooks.length - 1)) * (maxX - minX);
  const x = `${clamp(baseX + randomBetween(-4, 4), minX, maxX).toFixed(1)}%`;
  const delay = `${randomBetween(0, 6).toFixed(2)}s`;
  const duration = `${randomBetween(8, 32).toFixed(2)}s`;
  const sway = `${randomBetween(-8, 8).toFixed(1)}px`;
  const startRotate = `${randomBetween(-10, 10).toFixed(1)}deg`;
  const endRotate = `${randomBetween(-8, 8).toFixed(1)}deg`;

  return {
    ...book,
    direction,
    x,
    delay,
    duration,
    sway,
    startRotate,
    endRotate,
    width: book.width,
    height: book.height,
  };
});

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
        {floatingBookItems.map((book) => (
          <div
            key={book.id}
            className={`book-float ${book.direction}`}
            style={{
              "--x": book.x,
              "--delay": book.delay,
              "--duration": book.duration,
              "--sway": book.sway,
              "--start-rotate": book.startRotate,
              "--end-rotate": book.endRotate,
              "--width": `${book.width}px`,
              "--height": `${book.height}px`,
            }}
            title={`${book.title} — ${book.author}`}
          >
            {book.coverUrl ? (
              <img
                className="book-cover"
                src={book.coverUrl}
                alt={book.title}
                loading="lazy"
              />
            ) : (
              <span
                className="book-cover"
                style={{
                  width: `${book.width}px`,
                  height: `${book.height}px`,
                  fontSize: `${Math.min(book.width, book.height) * 0.4}px`,
                }}
              >
                📘
              </span>
            )}
            <span className="book-tooltip">
              {book.title}
              <span className="book-author">{book.author}</span>
            </span>
          </div>
        ))}
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
