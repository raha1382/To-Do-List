from enum import Enum as PyEnum

class TaskStatus(PyEnum):
    TODO = "todo"
    DOING = "doing"
    DONE = "done"