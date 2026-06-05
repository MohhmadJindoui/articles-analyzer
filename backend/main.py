from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import create_engine, text
import os
import re
import httpx
from collections import Counter

app = FastAPI(title="Articles Analyzer API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://admin:password123@localhost:5432/articles_db"
)
engine = create_engine(DATABASE_URL)


def init_db():
    with engine.connect() as conn:
        conn.execute(text("""
            CREATE TABLE IF NOT EXISTS articles (
                id SERIAL PRIMARY KEY,
                title TEXT NOT NULL,
                url TEXT,
                source VARCHAR(255),
                author VARCHAR(255),
                published_date DATE,
                collected_date DATE DEFAULT CURRENT_DATE,
                language VARCHAR(10),
                category VARCHAR(100),
                summary TEXT,
                content TEXT,
                tags TEXT,
                created_at TIMESTAMP DEFAULT NOW()
            )
        """))
        conn.execute(text(
            "CREATE INDEX IF NOT EXISTS idx_source ON articles(source)"
        ))
        conn.execute(text(
            "CREATE INDEX IF NOT EXISTS idx_category ON articles(category)"
        ))
        conn.execute(text(
            "CREATE INDEX IF NOT EXISTS idx_published_date ON articles(published_date)"
        ))
        conn.execute(text(
            "CREATE INDEX IF NOT EXISTS idx_language ON articles(language)"
        ))
        conn.commit()


@app.on_event("startup")
async def startup():
    init_db()


@app.get("/")
def root():
    return {"status": "Articles Analyzer API is running!"}


@app.get("/api/stats/total")
def total_articles():
    with engine.connect() as conn:
        result = conn.execute(text("SELECT COUNT(*) FROM articles"))
        count = result.scalar()
    return {"total": count}


@app.get("/api/stats/by-source")
def by_source():
    with engine.connect() as conn:
        result = conn.execute(text("""
            SELECT source, COUNT(*) as count
            FROM articles
            WHERE source IS NOT NULL
            GROUP BY source
            ORDER BY count DESC
            LIMIT 10
        """))
        rows = [{"source": r[0], "count": r[1]} for r in result]
    return rows


@app.get("/api/stats/by-category")
def by_category():
    with engine.connect() as conn:
        result = conn.execute(text("""
            SELECT category, COUNT(*) as count
            FROM articles
            WHERE category IS NOT NULL
            GROUP BY category
            ORDER BY count DESC
        """))
        rows = [{"category": r[0], "count": r[1]} for r in result]
    return rows


@app.get("/api/stats/by-language")
def by_language():
    with engine.connect() as conn:
        result = conn.execute(text("""
            SELECT language, COUNT(*) as count
            FROM articles
            WHERE language IS NOT NULL
            GROUP BY language
            ORDER BY count DESC
        """))
        rows = [{"language": r[0], "count": r[1]} for r in result]
    return rows


@app.get("/api/stats/by-date")
def by_date():
    with engine.connect() as conn:
        result = conn.execute(text("""
            SELECT published_date, COUNT(*) as count
            FROM articles
            WHERE published_date IS NOT NULL
            GROUP BY published_date
            ORDER BY published_date DESC
            LIMIT 30
        """))
        rows = [{"date": str(r[0]), "count": r[1]} for r in result]
    return rows


@app.get("/api/stats/wordcloud")
def wordcloud():
    with engine.connect() as conn:
        result = conn.execute(text("""
            SELECT title, content, tags FROM articles LIMIT 500
        """))
        rows = result.fetchall()

    import nltk
    from nltk.corpus import stopwords
    nltk.download('stopwords', quiet=True)

    stop_words = set(stopwords.words('english'))
    word_freq = Counter()

    for row in rows:
        text_combined = " ".join(filter(None, [row[0], row[1], row[2]]))
        words = re.findall(r'\b[a-zA-Z]{3,}\b', text_combined.lower())
        words = [w for w in words if w not in stop_words]
        word_freq.update(words)

    top_words = [
        {"word": w, "count": c}
        for w, c in word_freq.most_common(50)
    ]
    return top_words


@app.get("/api/articles")
def get_articles(limit: int = 20, offset: int = 0):
    with engine.connect() as conn:
        result = conn.execute(text("""
            SELECT id, title, source, category, language, published_date, url
            FROM articles
            ORDER BY published_date DESC
            LIMIT :limit OFFSET :offset
        """), {"limit": limit, "offset": offset})
        rows = [dict(r._mapping) for r in result]
    return rows

@app.post("/api/chat")
async def chat(request: dict):
    question = request.get("question", "")
    try:
        async with httpx.AsyncClient(timeout=30) as client:
            res = await client.post(
                "http://mindsdb:47334/api/sql/query",
                json={
                    "query": f"SELECT answer FROM mindsdb.articles_model WHERE question = '{question}'"
                }
            )
            data = res.json()
            if data.get("type") == "table" and data.get("data"):
                answer = data["data"][0][0]
            else:
                answer = "No answer"
            return {"answer": answer}
    except Exception as e:
        return {"answer": f"Error: {str(e)}"}