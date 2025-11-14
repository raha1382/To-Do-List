# 📝 ToDo CLI Project

A simple and extensible **Command-Line Interface (CLI) To-Do List Manager** built with Python and Poetry.  
This tool allows you to manage multiple projects, each containing tasks that can be created, listed, updated, or deleted — all from your terminal.

---
🌱 Branch Information
This repository uses a structured branching model to separate experimental work, refactoring, and stable releases.

| Branch | Description |
|---------|--------------|
| **`develop`** | 🌱 **Experimental Development Branch** — Used for testing and adding new features. Code here may be unstable. |
| **`develop-db-version`** | 🌱 **Experimental Development Branch using database** — This version has database instead of saving in memory. |
| **`refactor/correct-version`** | 🔧 **Refactored & Corrected Version** — Contains the latest fixes, improvements, and architectural refinements. |
| **`main`** | 🧩 **Stable Release Branch** — Production-ready and runnable version of the CLI. Merges from `refactor/correct-version` after validation. |


---

## 🚀 Getting Started

### Prerequisites
Make sure you have **Poetry** and **Python (3.10+)** installed.

You can install Poetry using this codes and run code:
```bash
pip install poetry
poetry install
poetry run python src/todo/cli/main.py
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
