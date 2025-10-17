from ..utils.utils import (
    MAX_PROJECT_NAME_WORDS,
    MAX_PROJECT_DESCRIPTION_WORDS,
    MAX_TASK_TITLE_WORDS,
    MAX_TASK_DESCRIPTION_WORDS,
    TASK_STATUS
)

def validate_name_of_project(name: str) -> str:
    if len(name.split()) > MAX_PROJECT_NAME_WORDS:
        raise ValueError(f"Project name exceeds {MAX_PROJECT_NAME_WORDS} words")
    return name

def validate_description_of_project(description: str) -> str:
    if len(description.split()) > MAX_PROJECT_DESCRIPTION_WORDS:
        raise ValueError(f"Project description exceeds {MAX_PROJECT_DESCRIPTION_WORDS} words")
    return description

def validate_name_of_task(name: str) -> str:
    if len(name.split()) > MAX_TASK_TITLE_WORDS:
        raise ValueError(f"Task title exceeds {MAX_TASK_TITLE_WORDS} words")
    return name

def validate_description_of_task(description: str) -> str:
    if len(description.split()) > MAX_TASK_DESCRIPTION_WORDS:
        raise ValueError(f"Task description exceeds {MAX_TASK_DESCRIPTION_WORDS} words")
    return description

def validate_status_of_task(status: str) -> str:
    lower_case_status = status.lower()
    if lower_case_status not in TASK_STATUS:
        raise ValueError(f"Invalid status: must be one of {', '.join(TASK_STATUS)}.")
    return lower_case_status