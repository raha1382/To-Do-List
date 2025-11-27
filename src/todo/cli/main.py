import argparse
from todo.core.project_service import ProjectService
from todo.core.task_service import TaskService
from ..repositories.project_repository import ProjectRepository
from ..repositories.task_repository import TaskRepository
from datetime import datetime
from todo.app.commands.scheduler import start_scheduler
import threading
from todo.db.session import get_db

import warnings

warnings.warn(
    "CLI is deprecated. Use the Web API at http://localhost:8000/docs instead.",
    DeprecationWarning,
    stacklevel=2
)

print("""
╔══════════════════════════════════════════════════════════════════╗
║                         CLI IS DEPRECATED                        ║
║                                                                  ║
║  This CLI has been deprecated .                                  ║
║  Please use the new Web API:                                     ║
║                                                                  ║
║       http://localhost:8000/docs   (Swagger UI)                  ║
║       http://localhost:8000/redoc  (ReDoc)                       ║
║                                                                  ║
╚══════════════════════════════════════════════════════════════════╝
""")

def main(project_repo: ProjectRepository, task_repo: TaskRepository):

    project_service = ProjectService(project_repo, task_repo)
    task_service = TaskService(project_repo, task_repo)


    parser = argparse.ArgumentParser(description="ToDo List CLI Application")
    subparsers = parser.add_subparsers(dest="command")

    # Create project command
    parser_create_project = subparsers.add_parser("create-project", help="Create a new project")
    parser_create_project.add_argument("--name", required=True, help="Name of the project")
    parser_create_project.add_argument("--description", help="Description of the project")

    # Update project command
    parser_update_project = subparsers.add_parser("update-project", help="Update an existing project")
    parser_update_project.add_argument("--name", required=True, help="Name of the project to update")
    parser_update_project.add_argument("--new-name", help="New name of the project")
    parser_update_project.add_argument("--new-description", help="New description of the project")

    # Add task command
    parser_add_task = subparsers.add_parser("add-task", help="Add a task to a project")
    parser_add_task.add_argument("--project-name", required=True, help="Name of the project")
    parser_add_task.add_argument("--task-name", required=True, help="Name of the task")
    parser_add_task.add_argument("--description", help="Description of the task")
    parser_add_task.add_argument("--deadline", help="Deadline of the task in 'YYYY-MM-DD', 'YYYY-MM-DD HH:MM', or 'YYYY-MM-DD HH:MM:SS' format (optional)")

    # Update task command
    parser_update_task = subparsers.add_parser("update-task", help="Update an existing task")
    parser_update_task.add_argument("--project-name", required=True, help="Name of the project")
    parser_update_task.add_argument("--task-name", required=True, help="Name of the task to update")
    parser_update_task.add_argument("--new-name", help="New name of the task")
    parser_update_task.add_argument("--new-description", help="New description of the task")
    parser_update_task.add_argument("--status", help="New status of the task (todo, doing, done)")
    parser_update_task.add_argument("--deadline", help="Deadline of the task (optional)")

    # Change task status command
    parser_change_status = subparsers.add_parser("change-task-status", help="Change the status of a task")
    parser_change_status.add_argument("--project-name", required=True, help="Name of the project")
    parser_change_status.add_argument("--task-name", required=True, help="Name of the task")
    parser_change_status.add_argument("--status", required=True, help="New status (todo, doing, done)")

    # Delete task command
    parser_delete_task = subparsers.add_parser("delete-task", help="Delete a task")
    parser_delete_task.add_argument("--project-name", required=True, help="Name of the project")
    parser_delete_task.add_argument("--task-id", type=int, required=True, help="ID of the task to delete")

    # List tasks command
    parser_list_tasks = subparsers.add_parser("list-tasks", help="List all tasks of a project")
    parser_list_tasks.add_argument("--project-name", required=True, help="Name of the project")

    # List projects command
    parser_list_projects = subparsers.add_parser("list-projects", help="List all projects")

    # Delete project command
    parser_delete_project = subparsers.add_parser("delete-project", help="Delete a project")
    parser_delete_project.add_argument("--name", required=True, help="Name of the project to delete")

    while True:
        try:
           
            command = input("Enter command (or 'exit' to quit): ").strip()
            if command.lower() == 'exit':
                print("Exiting...")
                break

            
            import shlex
            args = parser.parse_args(shlex.split(command))

            if args.command == "create-project":
                try:
                    args.name = args.name.strip() if args.name else None
                    args.description = args.description.strip() if args.description else None
                    project = project_service.create_project(args.name, args.description or "")
                    print(f"Project '{project.name}' created successfully.")
                except ValueError as e:
                    print(f"Error: {e}")
            elif args.command == "update-project":
                try:
                    args.name = args.name.strip() if args.name else None
                    args.new_name = args.new_name.strip() if args.new_name else None
                    args.new_description = args.new_description.strip() if args.new_description else None
                    success = project_service.update_project(
                        args.name,
                        args.new_name or args.name,
                        args.new_description or ""
                    )
                    if success:
                        print(f"Project '{args.name}' updated successfully.")
                    else:
                        print(f"Error: Project '{args.name}' not found.")
                except ValueError as e:
                    print(f"Error: {e}")
            elif args.command == "add-task":
                try:
                    args.task_name = args.task_name.strip() if args.task_name else None
                    args.description = args.description.strip() if args.description else None
                    args.project_name = args.project_name.strip() if args.project_name else None
                    if args.deadline:
                        d = args.deadline.strip()
                        try:
                            args.deadline = datetime.strptime(d, "%Y-%m-%d %H:%M:%S")
                        except ValueError:
                            try:
                                args.deadline = datetime.strptime(d, "%Y-%m-%d %H:%M")
                            except ValueError:
                                try:
                                    args.deadline = datetime.strptime(d, "%Y-%m-%d")
                                except ValueError:
                                    raise ValueError("Invalid deadline format")
                    task = task_service.create_task(
                        name=args.task_name,
                        description=args.description or "",
                        deadline=args.deadline,  
                        project_name=args.project_name
                    )
                    print(f"Task '{args.task_name}' added successfully with ID {task.id}.")
                except ValueError as e:
                    print(f"Error: {e}")
            elif args.command == "update-task":
                try:
                    args.project_name = args.project_name.strip() if args.project_name else None
                    args.task_name = args.task_name.strip() if args.task_name else None
                    args.new_name = args.new_name.strip() if args.new_name else None
                    args.new_description = args.new_description.strip() if args.new_description else None
                    args.status = args.status.strip() if args.status else None
                    if args.deadline:
                        d = args.deadline.strip()
                        try:
                            args.deadline = datetime.strptime(d, "%Y-%m-%d %H:%M:%S")
                        except ValueError:
                            try:
                                args.deadline = datetime.strptime(d, "%Y-%m-%d %H:%M")
                            except ValueError:
                                try:
                                    args.deadline = datetime.strptime(d, "%Y-%m-%d")
                                except ValueError:
                                    raise ValueError("Invalid deadline format")
                    task = task_service.get_task(args.task_name)
                    if task is None:
                        print(f"Error: Task '{args.task_name}' not found in project '{args.project_name}'.")
                    else:
                        success = task_service.update_task(
                            project_name=args.project_name,
                            task_name=args.task_name,
                            new_name=args.new_name or args.task_name,
                            description=args.new_description or task.description,
                            status=args.status or task.status.value,
                            deadline=args.deadline
                        )
                        if success:
                            print(f"Task '{args.task_name}' updated successfully in project '{args.project_name}'.")
                        else:
                            print(f"Error: Task '{args.task_name}' not found in project '{args.project_name}'.")
                except ValueError as e:
                    print(f"Error: {e}")
            elif args.command == "change-task-status":
                try:
                    args.project_name = args.project_name.strip() if args.project_name else None
                    args.task_name = args.task_name.strip() if args.task_name else None
                    args.status = args.status.strip() if args.status else None
                    success = task_service.change_task_status(args.project_name, args.task_name, args.status)
                    if success:
                        print(f"Status of task '{args.task_name}' in project '{args.project_name}' changed to '{args.status}'.")
                    else:
                        print(f"Error: Task '{args.task_name}' not found in project '{args.project_name}'.")
                except ValueError as e:
                    print(f"Error: {e}")
            elif args.command == "delete-task":
                try:
                    args.project_name = args.project_name.strip() if args.project_name else None
                    success = task_service.delete_task(args.project_name, args.task_id)
                    if success:
                        print(f"Task with ID '{args.task_id}' deleted successfully from project '{args.project_name}'.")
                    else:
                        print(f"Error: Task with ID '{args.task_id}' not found in project '{args.project_name}'.")
                except Exception as e:
                    print(f"Error: {e}")
            elif args.command == "list-tasks":
                try:
                    args.project_name = args.project_name.strip() if args.project_name else None
                    tasks = task_service.list_tasks(args.project_name)
                    if tasks:
                        print(f"Tasks in project '{args.project_name}':")
                        for task in tasks:
                            closed = task.closed_at.strftime("%Y-%m-%d %H:%M:%S") if task.closed_at else "task has not been done yet."
                            print(f"- (name: {task.title}) : (description: {task.description}) (Status: {task.status.value}) (id: {task.id}) (deadline: {task.deadline}) (closed at: {closed})")
                    else:
                        print(f"No tasks found in project '{args.project_name}'.")
                except ValueError as e:
                    print(f"Error: {e}")
            elif args.command == "list-projects":
                projects = project_service.list_projects()
                if projects:
                    for project in projects:
                        print(f"(name: {project.name}) - (id: {project.id}) - (description: {project.description})")
                else:
                    print("No projects found.")
            elif args.command == "delete-project":
                try:
                    args.name = args.name.strip() if args.name else None
                    success = project_service.delete_project(args.name)
                    if success:
                        print(f"Project '{args.name}' and its tasks deleted successfully.")
                    else:
                        print(f"Error: Project '{args.name}' not found.")
                except ValueError as e:
                    print(f"Error: {e}")
            else:
                print("Unknown command. Available commands: create-project, update-project, add-task, update-task, change-task-status, delete-task, list-tasks, list-projects, delete-project")

        except SystemExit:
            pass 
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    db = next(get_db())
    task_repo = TaskRepository(db)
    project_repo = ProjectRepository(db)

    scheduler_thread = threading.Thread(
        target=lambda: start_scheduler(task_repo),
        daemon=True
    )
    scheduler_thread.start()

    main(project_repo, task_repo)
    