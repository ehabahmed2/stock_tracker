# 📊 Stock Tracker API

This is a simple Django REST API for tracking stock prices using Celery and JWT authentication.

## 🚀 Features
- User authentication (JWT)
- Fetch stock price by symbol (real-time from external API)
- Auto-updating prices via Celery
- API to list/view all tracked stocks

## ⚙️ Tech Stack
- Django
- Django REST Framework
- Celery + Redis
- SimpleJWT
- PostgreSQL

## 🔐 Authentication

Use `/api/token/` to get your JWT access and refresh tokens.

## 📈 API Endpoints

| Method | Endpoint | Description | Auth |
|--------|----------|-------------|------|
| GET | `/api/stocks/` | List all stocks | ✅ |
| GET | `/api/stocks/<id>/` | Get stock detail | ✅ |
| GET | `/api/stocks/fetch-symbol/?symbol=TSLA` | Fetch or add stock by symbol | ✅ |
| POST | `/api/token/` | Get access + refresh tokens | ❌ |
| POST | `/api/token/refresh/` | Refresh access token | ❌ |

## 📥 Setup (Local)

```bash
git clone ...
cd project
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# configure .env file with DB and API key

python manage.py migrate
python manage.py runserver
```
