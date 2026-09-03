# Banter - A Chat Application

A real time chat application built using React, Zustand, FastAPI, and PostgreSQL.

The goal of the project is to implement the core architecture of a real-time messaging system. The application will allow users to create accounts, log in, and send and receive messages in a chat room.

### TechStack

| Frontend         | Backend                 |
| :--------------- | :---------------------- |
| JavaScript       | Python                  |
| React            | FastAPI                 |
| Zustand          | SQLAlchemy              |
| Vite             | PostgreSQL              |
| Native Fetch API | JWT Authentication      |
| React Router     | Argon2 Password Hashing |
|                  | Pydantic                |

### Features

- User Signup
- Login & Logout
- JWT-based Authentication
- Search users by name
- Create one-on-one conversations
- List user conversations
- Fetch messages from conversations
- Zustand state management for authentication and chat state

### Run locally

#### .env file

1. DATABASE_URL=link to your postgres database
2. JWT_SECRET_KEY=your-secret-key
3. JWT_ALGORITHM=HS256
4. ACCESS_TOKEN_EXPIRE_MINUTES=30
5. VITE_API_URL=http://127.0.0.1:8000

#### Backend

```bash
cd backend
uvicorn app.main:app --reload
```

#### Frontend

```bash
cd frontend
npm install
npm run dev
```
