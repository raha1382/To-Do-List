import argparse
from todo.core.project_service import ProjectService
from todo.core.task_service import TaskService
from todo.storage.in_memory_storage import InMemoryStorage

# Global storage for persistence within session
storage = InMemoryStorage()
project_service = ProjectService(storage)
task_service = TaskService(storage)

def main():
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
    parser_add_task.add_argument("--deadline", help="Deadline of the task in YYYY-MM-DD format (optional)")

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
                    project = project_service.create_project(args.name, args.description or "")
                    print(f"Project '{project.name}' created successfully.")
                except ValueError as e:
                    print(f"Error: {e}")
            elif args.command == "update-project":
                try:
                    success = project_service.update_project(args.name, args.new_name or args.name, args.new_description or "")
                    if success:
                        print(f"Project '{args.name}' updated successfully.")
                    else:
                        print(f"Error: Project '{args.name}' not found.")
                except ValueError as e:
                    print(f"Error: {e}")
            elif args.command == "add-task":
                try:
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
                    success = task_service.update_task(args.project_name, args.task_name, args.new_name or args.task_name, args.new_description or "", args.status or task.status, args.deadline)
                    if success:
                        print(f"Task '{args.task_name}' updated successfully in project '{args.project_name}'.")
                    else:
                        print(f"Error: Task '{args.task_name}' not found in project '{args.project_name}'.")
                except ValueError as e:
                    print(f"Error: {e}")
            elif args.command == "change-task-status":
                try:
                    success = task_service.change_task_status(args.project_name, args.task_name, args.status)
                    if success:
                        print(f"Status of task '{args.task_name}' in project '{args.project_name}' changed to '{args.status}'.")
                    else:
                        print(f"Error: Task '{args.task_name}' not found in project '{args.project_name}'.")
                except ValueError as e:
                    print(f"Error: {e}")
            elif args.command == "delete-task":
                try:
                    success = task_service.delete_task(args.project_name, args.task_id)
                    if success:
                        print(f"Task with ID '{args.task_id}' deleted successfully from project '{args.project_name}'.")
                    else:
                        print(f"Error: Task with ID '{args.task_id}' not found in project '{args.project_name}'.")
                except Exception as e:
                    print(f"Error: {e}")
            elif args.command == "list-tasks":
                try:
                    tasks = task_service.list_tasks(args.project_name)
                    if tasks:
                        print(f"Tasks in project '{args.project_name}':")
                        for task in tasks:
                            print(f"- {task.title}: {task.description} (Status: {task.status}) (id: {task.id})")
                    else:
                        print(f"No tasks found in project '{args.project_name}'.")
                except ValueError as e:
                    print(f"Error: {e}")
            elif args.command == "list-projects":
                projects = project_service.list_projects()
                if projects:
                    for project in projects:
                        print(f"Project: {project.id} - {project.name} - {project.description}")
                else:
                    print("No projects found.")
            elif args.command == "delete-project":
                try:
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
    main()