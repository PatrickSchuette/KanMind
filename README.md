# 📦 KanMind Backend API

## 📌 Description
KanMind is a Kanban board backend built with Django and Django REST Framework.
It includes user authentication, boards, tasks, comments, and task visualization
features such as assigned tasks and task counts.

**Note:** This repository contains the backend only. The matching frontend is
provided separately here:
[Developer-Akademie-Backendkurs/project.KanMind](https://github.com/Developer-Akademie-Backendkurs/project.KanMind).
Clone and run it independently (see the CORS note below for connecting them).

---

## ⚙️ Tech Stack
- Python 3.14.6
- Django 6.0.7
- Django REST Framework 3.17.1
- SQLite 3.51.0

---

## 🚀 Quickstart Instructions

- Clone the repository:
```bash
git clone https://github.com/PatrickSchuette/KanMind.git
```

- Create a virtual environment:
```bash
python -m venv env
```

- Activate the virtual environment:
```bash
# Windows
env\Scripts\activate

# macOS/Linux
source env/bin/activate
```

- Install dependencies:
```bash
pip install -r requirements.txt
```

- Create a `.env` file in the project root (see [Notes](#️-notes) below for
  the required values).

- Run database migrations:
```bash
python manage.py migrate
```

- Create a superuser:
```bash
python manage.py createsuperuser
```

- Run the server:
```bash
python manage.py runserver
```

---

# 📡 API Overview

## 🔐 Authentication
- `POST /api/registration/` → register user
- `POST /api/login/` → login user + get token
- `POST /api/logout/` → logout user (invalidates token)
- `GET /api/email-check/` → check if an email is already registered

## 📊 Boards
- `GET /api/boards/` → list boards
- `POST /api/boards/` → create board
- `GET /api/boards/{board_id}/` → get board details
- `PATCH /api/boards/{board_id}/` → update board
- `DELETE /api/boards/{board_id}/` → delete board

## ✅ Tasks
- `GET /api/tasks/assigned-to-me/` → tasks assigned to me
- `GET /api/tasks/reviewing/` → tasks I'm reviewing
- `POST /api/tasks/` → create task
- `PATCH /api/tasks/{task_id}/` → update task
- `DELETE /api/tasks/{task_id}/` → delete task

## 💬 Comments
- `GET /api/tasks/{task_id}/comments/` → list comments
- `POST /api/tasks/{task_id}/comments/` → add comment
- `DELETE /api/tasks/{task_id}/comments/{comment_id}/` → delete comment

---

## ⚠️ Notes

- Authentication uses DRF Token Authentication. Include the token in every
  authenticated request as:
  ```
  Authorization: Token <your_token>
  ```
- The `SECRET_KEY` and `DEBUG` values are loaded from a `.env` file, which is
  **not** included in this repository. Create your own `.env` file in the
  project root before running the server:
  ```
  SECRET_KEY=your-secret-key-here
  DEBUG=True
  ```
- CORS is currently allowed for `http://localhost:5173` and
  `http://127.0.0.1:5500` (adjust `CORS_ALLOWED_ORIGINS` in
  `core/settings.py` if your frontend runs on a different port).
- A task's `board` field cannot be changed after creation.
- `assignee` and `reviewer` must be members of the task's board.

---

# 🧪 Testing

This project includes a Postman Collection and Environment file covering
both happy-path and unhappy-path scenarios:

- [KanMind.postman_collection.json](./postmanJson//KanMind.postman_collection.json)
- [KanMind.postman_environment.json](./postmanJson//KanMind.postman_environment.json)

To use them:
1. Import both files into Postman
2. Select the "KanMind" environment
3. Run requests individually, or use the Collection Runner to execute the
   full suite
