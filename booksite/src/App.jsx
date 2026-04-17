import React, { useEffect, useRef, useState } from "react";

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
  const textareaRef = useRef(null);

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

      {selectedBook && (
        <div className="modal-backdrop" onClick={() => setSelectedBook(null)}>
          <div
            className="modal-content"
            onClick={(e) => e.stopPropagation()}
          >
            <button className="modal-close" onClick={() => setSelectedBook(null)}>×</button>

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
    </div>
  );
}

export default App;
