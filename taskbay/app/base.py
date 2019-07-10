from celery import Celery


# FIXME: decouple from Celery
class TaskBay(Celery):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # init local event listners if there is a setting
        # init scheduler if there is a setting
        # init eventbus if there is a setting
        # init sender if there is a setting

    # TODO handle long result in listener (long result listener)
    # TODO handle error in listener
    def notify(self, event):
        for l in self.event_listeners:
            l.execute(event)

    @property
    def event_listeners(self):
        # TODO load local settings to construct listners in app object
        return []


# load default setting in PYTHON_PATH
default_app = TaskBay(config_source=None)
