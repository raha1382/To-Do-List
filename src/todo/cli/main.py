import argparse
from todo.core.project_service import Project_Service
from todo.core.task_service import Task_Service
from todo.storage.in_memory_storage import In_Memory_Storage

def main():
    storage = In_Memory_Storage()
    project_service = Project_Service(storage)
    task_service = Task_Service(storage)

    parser = argparse.ArgumentParser(description="ToDo List CLI Application")
    subparsers = parser.add_subparsers(dest="command")

    # Create project command
    parser_create_project = subparsers.add_parser("create-project", help="Create a new project")
    parser_create_project.add_argument("--name", required=True, help="Name of the project")
    parser_create_project.add_argument("--description", help="Description of the project")

    # Add task command
    parser_add_task = subparsers.add_parser("add-task", help="Add a task to a project")
    parser_add_task.add_argument("--project-name", required=True, help="Name of the project")
    parser_add_task.add_argument("--task-name", required=True, help="Name of the task")
    parser_add_task.add_argument("--description", help="Description of the task")

    # List projects command
    parser_list_projects = subparsers.add_parser("list-projects", help="List all projects")

    # Delete project command
    parser_delete_project = subparsers.add_parser("delete-project", help="Delete a project")
    parser_delete_project.add_argument("--name", required=True, help="Name of the project to delete")

    args = parser.parse_args()

    if args.command == "create-project":
        try:
            project = project_service.create_project(args.name, args.description or "")
            print(f"Project '{project.name}' created successfully.")
        except ValueError as e:
            print(f"Error: {e}")
    elif args.command == "add-task":
        try:
            success = project_service.add_task_to_project(args.project_name, args.task_name, args.description or "")
            if success:
                print(f"Task '{args.task_name}' added to project '{args.project_name}'.")
            else:
                print(f"Error: Project '{args.project_name}' not found.")
        except ValueError as e:
            print(f"Error: {e}")
    elif args.command == "list-projects":
        projects = project_service.list_projects()
        if projects:
            for project in projects:
                print(f"Project: {project.name} - {project.description}")
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

if __name__ == "__main__":
    main()