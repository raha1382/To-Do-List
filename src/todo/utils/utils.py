import os
from dotenv import load_dotenv

# Load environment variables from .env file in the current directory
load_dotenv()  # Looks for .env in src/todo/

# Load numeric variables with default values (from .env.example)
MAX_NUMBER_OF_PROJECTS = int(os.getenv("MAX_NUMBER_OF_PROJECTS", 8))
MAX_NUMBER_OF_TASKS = int(os.getenv("MAX_NUMBER_OF_TASKS", 40))
MAX_PROJECT_NAME_WORDS = int(os.getenv("MAX_PROJECT_NAME_WORDS", 30))
MAX_PROJECT_DESCRIPTION_WORDS = int(os.getenv("MAX_PROJECT_DESCRIPTION_WORDS", 150))
MAX_TASK_TITLE_WORDS = int(os.getenv("MAX_TASK_TITLE_WORDS", 30))
MAX_TASK_DESCRIPTION_WORDS = int(os.getenv("MAX_TASK_DESCRIPTION_WORDS", 150))

# Load and parse TASK_STATUS
task_status_str = os.getenv("TASK_STATUS", "todo,doing,done")
TASK_STATUS = task_status_str.split(',')