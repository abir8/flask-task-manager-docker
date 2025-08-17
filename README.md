# ✅ Flask Task Manager API (Dockerized)

A simple REST API to manage tasks.  
Built with **Python Flask** + **SQLite**, containerized with **Docker**.

## 🚀 Run with Docker
```bash
docker build -t flask-task-manager .
docker run -d -p 5000:5000 flask-task-manager
```


🔧 API Endpoints
GET /tasks → List all tasks

POST /tasks → Create a new task

PUT /tasks/<id> → Update task

DELETE /tasks/<id> → Delete task