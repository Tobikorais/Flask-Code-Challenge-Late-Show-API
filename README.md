# Late Show API Challenge

## Overview
A Flask REST API for a Late Night TV show system using PostgreSQL, JWT authentication, and MVC architecture.

## 🛠 Setup

### 1. Clone and Install Dependencies
```bash
git clone https://github.com/your-username/late-show-api-challenge.git
cd late-show-api-challenge
pipenv install flask flask_sqlalchemy flask_migrate flask-jwt-extended psycopg2-binary
pipenv shell
```

### 2. PostgreSQL Setup
- Create the database:
```sql
CREATE DATABASE late_show_db;
```
- Create a user (if needed):
```sql
CREATE USER your_username WITH PASSWORD 'your_password';
GRANT ALL PRIVILEGES ON DATABASE late_show_db TO your_username;
GRANT ALL ON SCHEMA public TO your_username;
```

### 3. Environment Variables
Set your database connection:
```bash
export DATABASE_URI="postgresql://username:password@localhost:5432/late_show_db"
export JWT_SECRET_KEY="your-secret-key"
export FLASK_APP=server.app
```

### 4. Migrate and Seed
```bash
flask db init
flask db migrate -m "initial migration"
flask db upgrade
python -m server.seed
```

### 5. Run the Server
```bash
flask run
```

## 🔐 Auth Flow
1. **Register:** `POST /register` (username, password)
2. **Login:** `POST /login` (returns JWT token)
3. **Use token:** Add header `Authorization: Bearer <token>` to protected routes

## 🛣 Routes

| Route                  | Method | Auth? | Description                       |
|------------------------|--------|-------|-----------------------------------|
| /register              | POST   | ❌    | Register a user                   |
| /login                 | POST   | ❌    | Log in + get JWT                  |
| /episodes              | GET    | ❌    | List episodes                     |
| /episodes/<id>         | GET    | ❌    | Get episode + appearances         |
| /episodes/<id>         | DELETE | ✅    | Delete episode + appearances      |
| /guests                | GET    | ❌    | List guests                       |
| /appearances           | POST   | ✅    | Create appearance                 |

## 📝 Sample Requests & Responses

### Register User
```bash
POST /register
Content-Type: application/json

{
  "username": "admin",
  "password": "password"
}
```
**Response:**
```json
{
  "message": "User registered successfully"
}
```

### Login
```bash
POST /login
Content-Type: application/json

{
  "username": "admin",
  "password": "password"
}
```
**Response:**
```json
{
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
}
```

### List Episodes
```bash
GET /episodes
```
**Response:**
```json
[
  {
    "id": 1,
    "date": "2023-01-01",
    "number": 1
  },
  {
    "id": 2,
    "date": "2023-01-02",
    "number": 2
  }
]
```

### Get Episode Details
```bash
GET /episodes/1
```
**Response:**
```json
{
  "id": 1,
  "date": "2023-01-01",
  "number": 1,
  "appearances": [
    {
      "id": 1,
      "rating": 5,
      "guest": {
        "id": 1,
        "name": "Tom Hanks",
        "occupation": "Actor"
      }
    }
  ]
}
```

### Create Appearance (Protected)
```bash
POST /appearances
Authorization: Bearer <your_jwt_token>
Content-Type: application/json

{
  "rating": 5,
  "guest_id": 1,
  "episode_id": 1
}
```
**Response:**
```json
{
  "id": 4,
  "rating": 5,
  "guest_id": 1,
  "episode_id": 1
}
```

### Delete Episode (Protected)
```bash
DELETE /episodes/1
Authorization: Bearer <your_jwt_token>
```
**Response:**
```json
{
  "message": "Episode deleted"
}
```

## 🧪 Postman Usage Guide

1. **Import Collection:**
   - Open Postman
   - Click "Import" → "File"
   - Select `challenge-4-lateshow.postman_collection.json`

2. **Set Environment Variables:**
   - Create a new environment
   - Add variable `base_url` = `http://localhost:5000`
   - Add variable `token` (will be set after login)

3. **Testing Flow:**
   - Run "Register User" request
   - Run "Login" request and copy the token
   - Set the `token` environment variable
   - Test all other endpoints

4. **Protected Routes:**
   - Use `{{token}}` in Authorization header
   - Format: `Bearer {{token}}`

## 📁 Folder Structure
```
.
├── server/
│   ├── app.py              # Flask app factory
│   ├── config.py           # Configuration settings
│   ├── seed.py             # Database seeding script
│   ├── models/
│   │   ├── __init__.py
│   │   ├── user.py         # User model with auth
│   │   ├── guest.py        # Guest model
│   │   ├── episode.py      # Episode model
│   │   └── appearance.py   # Appearance model
│   └── controllers/
│       ├── __init__.py
│       ├── auth_controller.py      # Auth endpoints
│       ├── guest_controller.py     # Guest endpoints
│       ├── episode_controller.py   # Episode endpoints
│       └── appearance_controller.py # Appearance endpoints
├── migrations/             # Database migrations
├── README.md
└── .gitignore
```

## ✅ Submission Checklist

- ✅ **MVC folder structure** - Complete with models, controllers, and app factory
- ✅ **PostgreSQL used** - No SQLite, using PostgreSQL with proper configuration
- ✅ **Models + validations complete** - All models with proper relationships and validations
- ✅ **Auth implemented + protected routes** - JWT authentication with protected endpoints
- ✅ **Seed data works** - Database seeded with sample data
- ✅ **All routes work** - All endpoints implemented and functional
- ✅ **Clean, complete README.md** - Comprehensive documentation
- ⏳ **GitHub repo pushed and shared** - Ready for submission

## 🔗 GitHub Repository
**Repository:** https://github.com/your-username/late-show-api-challenge

## 🚀 Quick Start
```bash
# Clone and setup
git clone https://github.com/your-username/late-show-api-challenge.git
cd late-show-api-challenge
pipenv install
pipenv shell

# Database setup
export DATABASE_URI="postgresql://username:password@localhost:5432/late_show_db"
export FLASK_APP=server.app
flask db upgrade
python -m server.seed

# Run server
flask run
```

**Server will be available at:** `http://localhost:5000` 