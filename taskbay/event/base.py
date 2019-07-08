from datetime import datetime
from enum import Enum


class TaskEvent(object):

    def __init__(self, task_id, task_name, event_name, event_at, machine=None, result=None, error=None, tag=None,
                 time_for_retry=None):
        self.task_id = task_id
        self.task_name = task_name
        self.event_name = event_name
        self.event_at = event_at or datetime.now()
        self.machine = machine
        self.result = result
        self.error = error
        self.tag = tag
        self.time_for_retry = time_for_retry


# build-in task names
class TaskEventNames(Enum):
    START = 'STARTED'
    FAIL = 'FAILED'
    RETRY = 'RETRY'
    COMPLETE = 'COMPLETED'
