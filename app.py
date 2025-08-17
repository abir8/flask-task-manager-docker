from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)
DB_NAME = "tasks.db"

def init_db():
    with sqlite3.connect(DB_NAME) as conn:
        conn.execute('''CREATE TABLE IF NOT EXISTS tasks
                        (id INTEGER PRIMARY KEY AUTOINCREMENT,
                         title TEXT NOT NULL,
                         description TEXT,
                         done BOOLEAN NOT NULL DEFAULT 0)''')
    print("✅ Database initialized")

@app.route("/tasks", methods=["GET"])
def get_tasks():
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.execute("SELECT * FROM tasks")
        tasks = [
            {"id": row[0], "title": row[1], "description": row[2], "done": bool(row[3])}
            for row in cursor.fetchall()
        ]
    return jsonify(tasks)

@app.route("/tasks", methods=["POST"])
def add_task():
    data = request.json
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.execute("INSERT INTO tasks (title, description) VALUES (?, ?)",
                              (data["title"], data.get("description", "")))
        conn.commit()
        task_id = cursor.lastrowid
    return jsonify({"id": task_id, "message": "Task created"}), 201

@app.route("/tasks/<int:task_id>", methods=["PUT"])
def update_task(task_id):
    data = request.json
    with sqlite3.connect(DB_NAME) as conn:
        conn.execute("UPDATE tasks SET title=?, description=?, done=? WHERE id=?",
                     (data.get("title"), data.get("description"), int(data.get("done", 0)), task_id))
        conn.commit()
    return jsonify({"message": "Task updated"})

@app.route("/tasks/<int:task_id>", methods=["DELETE"])
def delete_task(task_id):
    with sqlite3.connect(DB_NAME) as conn:
        conn.execute("DELETE FROM tasks WHERE id=?", (task_id,))
        conn.commit()
    return jsonify({"message": "Task deleted"})

if __name__ == "__main__":
    init_db()
    app.run(host="0.0.0.0", port=5000, debug=True)