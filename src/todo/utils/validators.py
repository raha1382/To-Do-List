from ..utils.utils import (
    MAX_PROJECT_NAME_WORDS,
    MAX_PROJECT_DESCRIPTION_WORDS,
    MAX_TASK_TITLE_WORDS,
    MAX_TASK_DESCRIPTION_WORDS,
    TASK_STATUS
)

def validate_name_of_project(name: str) -> None:
    if len(name.split()) > MAX_PROJECT_NAME_WORDS : 
        raise ValueError(f"Project name exceeds {MAX_PROJECT_NAME_WORDS} words")
    
def validate_description_of_project(description: str) -> None:
    if len(description.split()) > MAX_PROJECT_DESCRIPTION_WORDS : 
        raise ValueError(f"Project name exceeds {MAX_PROJECT_DESCRIPTION_WORDS} words")
    
def validate_name_of_task(name: str) -> None:
    if len(name.split()) > MAX_TASK_TITLE_WORDS : 
        raise ValueError(f"Project name exceeds {MAX_TASK_TITLE_WORDS} words")
    
def validate_description_of_task(description: str) -> None:
    if len(description.split()) > MAX_TASK_DESCRIPTION_WORDS : 
        raise ValueError(f"Project name exceeds {MAX_TASK_DESCRIPTION_WORDS} words")
    
def validate_status_of_task(status: str) -> None:
    lower_case_status = status.lower()
    if lower_case_status not in TASK_STATUS:
        raise ValueError(f"Invalid status: must be one of {TASK_STATUS}")
    else:
        return lower_case_status