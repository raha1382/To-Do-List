from ..utils.utils import (
    MAX_PROJECT_NAME_WORDS,
    MAX_PROJECT_DESCRIPTION_WORDS,
    MAX_TASK_TITLE_WORDS,
    MAX_TASK_DESCRIPTION_WORDS,
    TASK_STATUS
)
from datetime import datetime
from ..model.enums import TaskStatus

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
    status = status.lower().strip()
    if status not in {s.value for s in TaskStatus}:
        raise ValueError(f"Invalid status: must be one of {', '.join(s.value for s in TaskStatus)}.")
    return status  


def validate_deadline(deadline: datetime | str | None) -> datetime | None:
    """Validate the deadline format and ensure it is after the current time (date + time)."""
    if deadline is None:
        return None

    if isinstance(deadline, str):
        for fmt in ("%Y-%m-%d %H:%M", "%Y-%m-%d %H:%M:%S", "%Y-%m-%d"):
            try:
                deadline_datetime = datetime.strptime(deadline, fmt)
                break
            except ValueError:
                deadline_datetime = None
        if not deadline_datetime:
            raise ValueError(
                "Deadline must be in one of the following formats: "
                "'YYYY-MM-DD', 'YYYY-MM-DD HH:MM', or 'YYYY-MM-DD HH:MM:SS'."
            )

    elif isinstance(deadline, datetime):
        deadline_datetime = deadline
    else:
        raise ValueError(
            "Deadline must be a string in 'YYYY-MM-DD [HH:MM[:SS]]' format, a datetime object, or None."
        )

    current_time = datetime.now()
    if deadline_datetime <= current_time:
        raise ValueError("Deadline must be a future date and time, not in the past or present.")

    return deadline_datetime