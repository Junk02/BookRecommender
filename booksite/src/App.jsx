import React, { useEffect, useRef, useState } from "react";
// Для роутинга
import { useState as useReactState } from "react";
// Минималистичная SVG-звезда (уже есть выше)

// Минималистичная, ровная, мягкая SVG-звезда
function Star({ filled, onClick, className, title }) {
  return (
    <svg
      onClick={onClick}
      className={className}
      width="28"
      height="28"
      viewBox="0 0 28 28"
      fill="none"
      xmlns="http://www.w3.org/2000/svg"
      style={{ cursor: onClick ? 'pointer' : 'default', verticalAlign: 'middle', transition: 'filter 0.18s' }}
      title={title}
    >
      <path
        d="M14 4.5c.38-1.1 1.62-1.1 2 0l2.1 6.1c.16.47.59.8 1.09.83l6.3.45c1.13.08 1.6 1.45.75 2.19l-5 4.2c-.4.34-.56.89-.43 1.4l1.6 6.1c.29 1.11-.91 2-1.85 1.36l-5.2-3.5a1.1 1.1 0 0 0-1.2 0l-5.2 3.5c-.94.64-2.14-.25-1.85-1.36l1.6-6.1c.13-.51-.03-1.06-.43-1.4l-5-4.2c-.85-.74-.38-2.11.75-2.19l6.3-.45c.5-.03.93-.36 1.09-.83L14 4.5z"
        fill={filled ? '#FFD600' : 'none'}
        stroke="#C2B280"
        strokeWidth="1.2"
        style={{ filter: filled ? 'drop-shadow(0 2px 8px #ffe06688)' : 'none', transition: 'filter 0.18s' }}
      />
    </svg>
  );
}

const BOOKS_COUNT = 15;
const DEFAULT_WIDTH = 84;
const DEFAULT_HEIGHT = 110;
const FALLBACK_COVER = "/covers/book1.png";

// ================= CSV PARSER =================
function parseCSV(text) {
  const rows = [];
  const headers = [];
  let currentValue = "";
  let currentRow = [];
  let inQuotes = false;

  for (let i = 0; i < text.length; i++) {
    const char = text[i];
    const next = text[i + 1];

    if (char === '"') {
      if (inQuotes && next === '"') {
        currentValue += '"';
        i++;
      } else {
        inQuotes = !inQuotes;
      }
    } else if ((char === "," || char === ";") && !inQuotes) {
      currentRow.push(currentValue.trim());
      currentValue = "";
    } else if (char === "\n" && !inQuotes) {
      currentRow.push(currentValue.trim());
      currentValue = "";

      if (currentRow.some((value) => value !== "")) {
        rows.push(currentRow);
      }
      currentRow = [];
    } else if (char !== "\r") {
      currentValue += char;
    }
  }

  if (currentValue.length > 0 || currentRow.length > 0) {
    currentRow.push(currentValue.trim());
    rows.push(currentRow);
  }

  if (rows.length === 0) return [];

  const normalizedHeaders = rows[0].map((h) => String(h).toLowerCase());
  return rows.slice(1).map((values) => {
    const row = {};
    normalizedHeaders.forEach((header, index) => {
      row[header] = values[index] ?? "";
    });
    return row;
  });
}

// ================= HELPERS =================
const randomBetween = (min, max) => Math.random() * (max - min) + min;
const clamp = (value, min, max) => Math.min(Math.max(value, min), max);

function pickRandom(arr) {
  return arr[Math.floor(Math.random() * arr.length)];
}

function normalizeBookRow(row) {
  const id = String(row.id ?? "").trim();
  const coverUrl = id
    ? `/covers/book_${id}.jpg`
    : FALLBACK_COVER;

  return {
    id,
    title: row.title || "Без названия",
    author: row.authors || "Неизвестный автор",
    description: row.book_description || "Описание отсутствует.",
    coverUrl,
    width: DEFAULT_WIDTH,
    height: DEFAULT_HEIGHT,
  };
}

// ================= FLOATING ITEM =================
function makeFloatingItem(base, index, total) {
  const direction = index % 2 === 0 ? "book-float--down" : "book-float--up";

  const minX = 6;
  const maxX = 88;
  const baseX =
    total > 1 ? minX + (index / (total - 1)) * (maxX - minX) : 50;

  return {
    ...base,
    slotId: index,
    direction,
    x: `${clamp(baseX + randomBetween(-4, 4), minX, maxX).toFixed(1)}%`,
    delay: `${randomBetween(0, 6).toFixed(2)}s`,
    duration: `${randomBetween(8, 32).toFixed(2)}s`,
    sway: `${randomBetween(-8, 8).toFixed(1)}px`,
    startRotate: `${randomBetween(-10, 10).toFixed(1)}deg`,
    endRotate: `${randomBetween(-8, 8).toFixed(1)}deg`,
  };
}

