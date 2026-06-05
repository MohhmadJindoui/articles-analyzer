import pandas as pd
from sqlalchemy import create_engine, text
import os
import re
import nltk
from nltk.corpus import stopwords

nltk.download('stopwords', quiet=True)
nltk.download('punkt', quiet=True)

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://admin:password123@localhost:5432/articles_db")
engine = create_engine(DATABASE_URL)

def clean_text(text):
    if not isinstance(text, str):
        return ""
    text = text.lower()
    text = re.sub(r'[^\w\s]', '', text)
    stop_words = set(stopwords.words('english'))
    words = text.split()
    words = [w for w in words if w not in stop_words]
    return " ".join(words)

def load_csv(filepath):
    print(f"Loading file: {filepath}")
    df = pd.read_csv(filepath)
    
    print(f"Found {len(df)} articles")
    print(f"Columns: {list(df.columns)}")
    
    # נרמול שמות עמודות
    df.columns = df.columns.str.lower().str.strip()
    
    # ניקוי טקסט
    if 'content' in df.columns:
        df['content'] = df['content'].apply(clean_text)
    if 'summary' in df.columns:
        df['summary'] = df['summary'].apply(clean_text)
    
    # המרת תאריכים
    if 'published_date' in df.columns:
        df['published_date'] = pd.to_datetime(df['published_date'], errors='coerce').dt.date
    if 'collected_date' in df.columns:
        df['collected_date'] = pd.to_datetime(df['collected_date'], errors='coerce').dt.date
    
    # טעינה ל-PostgreSQL
    df.to_sql('articles', engine, if_exists='append', index=False)
    print(f"Successfully loaded {len(df)} articles to database!")

def create_sample_csv():
    """יוצר קובץ CSV לדוגמה אם אין קובץ אמיתי"""
    sample_data = {
        'title': [
            'Iran Expands Cyber Operations Against NATO',
            'Russia Military Budget Increases 40%',
            'China AI Military Applications 2024',
            'Hamas Cyber Unit Analysis',
            'NATO Defense Strategy Update',
            'Hezbollah Communication Networks',
            'US Cybersecurity Infrastructure Report',
            'Israel Iron Dome Technology Advances',
        ],
        'url': [
            'https://example.com/1',
            'https://example.com/2',
            'https://example.com/3',
            'https://example.com/4',
            'https://example.com/5',
            'https://example.com/6',
            'https://example.com/7',
            'https://example.com/8',
        ],
        'source': ['Reuters', 'BBC', 'CNN', 'Haaretz', 'Reuters', 'BBC', 'CNN', 'Times of Israel'],
        'author': ['John Smith', 'Jane Doe', 'Bob Johnson', 'Sarah Cohen', 
                   'Mike Davis', 'Anna Lee', 'Tom Brown', 'David Levy'],
        'published_date': [
            '2024-01-15', '2024-01-14', '2024-01-13', '2024-01-12',
            '2024-01-11', '2024-01-10', '2024-01-09', '2024-01-08',
        ],
        'collected_date': ['2024-01-16'] * 8,
        'language': ['en', 'en', 'en', 'he', 'en', 'en', 'en', 'en'],
        'category': ['cyber', 'military', 'ai', 'cyber', 'defense', 'geopolitics', 'cyber', 'defense'],
        'summary': [
            'Iran has expanded its cyber operations targeting NATO infrastructure',
            'Russia announced significant increase in military spending',
            'China develops AI applications for military use',
            'Analysis of Hamas cyber capabilities and operations',
            'NATO updates its defense strategy for 2024',
            'Investigation of Hezbollah communication networks',
            'US report on critical cybersecurity infrastructure',
            'Latest advances in Iron Dome missile defense system',
        ],
        'content': [
            'Full article about Iran cyber operations targeting NATO member states...',
            'Full article about Russian military budget and spending priorities...',
            'Full article about Chinese artificial intelligence military programs...',
            'Full article about Hamas cyber unit operations and capabilities...',
            'Full article about NATO defense strategy updates and changes...',
            'Full article about Hezbollah communication network analysis...',
            'Full article about US cybersecurity infrastructure vulnerabilities...',
            'Full article about Iron Dome system improvements and success rates...',
        ],
        'tags': [
            'iran;cyber;nato;espionage',
            'russia;military;budget;defense',
            'china;ai;military;technology',
            'hamas;cyber;gaza;operations',
            'nato;defense;strategy;alliance',
            'hezbollah;lebanon;communications;network',
            'usa;cybersecurity;infrastructure;policy',
            'israel;iron-dome;defense;missile',
        ]
    }
    
    df = pd.DataFrame(sample_data)
    df.to_csv('/data/sample_articles.csv', index=False)
    print("Sample CSV created at /data/sample_articles.csv")
    return '/data/sample_articles.csv'

if __name__ == "__main__":
    import time
    print("Waiting for database to be ready...")
    time.sleep(10)
    
    filepath = '/data/articles.csv'
    
    if not os.path.exists(filepath):
        print("No articles.csv found, creating sample data...")
        filepath = create_sample_csv()
    
    load_csv(filepath)