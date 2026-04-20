# TODO REST API

> A clean, fully-featured RESTful TODO API built with **Flask + SQLite**. Ready to plug into any frontend.

![Python](https://img.shields.io/badge/Python-3776AB?style=flat&logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-000000?style=flat&logo=flask&logoColor=white)
![SQLite](https://img.shields.io/badge/SQLite-003B57?style=flat&logo=sqlite&logoColor=white)

---

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/todos` | List all todos |
| `GET` | `/todos?done=true` | Filter by status |
| `GET` | `/todos?search=text` | Search by title |
| `GET` | `/todos/<id>` | Get one todo |
| `POST` | `/todos` | Create a todo |
| `PUT` | `/todos/<id>` | Update a todo |
| `DELETE` | `/todos/<id>` | Delete a todo |

---

## Quick Start

```bash
git clone https://github.com/Manzi-ol/todo-rest-api
cd todo-rest-api
pip install -r requirements.txt
python app.py
# → http://localhost:5001/todos
```

---

## Example Requests

```bash
# Create a todo
curl -X POST http://localhost:5001/todos \
  -H "Content-Type: application/json" \
  -d '{"title": "Build something great", "description": "Start today"}'

# List all todos
curl http://localhost:5001/todos

# Mark as done
curl -X PUT http://localhost:5001/todos/1 \
  -H "Content-Type: application/json" \
  -d '{"done": true}'

# Search
curl "http://localhost:5001/todos?search=great"

# Delete
curl -X DELETE http://localhost:5001/todos/1
```

---

## Response Format

```json
{
  "id": 1,
  "title": "Build something great",
  "description": "Start today",
  "done": false,
  "created_at": "2026-04-20T18:00:00",
  "updated_at": "2026-04-20T18:00:00"
}
```

---

## Tech Stack

- **Flask** — HTTP server & routing
- **SQLite** — Lightweight persistent storage
- Standard library only — no ORM needed

---

*Part of [Manzi's 100 GitHub Projects Roadmap](https://github.com/Manzi-ol) · Project #20*