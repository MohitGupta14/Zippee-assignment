# Zippie

A Flask-based task management API with JWT authentication, user roles, and task CRUD functionality. Designed for learning, testing, or as a starter backend for task-oriented applications.

---

## Features

- **User Management**
  - Register new users
  - Login and logout with JWT
  - Admin and regular user roles

- **Task Management**
  - Create, read, update, delete tasks
  - Filter tasks by completion status
  - Pagination support

- **Security**
  - JWT-based authentication
  - Blacklist tokens on logout

- **Database**
  - PostgreSQL with SQLAlchemy ORM
  - Flask-Migrate for migrations

- **Deployment**
  - Docker and Docker Compose support
  - Production-ready containerization

---

## Quick Start with Docker (Recommended)

### Prerequisites
- Docker and Docker Compose installed
- Git

### Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/MohitGupta14/Zippee-assignment
   cd Zippee-assignment
   ```

2. **Create environment file:**
   Create a `.env` file in the project root:
   ```env
   FLASK_ENV=production
   FLASK_DEBUG=0
   SECRET_KEY=your-super-secret-flask-key-here
   JWT_SECRET_KEY=your-super-secret-jwt-key-here
   ```

3. **Start the application:**
   ```bash
   docker compose up --build
   ```

4. **Access the API:**
   - API will be available at `http://localhost:3000`
   - Database runs on `localhost:5432`

### Docker Commands

```bash
# Start the application
docker compose up

# Start in background
docker compose up -d

# Stop the application
docker compose down

# View logs
docker compose logs app
docker compose logs postgres

# Restart after code changes
docker compose up --build

# Clean restart (removes database data)
docker compose down
docker volume rm $(docker compose config --volumes)
docker compose up --build
```

---

## Manual Installation (Alternative)

If you prefer to run without Docker:

1. **Clone the repository:**
   ```bash
   git clone https://github.com/MohitGupta14/Zippee-assignment
   cd Zippee-assignment
   ```

2. **Create and activate a virtual environment:**
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate   # Linux/macOS
   .venv\Scripts\activate      # Windows
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up PostgreSQL database:**
   ```bash
   # Install PostgreSQL and create database
   createdb taskdb
   ```

5. **Set up environment variables in `.env`:**
   ```env
   FLASK_ENV=development
   FLASK_DEBUG=1
   SECRET_KEY=super-secret-flask-key
   DATABASE_URL=postgresql://postgres:<password>@localhost:5432/taskdb
   JWT_SECRET_KEY=super-secret-jwt-key
   ```

6. **Initialize the database:**
   ```bash
   flask db init
   flask db migrate -m "Initial migration"
   flask db upgrade
   ```

7. **Run the server:**
   ```bash
   python run.py
   ```

---

## API Documentation

**Base URL:** 
- Docker: `http://localhost:3000`
- Manual: `http://127.0.0.1:5000`

### Auth Endpoints

* `POST /auth/register` – Register a new user
* `POST /auth/login` – Login and get JWT access token
* `POST /auth/logout` – Logout and blacklist JWT

### Tasks Endpoints

* `GET /tasks/tasks` – List tasks (with pagination and optional filtering by `completed`)
* `GET /tasks/tasks/<task_id>` – Get a specific task
* `POST /tasks/tasks` – Create a task
* `PUT /tasks/tasks/<task_id>` – Update a task
* `DELETE /tasks/tasks/<task_id>` – Delete a task

> All `/tasks` endpoints require the header:
> ```
> Authorization: Bearer <access_token>
> ```

### Example API Usage

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

## Development

### Project Structure
```
├── app/
│   ├── auth/          # Authentication routes
│   ├── tasks/         # Task management routes
│   ├── models.py      # Database models
│   └── __init__.py    # App factory
├── docker-compose.yml # Docker configuration
├── Dockerfile        # Container definition
├── requirements.txt  # Python dependencies
├── run.py            # Application entry point
├── start.sh          # Application startup script
├── wait_for_db.py    # Database connection checker
└── .env              # Environment variables (create this)
```

### Making Changes

1. **Code changes with Docker:**
   - Edit your code
   - Restart containers: `docker compose restart app`
   - For major changes: `docker compose up --build`

2. **Database changes:**
   ```bash
   # Create migration
   docker compose exec app python3 -m flask db migrate -m "Description"
   
   # Apply migration
   docker compose exec app python3 -m flask db upgrade
   ```

3. **Access database:**
   ```bash
   docker compose exec postgres psql -U postgres -d taskdb
   ```

---

## Troubleshooting

### Common Issues

**Port already in use:**
```bash
# Change port in docker-compose.yml or kill process using port
sudo lsof -i :3000
sudo kill -9 <PID>
```

**Database connection issues:**
```bash
# Check if postgres is running
docker compose ps

# View postgres logs
docker compose logs postgres

# Reset database
docker compose down
docker volume rm $(docker compose config --volumes)
docker compose up --build
```

**Migration conflicts:**
```bash
# Reset migrations (development only)
docker compose down
docker volume rm $(docker compose config --volumes)
rm -rf migrations/
docker compose up --build
```

---

## Contributing

1. Fork the repository
2. Create your feature branch: `git checkout -b feature/xyz`
3. Make changes and test with Docker: `docker compose up --build`
4. Commit changes: `git commit -m "Add xyz feature"`
5. Push to branch: `git push origin feature/xyz`
6. Open a pull request