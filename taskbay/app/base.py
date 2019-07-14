# FIXME: decouple from Celery
from celery import Celery
from taskbay.event.base import TaskEvent

TASKBAY_DEFAULT_CONFIG_MODULE = 'taskbay_config'


class TaskBay(Celery):

    task_cls = 'taskbay.task.base:_Task'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # init local event listners if there is a setting
        # init scheduler if there is a setting
        # init eventbus if there is a setting
        # init sender if there is a setting

    # TODO handle long result in listener (long result listener)
    # TODO handle error in listener
    def notify(self, event: TaskEvent):
        for l in self.event_listeners():
            l.on_event(event)

    def _event_listeners(self):
        # TODO load local settings to construct listners in app object
        return []


# TODO: support config from env variable
# load default setting in PYTHON_PATH
default_app = TaskBay(config_source=TASKBAY_DEFAULT_CONFIG_MODULE)
