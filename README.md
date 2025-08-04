# 📊 Stock Tracker API

This is a simple Django REST API for tracking stock prices using Celery and JWT authentication.

## 🚀 Features
- User authentication (JWT)
- Fetch stock price by symbol (real-time from external API)
- Auto-updating prices via Celery
- API to list/view all tracked stocks
- To access the API doc go to  `base_link/docs/`


## ⚙️ Tech Stack
- Django
- Django REST Framework
- Celery + Redis
- SimpleJWT
- PostgreSQL

## 🔐 Authentication

Use `/api/accounts/register/` then `/api/accounts/login/` to get your JWT access and refresh tokens.

## 📈 API Endpoints

| Method | Endpoint | Description | Auth |
|--------|----------|-------------|------|
| GET | `/api/stocks/` | List all stocks | ✅ |
| GET | `/api/stocks/<id>/` | Get stock detail | ✅ |
| GET | `/api/stocks/fetch-symbol/?symbol=TSLA` | Fetch or add stock by symbol | ✅ |
| POST | `/api/accounts/register/` | To register a user | ❌ |
| POST | `/api/token/login/` | To Log in | ❌ |



## 🔔 Alerts Endpoints

| Method | Endpoint | Description | Auth |
|--------|----------|-------------|------|
| GET | `/api/alerts/` | List all your alerts | ✅ |
| POST | `/api/alerts/` | Create new alert | ✅ |
| GET/PUT/DELETE | `/api/alerts/<id>/` | View, update or delete specific alert | ✅ |

### Creating an Alert (POST `/api/alerts/`)
```json
{
    "stock": "AAPL",
    "condition": "above",
    "target_price": 150.00
}
```
### Required Fields:
- stock: Stock symbol (string)
- condition: "gt" for greater than or "lt" for less than
- target_price: Price threshold (decimal)
- duration_minutes: number of minutes and it is OPTIONAL (integer)

### Notes:
- Alerts are user-specific
- user field is automatically set
- Use condition "above" or "below" target price


## 📥 Setup (Local)

```bash
git clone https://github.com/ehabahmed2/stock_tracker
cd stock_tracker
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# configure .env file with DB and API key

python manage.py migrate
python manage.py runserver
```
## 📚 API Documentation
- Access interactive API docs at: base_url/docs/