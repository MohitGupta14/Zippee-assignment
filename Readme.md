# 📝 Zippie

A Flask-based task management API with JWT authentication, user roles, and task CRUD functionality. Designed for learning, testing, or as a starter backend for task-oriented applications.

---

## ✨ Features

* **User Management**

  * Register new users
  * Login and logout with JWT
  * Admin and regular user roles

* **Task Management**

  * Create, read, update, delete tasks
  * Filter tasks by completion status
  * Pagination support

* **Security**

  * JWT-based authentication
  * Blacklist tokens on logout

* **Database**

  * PostgreSQL with SQLAlchemy ORM
  * Flask-Migrate for migrations

* **Deployment**

  * Docker and Docker Compose support
  * Production-ready containerization

---

# 🚀 Quick Start

You can run the Zippie API in **three ways**:

---

## 1️⃣ Run from Docker Hub (Prebuilt Image)

This is the fastest way to try the app without building locally.

### Pull the app image:

```bash
docker pull fireefurry/zippie-app:latest
```

### Run PostgreSQL:

```bash
docker run -d \
  --name zippie-postgres \
  -e POSTGRES_USER=user \
  -e POSTGRES_PASSWORD=password \
  -e POSTGRES_DB=taskdb \
  -p 5432:5432 \
  postgres:15
```

### Run the app:

```bash
docker run -d -p 5000:5000 \
  --name zippie-app \
  --link zippie-postgres:db \
  -e DATABASE_URL=postgresql://user:password@db:5432/taskdb \
  fireefurry/zippie-app:latest
```

### Demo Video

[![Watch the demo](https://github.com/user-attachments/assets/430dcffc-6922-4e0c-b44a-6d1c333101a4)](https://www.youtube.com/watch?v=UJH7r4i1ppU&autoplay=1)




### check the logs
```bash
docker logs -f zippie-app
```

### Access the API:

* API → `http://localhost:3000`
* Database → `localhost:5432`
* Postman documentation → [https://documenter.getpostman.com/view/31247402/2sB3QDvYXe](https://documenter.getpostman.com/view/31247402/2sB3QDvYXe)

---

## 2️⃣ Run with Docker Compose (Build from Source)

This is the recommended setup for local development.

### Prerequisites:

* Docker & Docker Compose
* Git

### Setup:

```bash
# Clone repository
git clone https://github.com/MohitGupta14/Zippee-assignment
cd Zippee-assignment
```

### Create `.env` file:

```env
FLASK_ENV=production
FLASK_DEBUG=0
SECRET_KEY=your-super-secret-flask-key-here
JWT_SECRET_KEY=your-super-secret-jwt-key-here
```

### Start the app:

```bash
docker compose up --build
```

### Demo Video

### Demo Video

[![Watch the demo](https://github.com/user-attachments/assets/4e6fd9d2-a97a-42b3-bb9b-26492b19beb2)](https://www.youtube.com/watch?v=52q7BTBEZxM&autoplay=1)



### Access the API:

* API → `http://localhost:3000`
* Database → `localhost:5432`
* Postman documentation → [https://documenter.getpostman.com/view/31247402/2sB3QDvYXe](https://documenter.getpostman.com/view/31247402/2sB3QDvYXe)

---

## 3️⃣ Run without Docker (Manual Setup)

If you prefer running directly on your machine.

### Clone repo:

```bash
git clone https://github.com/MohitGupta14/Zippee-assignment
cd Zippee-assignment
```

### Setup virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate   # macOS/Linux
.venv\Scripts\activate      # Windows
```

### Install dependencies:

```bash
pip install -r requirements.txt
```

### Setup PostgreSQL manually:

```bash
# 1. Log in to PostgreSQL
psql -U postgres

# 2. Create the database
CREATE DATABASE taskdb;

# 3. Set/update password for postgres user
ALTER USER postgres WITH PASSWORD 'newpassword';

# 4. Connect to the new database
\c taskdb

# 5. Database connection URL
# postgresql://postgres:newpassword@localhost:5432/taskdb

```

### Create `.env` file:

```env
FLASK_ENV=development
FLASK_DEBUG=1
SECRET_KEY=super-secret-flask-key
DATABASE_URL=postgresql://postgres:<password>@localhost:5432/taskdb
JWT_SECRET_KEY=super-secret-jwt-key
```

### Initialize database:

```bash
flask db init
flask db migrate -m "Initial migration"
flask db upgrade
```

### Run the server:

```bash
python run.py
```

### Demo Video

[![Watch the demo](https://github.com/user-attachments/assets/4e6fd9d2-a97a-42b3-bb9b-26492b19beb2)](https://www.youtube.com/watch?v=0ctRfGpavmo&autoplay=1)

### Access the API:

* API → `http://127.0.0.1:5000`
* Postman documentation → [https://documenter.getpostman.com/view/31247402/2sB3QDvYXe](https://documenter.getpostman.com/view/31247402/2sB3QDvYXe)

---

# 📖 API Documentation

**Base URL:**

* Docker / Compose → `http://localhost:3000`
* Manual → `http://127.0.0.1:5000`

### Auth Endpoints

* `POST /auth/register` – Register a new user
* `POST /auth/login` – Login and get JWT
* `POST /auth/logout` – Logout and blacklist JWT

### Task Endpoints

* `GET /tasks/tasks` – List tasks (with pagination/filtering)
* `GET /tasks/tasks/<task_id>` – Get a specific task
* `POST /tasks/tasks` – Create a task
* `PUT /tasks/tasks/<task_id>` – Update a task
* `DELETE /tasks/tasks/<task_id>` – Delete a task

🔑 **Authorization header required for tasks:**

```
Authorization: Bearer <access_token>
```

### Example API Usage (curl)

**Register a user:**

```bash
curl -X POST http://localhost:3000/auth/register \
  -H "Content-Type: application/json" \
  -d '{"username": "testuser", "email": "test@example.com", "password": "password123"}'
```

**Login:**

```bash
curl -X POST http://localhost:3000/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username": "testuser", "password": "password123"}'
```

**Create a task:**

```bash
curl -X POST http://localhost:3000/tasks/tasks \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <your-jwt-token>" \
  -d '{"title": "My First Task", "description": "Task description"}'
```

---

# ⚙️ Development Guide

### Project Structure

```
├── app/
│   ├── auth/          # Authentication routes
│   ├── tasks/         # Task management routes
│   ├── models.py      # Database models
│   └── __init__.py    # App factory
├── docker-compose.yml
├── Dockerfile
├── requirements.txt
├── run.py
├── start.sh
├── wait_for_db.py
└── .env
```

### Common Docker Commands

```bash
docker compose up         # start
docker compose up -d      # start detached
docker compose down       # stop
docker compose logs app   # app logs
docker compose logs postgres  # DB logs
```

### Database migrations (inside container):

```bash
docker compose exec app flask db migrate -m "message"
docker compose exec app flask db upgrade
```

---

# 🛠️ Troubleshooting

**Port already in use:**

```bash
sudo lsof -i :3000
sudo kill -9 <PID>
```

**Check Postgres logs:**

```bash
docker compose logs postgres
```

**Reset DB (development only):**

```bash
docker compose down
docker volume rm $(docker compose config --volumes)
docker compose up --build
```
