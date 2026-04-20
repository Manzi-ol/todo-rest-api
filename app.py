"""
app.py — RESTful TODO API with Flask + SQLite.

Run:
    pip install -r requirements.txt
    python app.py

Endpoints:
    GET    /todos              List all todos
    GET    /todos/<id>         Get one todo
    POST   /todos              Create todo  { "title": "...", "description": "..." }
    PUT    /todos/<id>         Update todo  { "title": "...", "done": true }
    DELETE /todos/<id>         Delete todo
    GET    /todos?done=true    Filter by completion status
    GET    /todos?search=text  Search by title
"""

import os
import sqlite3
from datetime import datetime

from flask import Flask, jsonify, request, abort

app = Flask(__name__)
DB_PATH = "todos.db"


def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    with get_db() as db:
        db.execute("""
            CREATE TABLE IF NOT EXISTS todos (
                id          INTEGER PRIMARY KEY AUTOINCREMENT,
                title       TEXT NOT NULL,
                description TEXT DEFAULT '',
                done        BOOLEAN DEFAULT 0,
                created_at  TEXT NOT NULL,
                updated_at  TEXT NOT NULL
            )
        """)


def todo_to_dict(row) -> dict:
    return {
        "id":          row["id"],
        "title":       row["title"],
        "description": row["description"],
        "done":        bool(row["done"]),
        "created_at":  row["created_at"],
        "updated_at":  row["updated_at"],
    }


@app.route("/todos", methods=["GET"])
def list_todos():
    done_filter = request.args.get("done")
    search = request.args.get("search", "").strip()
    query = "SELECT * FROM todos WHERE 1=1"
    params: list = []

    if done_filter is not None:
        query += " AND done = ?"
        params.append(1 if done_filter.lower() == "true" else 0)

    if search:
        query += " AND title LIKE ?"
        params.append(f"%{search}%")

    query += " ORDER BY id DESC"
    with get_db() as db:
        rows = db.execute(query, params).fetchall()
    return jsonify([todo_to_dict(r) for r in rows])


@app.route("/todos/<int:todo_id>", methods=["GET"])
def get_todo(todo_id: int):
    with get_db() as db:
        row = db.execute("SELECT * FROM todos WHERE id = ?", (todo_id,)).fetchone()
    if not row:
        abort(404, description=f"Todo #{todo_id} not found.")
    return jsonify(todo_to_dict(row))


@app.route("/todos", methods=["POST"])
def create_todo():
    data = request.get_json(force=True)
    title = (data.get("title") or "").strip()
    if not title:
        abort(400, description="'title' is required.")
    now = datetime.utcnow().isoformat()
    with get_db() as db:
        cursor = db.execute(
            "INSERT INTO todos (title, description, created_at, updated_at) VALUES (?, ?, ?, ?)",
            (title, data.get("description", ""), now, now),
        )
        row = db.execute("SELECT * FROM todos WHERE id = ?", (cursor.lastrowid,)).fetchone()
    return jsonify(todo_to_dict(row)), 201


@app.route("/todos/<int:todo_id>", methods=["PUT"])
def update_todo(todo_id: int):
    data = request.get_json(force=True)
    with get_db() as db:
        row = db.execute("SELECT * FROM todos WHERE id = ?", (todo_id,)).fetchone()
        if not row:
            abort(404, description=f"Todo #{todo_id} not found.")
        title = data.get("title", row["title"]).strip() or row["title"]
        description = data.get("description", row["description"])
        done = int(data.get("done", row["done"]))
        now = datetime.utcnow().isoformat()
        db.execute(
            "UPDATE todos SET title=?, description=?, done=?, updated_at=? WHERE id=?",
            (title, description, done, now, todo_id),
        )
        updated = db.execute("SELECT * FROM todos WHERE id = ?", (todo_id,)).fetchone()
    return jsonify(todo_to_dict(updated))


@app.route("/todos/<int:todo_id>", methods=["DELETE"])
def delete_todo(todo_id: int):
    with get_db() as db:
        row = db.execute("SELECT id FROM todos WHERE id = ?", (todo_id,)).fetchone()
        if not row:
            abort(404, description=f"Todo #{todo_id} not found.")
        db.execute("DELETE FROM todos WHERE id = ?", (todo_id,))
    return jsonify({"message": f"Todo #{todo_id} deleted."})


@app.errorhandler(400)
@app.errorhandler(404)
def http_error(e):
    return jsonify({"error": str(e.description)}), e.code


if __name__ == "__main__":
    init_db()
    port = int(os.getenv("PORT", 5001))
    print(f"TODO API running → http://localhost:{port}/todos")
    app.run(host="0.0.0.0", port=port, debug=False)
