from ..utils.utils import (
    MAX_PROJECT_NAME_WORDS,
    MAX_PROJECT_DESCRIPTION_WORDS,
    MAX_TASK_TITLE_WORDS,
    MAX_TASK_DESCRIPTION_WORDS,
    TASK_STATUS
)
from datetime import datetime

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

def validate_deadline(deadline: datetime | str | None) -> datetime | None:
    """Validate the deadline format and ensure it is after the current time."""
    if deadline is None:
        return None
    if isinstance(deadline, str):
        try:
            deadline_datetime = datetime.strptime(deadline, "%Y-%m-%d")
        except ValueError:
            raise ValueError("Deadline must be in 'YYYY-MM-DD' format or a valid datetime object.")
    elif isinstance(deadline, datetime):
        deadline_datetime = deadline
    else:
        raise ValueError("Deadline must be a string in 'YYYY-MM-DD' format, a datetime object, or None.")

    # Check if deadline is after current time
    current_time = datetime.now()
    if deadline_datetime <= current_time:
        raise ValueError("Deadline must be a future date and time, not in the past or present.")

    return deadline_datetime