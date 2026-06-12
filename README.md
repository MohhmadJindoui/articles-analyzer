# Articles Analyzer

מערכת לניתוח מאמרי קוד פתוח בתחומי ביטחון, סייבר וגיאופוליטיקה.

## הרצה מהירה
docker compose up --build

## Dashboard
פתח את frontend/index.html בדפדפן

## ניתוחים ב-Dashboard
1. מאמרים לפי מקור
2. התפלגות לפי קטגוריה  
3. מאמרים לפי שפה
4. מגמות לאורך זמן
5. ענן תגיות

## הגדרת MindsDB
פתח http://localhost:47334 והרץ בסדר:

שלב 1 - חיבור PostgreSQL:
CREATE DATABASE articles_postgres WITH ENGINE = 'postgres',
PARAMETERS = {"host":"articles-db","port":5432,
"database":"articles_db","user":"admin","password":"password123"};

שלב 2 - Groq Engine:
CREATE ML_ENGINE groq_engine FROM groq USING api_key = 'YOUR_GROQ_KEY';

שלב 3 - AI Model:
CREATE MODEL mindsdb.articles_model PREDICT answer
USING engine='groq_engine', model_name='llama-3.1-8b-instant',
prompt_template='Answer this question about security articles: {{question}}';

## שאילתות לדוגמה
- What are the main cyber threats?
- Which sources published the most articles?
- What are the key articles about Iran?
- Is there an increase in cyber articles?
## API Endpoints

| Method | Endpoint |
|--------|----------|
| GET | /api/stats/total |
| GET | /api/stats/by-source |
| GET | /api/stats/by-category |
| GET | /api/stats/by-language |
| GET | /api/stats/by-date |
| GET | /api/stats/wordcloud |
| GET | /api/articles |
| POST | /api/chat |
## מבנה הפרויקט

| קובץ | תיאור |
|------|-------|
| docker-compose.yml | הגדרות Docker |
| backend/main.py | FastAPI - כל ה-endpoints |
| data-loader/loader.py | טעינת CSV ל-PostgreSQL |
| frontend/index.html | מבנה ה-Dashboard |
| frontend/style.css | עיצוב |
| frontend/charts.js | גרפים וסטטיסטיקות |
| frontend/chat.js | ממשק AI Chat |


## 🎥 הקלטת Dashboard
[לחץ כאן לצפייה בסרטון](https://drive.google.com/file/d/1UNU69rjZ0GVjOdgN4_hRgdZo3mVPEOHX/view?usp=sharing)

הסרטון מדגים:
- ניתוחי ה-Dashboard (5 גרפים)
- ענן התגיות
- שאילתות AI Agent (MindsDB + Groq)

## פרטי הגשה
קורס: ארכיטקטורת מערכות תוכנה
מכללה: מכללת עמק יזרעאל
תרגיל: מספר 2
