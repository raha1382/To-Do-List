# 📝 ToDo CLI Project

A simple and extensible **To-Do List Manager using API and database** built with Python and Poetry.  

---
🌱 Branch Information
This repository uses a structured branching model to separate experimental work, refactoring, and stable releases.

| Branch | Description |
|---------|--------------|
| **`develop`** | 🌱 **Experimental Development Branch** — Used for testing and adding new features. Code here may be unstable. |
| **`develop-db-version`** | 🌱 **Experimental Development Branch using database** — This version has database instead of saving in memory. |
| **`develop-API-version`** | 🌱 **Experimental Development Branch using database** — This version uses API instead of CLI |
| **`refactor/correct-version`** | 🔧 **Refactored & Corrected Version** — Contains the latest fixes, improvements, and architectural refinements for in memory verion and usage of the code.|
| **`refactor-db/correct-version`** | 🔧 **Refactored & Corrected Version** — Contains the latest fixes, improvements, and architectural refinements for database verion and usage of the code. |
| **`refactor-API/correct-version`** | 🔧 **Refactored & Corrected Version** — Contains the latest fixes, improvements, and architectural refinements for API verion and usage of the code without CLI. |
| **`main`** | 🧩 **Stable Release Branch** — Production-ready and runnable version of the API. Merges from `refactor-API/correct-version` after validation. |


---

# 1️⃣ API Section (latest version)

This section describes the **latest API version** (branch: `refactor-API/correct-version`) with full FastAPI endpoints.  

### Branches
- `develop-API-version` → development version of the API  
- `refactor-API/correct-version` → latest, fully corrected API version

### Run API Server
Make sure you have **Poetry** and **Python (3.10+)** installed.
```bash
# install dependencies
poetry install

# run server
poetry run uvicorn todo.app.main:app --reload
```

### Server
```bash
http://127.0.0.1:8000
```

### Swagger & API Docs
```bash
http://127.0.0.1:8000/docs
```

##Here you can see all endpoints:

Projects
```bash
POST /projects/ → create project

GET /projects/ → list all projects

GET /projects/{name} → get single project

PUT /projects/{name} → update project completely

PATCH /projects/{name} → update part of a project

DELETE /projects/{id} → delete project
```

Tasks
```bash

POST /tasks/ → create task

GET /tasks?project_name= → list tasks in a project

GET /tasks/{task_id} → get single task

PUT /tasks/{task_id} → update task status

PATCH /tasks/{task_id} → update task partially

DELETE /tasks/{task_id} → delete task
```

---

# 2️⃣ DB or In Memory Storage versions

### Prerequisites

You can install Poetry using this codes and run code:
```bash
pip install poetry
poetry install
poetry run python src/todo/cli/main.py

# generate migration for db-version
poetry run alembic revision --autogenerate -m "initial"

# apply migration for db-version
poetry run alembic upgrade head

```
create a project:
```bash
create-project --name "MyProject" --description "A test project"
```
add a task:
```bash
add-task --project-name "MyProject" --task-name "Task1" --description "First task"
```
get list of tasks:
```bash
list-tasks --project-name "MyProject"
```
update project:
```bash
update-project --name "MyProject" --new-description "Updated project"
```
update task:
```bash
update-task --project-name "MyProject" --task-name "Task1" --new-description "Updated task"
```
change task status: 
```bash
change-task-status --project-name "MyProject" --task-name "Task1" --status "done"
```
delete tasks:
```bash
delete-task --project-name "MyProject" --task-id "1"
```
get list of projects:
```bash
list-projects
```
delete projects:
```bash
delete-project --name "MyProject"
```
exit cli:
```bash
exit
```
