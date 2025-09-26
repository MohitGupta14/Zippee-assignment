````markdown
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

---

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/MohitGupta14/Zippee-assignment
   cd Zippee-assignment
````

2. Create and activate a virtual environment:

   ```bash
   python3 -m venv .venv
   source .venv/bin/activate   # Linux/macOS
   .venv\Scripts\activate      # Windows
   ```

3. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Set up environment variables in `.env`:

   ```env
   FLASK_ENV=development
   FLASK_DEBUG=1
   SECRET_KEY=super-secret-flask-key
   DATABASE_URL=postgresql://postgres:<password>@localhost:5432/taskdb
   JWT_SECRET_KEY=super-secret-jwt-key
   ```

5. Initialize the database:

   ```bash
   flask db init
   flask db migrate
   flask db upgrade
   ```

6. Run the server:

   ```bash
   python run.py
   ```

---

## API Documentation

**Base URL:** `http://127.0.0.1:5000`

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
>
> ```
> Authorization: Bearer <access_token>
> ```

---

## Postman Collection

You can import the provided Postman collection to test all endpoints quickly. Make sure to replace `<access_token>` with your JWT token from login.

---

## Contributing

1. Fork the repository
2. Create your feature branch: `git checkout -b feature/xyz`
3. Commit changes: `git commit -m "Add xyz feature"`
4. Push to branch: `git push origin feature/xyz`
5. Open a pull request
