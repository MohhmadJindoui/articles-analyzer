# Articles Analyzer

## Overview

Articles Analyzer is a full-stack web application developed as part of a Software Architecture course.

The platform analyzes open-source articles related to cybersecurity, defense, and geopolitics. It provides interactive dashboards, statistical insights, and an AI-powered assistant for querying article data.

---

## Technologies

- Python
- FastAPI
- PostgreSQL
- SQLAlchemy
- Docker
- Docker Compose
- HTML
- CSS
- JavaScript
- MindsDB
- Groq API (Llama 3.1)

---

## Main Features

- Import articles into PostgreSQL
- Interactive analytics dashboard
- Article statistics by:
  - Source
  - Category
  - Language
  - Publication date
- Word cloud generation
- AI-powered question answering
- RESTful API
- Dockerized deployment

---

## Dashboard

The dashboard provides:

- Articles by source
- Articles by category
- Articles by language
- Timeline analysis
- Word cloud visualization

---

## REST API

| Method | Endpoint |
|---------|----------|
| GET | /api/stats/total |
| GET | /api/stats/by-source |
| GET | /api/stats/by-category |
| GET | /api/stats/by-language |
| GET | /api/stats/by-date |
| GET | /api/stats/wordcloud |
| GET | /api/articles |
| POST | /api/chat |

---

## Project Structure

---

## Demo

Dashboard demonstration:

https://drive.google.com/file/d/1UNU69rjZ0GVjOdgN4_hRgdZo3mVPEOHX/view

---

## Learning Objectives

This project demonstrates practical experience with:

- Backend development using FastAPI
- Database design with PostgreSQL
- REST API development
- Docker containerization
- Data visualization
- AI integration using MindsDB and Groq
- Full-stack web development
