from enum import Enum


# TODO think: should we allow customized states?
class TaskState(Enum):
    READY = 0
    QUEUED = 10
    RUNNING = 20
    READY_FOR_RETRY = 30
    COMPLETED = 100
    FAILED = 200