// ================= APP =================
function App() {
  const [booksData, setBooksData] = useState([]);
  const [floatingBooks, setFloatingBooks] = useState([]);
  const [selectedBook, setSelectedBook] = useState(null);
  const [query, setQuery] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const [searchResults, setSearchResults] = useState([]);
  const [favorites, setFavorites] = useState(() => {
    try {
      return JSON.parse(localStorage.getItem('favorites') || '[]');
    } catch {
      return [];
    }
  });
  const textareaRef = useRef(null);
  // Простая реализация "роутинга" (main/favorites)
  const [page, setPage] = useState('main');
  // Сохранять избранное в localStorage
  useEffect(() => {
    localStorage.setItem('favorites', JSON.stringify(favorites));
  }, [favorites]);

  // Проверка, избранная ли книга
  const isFavorite = (id) => favorites.includes(String(id));

  // Переключить избранное
  const toggleFavorite = (id) => {
    setFavorites((prev) =>
      prev.includes(String(id))
        ? prev.filter((fid) => fid !== String(id))
        : [...prev, String(id)]
    );
  };

  // Resize textarea
  useEffect(() => {
    if (textareaRef.current) {
      textareaRef.current.style.height = "auto";
      textareaRef.current.style.height =
        textareaRef.current.scrollHeight + "px";
    }
  }, [query]);

  // ESC to close modal
  useEffect(() => {
    const handleKeyDown = (event) => {
      if (event.key === 'Escape' && selectedBook) {
        setSelectedBook(null);
      }
    };

    document.addEventListener('keydown', handleKeyDown);
    return () => document.removeEventListener('keydown', handleKeyDown);
  }, [selectedBook]);

  // Load CSV
  useEffect(() => {
    fetch("/books.csv")
      .then((res) => res.text())
      .then((text) => {
        const parsed = parseCSV(text);
        setBooksData(parsed);
      });
  }, []);

  // Init books
  useEffect(() => {
    if (!booksData.length) return;

    const items = Array.from({ length: BOOKS_COUNT }, (_, i) => {
      const book = normalizeBookRow(pickRandom(booksData));
      return makeFloatingItem(book, i, BOOKS_COUNT);
    });

    setFloatingBooks(items);
  }, [booksData]);

  // === ОБНОВЛЁННЫЙ ПОИСК ===
  const handleSearch = async (e) => {
    e.preventDefault();
    
    if (!query.trim()) return;
    
    setIsLoading(true);
    try {
      const response = await fetch("http://localhost:5000/api/search", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ query: query.trim() }),
      });
      
      if (!response.ok) {
        throw new Error("Ошибка при поиске");
      }
      
      const data = await response.json();
      console.log("Ответ сервера:", data);

      // === НОВОЕ: получаем ID и превращаем в книги ===
      if (data.ids && Array.isArray(data.ids)) {
        const foundBooks = data.ids
          .map((id) => booksData.find((b) => String(b.id) === String(id)))
          .filter(Boolean);

        setSearchResults(foundBooks);
      } else {
        setSearchResults([]);
      }

    } catch (error) {
      console.error("Ошибка:", error);
      alert("Не удалось подключиться к серверу. Убедитесь, что бекенд запущен на http://localhost:5000");
    } finally {
      setIsLoading(false);
    }
  };

  // Replace book WITHOUT breaking animation
  const replaceBook = (index) => {
    setFloatingBooks((prev) =>
      prev.map((item, i) =>
        i === index
          ? {
              ...item,
              ...normalizeBookRow(pickRandom(booksData)),
            }
          : item
      )
    );
  };

  // Image fallback
  const handleImageError = (e, id) => {
    const img = e.currentTarget;

    if (!img.dataset.step) {
      img.dataset.step = "1";
      img.src = `/covers/book_${id}.png`;
    } else {
      img.src = FALLBACK_COVER;
    }
  };

  return (
    <div className="page">
      {page === 'main' && (
        <>
          <div className={`background-floating ${selectedBook ? "paused" : ""}`}>
            {floatingBooks.map((book, index) => (
              <div
                key={book.slotId}
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
                onAnimationIteration={() => replaceBook(index)}
                onClick={() => setSelectedBook(book)}
              >
                <img
                  className="book-cover"
                  src={book.coverUrl}
                  alt={book.title}
                  loading="lazy"
                  onError={(e) => handleImageError(e, book.id)}
                />
                <span className="book-tooltip">
                  {book.title}
                  <span className="book-author">{book.author}</span>
                </span>
              </div>
            ))}
          </div>

          <form
            className="search-container"
            onSubmit={handleSearch}
          >
            <textarea
              ref={textareaRef}
              className="search-input"
              value={query}
              onChange={(e) => setQuery(e.target.value)}
              placeholder="Опиши, какие книги ты ищешь..."
              rows={1}
              disabled={isLoading}
            />
            <button className="search-button" disabled={isLoading}>
              {isLoading ? "Поиск..." : "Найти"}
            </button>
          </form>

          {/* Кнопка избранного в правом нижнем углу */}
          <button
            className="favorites-fab"
            onClick={() => setPage('favorites')}
            title="Избранные книги"
          >
            <span className="favorites-fab-center">
              <Star filled={favorites.length > 0} />
            </span>
          </button>

          {selectedBook && (
            <div className="modal-backdrop" onClick={() => setSelectedBook(null)}>
              <div
                className="modal-content"
                onClick={(e) => e.stopPropagation()}
                style={{ position: 'relative' }}
              >
                <button className="modal-close" onClick={() => setSelectedBook(null)}>×</button>
                {/* Кнопка избранного в углу карточки */}
                <span
                  className="star-favorite-modal"
                  onClick={() => toggleFavorite(selectedBook.id)}
                  title={isFavorite(selectedBook.id) ? 'Убрать из избранного' : 'В избранное'}
                >
                  <span className="star-favorite-center">
                    <Star filled={isFavorite(selectedBook.id)} />
                  </span>
                </span>
                <div className="modal-body">
                  <img
                    className="modal-cover"
                    src={selectedBook.coverUrl}
                    onError={(e) => handleImageError(e, selectedBook.id)}
                    alt=""
                  />
                  <div className="modal-info">
                    <h2>{selectedBook.title}</h2>
                    <p className="modal-author">{selectedBook.author}</p>
                    <p className="modal-description">{selectedBook.description}</p>
                    <p className="modal-debug">Обложка: {selectedBook.coverUrl}</p>
                  </div>
                </div>
              </div>
            </div>
          )}

          {searchResults.length > 0 && (
            <div className="search-results-container">
              <div className="search-results-header">
                <h3>Найдено {searchResults.length} книг</h3>
                <button 
                  className="close-results-btn"
                  onClick={() => setSearchResults([])}
                >
                  Закрыть
                </button>
              </div>
              <div className="search-results-grid">
                {searchResults.map((book, index) => {
                  const normalizedBook = normalizeBookRow(book);
                  return (
                    <div
                      key={index}
                      className="search-result-item"
                      style={{
                        animation: `cardAppear 0.4s ease ${index * 0.08}s both`
                      }}
                      onClick={() => setSelectedBook(normalizedBook)}
                    >
                      <img
                        src={normalizedBook.coverUrl}
                        alt={normalizedBook.title}
                        onError={(e) => handleImageError(e, normalizedBook.id)}
                      />
                      <div className="result-info">
                        <p className="result-title">{normalizedBook.title}</p>
                        <p className="result-author">{normalizedBook.author}</p>
                      </div>
                    </div>
                  );
                })}
              </div>
            </div>
          )}
        </>
      )}

      {page === 'favorites' && (
        <div className="favorites-page">
          <button className="favorites-back" onClick={() => setPage('main')} title="Назад на главную">←</button>
          <h2 className="favorites-title">Избранные книги</h2>
          <div className="favorites-count-onpage">В избранном: {favorites.length}</div>
          <div className="favorites-grid">
            {favorites.length === 0 && <div className="favorites-empty">Нет избранных книг</div>}
            {favorites.map(fid => {
              const book = booksData.find(b => String(b.id) === String(fid));
              if (!book) return null;
              const normalizedBook = normalizeBookRow(book);
              return (
                <div
                  key={fid}
                  className="favorites-item"
                  onClick={() => setSelectedBook(normalizedBook)}
                >
                  <img
                    src={normalizedBook.coverUrl}
                    alt={normalizedBook.title}
                    onError={(e) => handleImageError(e, normalizedBook.id)}
                  />
                  <div className="favorites-info">
                    <p className="favorites-title">{normalizedBook.title}</p>
                    <p className="favorites-author">{normalizedBook.author}</p>
                  </div>
                </div>
              );
            })}
          </div>
          {/* Модалка для книги из избранного */}
          {selectedBook && (
            <div className="modal-backdrop" onClick={() => setSelectedBook(null)}>
              <div
                className="modal-content"
                onClick={(e) => e.stopPropagation()}
                style={{ position: 'relative' }}
              >
                <button className="modal-close" onClick={() => setSelectedBook(null)}>×</button>
                {/* Кнопка избранного в углу карточки */}
                <span
                  className="star-favorite-modal"
                  onClick={() => toggleFavorite(selectedBook.id)}
                  title={isFavorite(selectedBook.id) ? 'Убрать из избранного' : 'В избранное'}
                >
                  <Star filled={isFavorite(selectedBook.id)} />
                </span>
                <div className="modal-body">
                  <img
                    className="modal-cover"
                    src={selectedBook.coverUrl}
                    onError={(e) => handleImageError(e, selectedBook.id)}
                    alt=""
                  />
                  <div className="modal-info">
                    <h2>{selectedBook.title}</h2>
                    <p className="modal-author">{selectedBook.author}</p>
                    <p className="modal-description">{selectedBook.description}</p>
                    <p className="modal-debug">Обложка: {selectedBook.coverUrl}</p>
                  </div>
                </div>
              </div>
            </div>
          )}
        </div>
      )}
    </div>
  );
}

export default App;
