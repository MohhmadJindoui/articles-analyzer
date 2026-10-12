# Articles Analyzer

A full-stack web application developed as part of a **Software Architecture** course.

Articles Analyzer provides interactive analytics for open-source articles covering cybersecurity, defense, and geopolitics. The application combines data visualization, REST APIs, and an AI-powered assistant for exploring article data.

## Technologies

| Category | Technologies |
|---|---|
| Backend | Python, FastAPI, SQLAlchemy |
| Frontend | HTML, CSS, JavaScript |
| Database | PostgreSQL |
| AI Integration | MindsDB, Groq API (Llama 3.1) |
| Containerization | Docker, Docker Compose |

## Key Features

- Import and store article data in PostgreSQL.
- Explore article statistics through an interactive dashboard.
- Analyze articles by source, category, language, and publication date.
- Visualize keyword patterns using a word cloud.
- Query article data through an AI-powered assistant.
- Access analytics and article information through REST APIs.
- Run containerized application components using Docker Compose.

## Dashboard

The analytics dashboard includes:

- Article distribution by source
- Article distribution by category
- Article distribution by language
- Publication timeline analysis
- Word cloud visualization

## REST API

| Method | Endpoint | Description |
|---|---|---|
| GET | `/api/stats/total` | Retrieve total article statistics |
| GET | `/api/stats/by-source` | Article distribution by source |
| GET | `/api/stats/by-category` | Article distribution by category |
| GET | `/api/stats/by-language` | Article distribution by language |
| GET | `/api/stats/by-date` | Article statistics by publication date |
| GET | `/api/stats/wordcloud` | Retrieve word cloud data |
| GET | `/api/articles` | Retrieve article data |
| POST | `/api/chat` | Submit questions to the AI assistant |

## Project Structure

```text
articles-analyzer/
├── backend/
├── data-loader/
├── frontend/
├── docker-compose.yml
├── test_mindsdb.py
└── README.md
```

**Component overview**

- `backend/` — Backend application and API implementation.
- `data-loader/` — Article data import components.
- `frontend/` — User interface and dashboard.
- `docker-compose.yml` — Container service configuration.
- `test_mindsdb.py` — MindsDB integration test script.

## Getting Started

The project uses Docker Compose to manage its containerized services.

Before running the application, review `docker-compose.yml` and configure the required database connection settings and AI integration credentials.

The MindsDB and Groq integrations may require separate configuration.

Detailed setup commands and environment variables should be verified against the project configuration before use.

## Demo

Watch the dashboard demonstration:

[Articles Analyzer — Video Demo](https://drive.google.com/file/d/1UNU69rjZ0GVjOdgN4_hRgdZo3mVPEOHX/view)

## Learning Outcomes

This academic project demonstrates practical experience in:

- Backend development with FastAPI
- Relational database integration using PostgreSQL
- REST API design and implementation
- Docker-based containerization
- Interactive data visualization
- AI integration using MindsDB and Groq
- Full-stack web application development
