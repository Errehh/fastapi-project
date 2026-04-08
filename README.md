# FastAPI Social Media API

A robust RESTful API built with FastAPI for a social media platform, featuring user authentication, post management, and a voting system. This project demonstrates modern backend development practices including containerization, database migrations, and comprehensive testing.

## 🚀 Features

- **User Authentication & Authorization**
  - JWT-based authentication
  - Secure password hashing with bcrypt
  - Token-based access control

- **Post Management**
  - Create, read, update, and delete posts
  - User-specific post ownership
  - Timestamp tracking for posts

- **Voting System**
  - Upvote/downvote functionality for posts
  - One vote per user per post
  - Vote count aggregation

- **RESTful API Design**
  - Clear and consistent endpoint structure
  - Proper HTTP status codes
  - Request/response validation with Pydantic

## 🛠️ Tech Stack

**Backend Framework:** FastAPI  
**Database:** PostgreSQL  
**ORM:** SQLAlchemy  
**Migration Tool:** Alembic  
**Authentication:** JWT (python-jose)  
**Password Hashing:** Bcrypt (passlib)  
**Containerization:** Docker & Docker Compose  
**Testing:** Pytest  
**Python Version:** 3.14


## 🔌 API Endpoints

### Authentication
- `POST /login` - User login (returns JWT token)

### Users
- `POST /users/` - Create new user
- `GET /users/{id}` - Get user by ID

### Posts
- `GET /posts` - Get all posts
- `POST /posts` - Create new post (requires authentication)
- `GET /posts/{id}` - Get specific post
- `PUT /posts/{id}` - Update post (requires authentication & ownership)
- `DELETE /posts/{id}` - Delete post (requires authentication & ownership)

### Votes
- `POST /vote` - Vote on a post (requires authentication)

## 📊 API Documentation

Once the server is running, visit:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

These provide interactive documentation where you can test all endpoints directly.

## 🧪 Testing

The project includes comprehensive tests using Pytest.

**Run all tests:**
```bash
pytest
```

## 🗄️ Database Migrations

This project uses Alembic for database migrations.

**Create a new migration:**
```bash
alembic revision --autogenerate -m "description of changes"
```

**Apply migrations:**
```bash
alembic upgrade head
```

**Rollback migration:**
```bash
alembic downgrade -1
```

**Note:** This is a learning project built to demonstrate backend development skills including API design, authentication, database management, and containerization.
