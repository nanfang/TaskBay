import os
import datetime
import logging
import socket
import psutil
from datetime import datetime, timedelta

from celery.app.task import Task
from celery.exceptions import Retry
from taskbay.event.base import TaskEventNames, TaskEvent

logger = logging.getLogger(__name__)


# FIXME: current version is coupled with Celery, need to decouple it when I figure out a solution
class _Task(Task):
    """task accept a process_event attribute as the celery task name
    to deliver event
    """
    abstract = True

    # suppress celery result backend. the COMPLETE event will carry the result (less than 2000 bytes)
    # TODO: support extra storage for larger result than 2000 bytes
    ignore_result = True

    # suppress celery task chain. the task chain (workflow) will be done by event driven architecture
    trail = False

    def __init__(self) -> None:
        super(_Task, self).__init__()

    def __call__(self, *args, **kwargs):
        self._start_time, self._start_mem = self._runtime_stats()
        self._emit_event(TaskEventNames.START, event_at=self._start_time)
        logger.info('Task %s[%s] started', self.task_name, self.task_id)
        val = self._inner_call(*args, **kwargs)
        return val

    def _execute_task(self, *args, **kwargs):
        try:
            return super(_Task, self).__call__(*args, **kwargs)
        except (Retry, self.MaxRetriesExceededError):
            raise
        except Exception as ex:
            logger.error(
                'Fail to run task[id=%s, task=%s, market=%s]',
                self.task_id, self.task_name, self.market,
                exc_info=True)
            if self.is_autoretry:
                raise self.retry(exc=ex)
            else:
                raise

    # override the celery retry to use event driven retry by taskbay
    def retry(self, args=None, kwargs=None, exc=None,
              throw=True, eta=None, countdown=None, max_retries=None,
              **options):
        _end_time, _end_mem = self._runtime_stats()

        if countdown is None:
            countdown = self.default_retry_delay
        time_for_retry = eta or datetime.now() + timedelta(seconds=countdown)

        # max retry times verification
        retries = self.request.retries
        max_retries = self.max_retries if max_retries is None else max_retries
        if retries + 1 > max_retries:
            raise self.MaxRetriesExceededError(
                "Exceed max retry times for {task_name} id: {task_id} max_retries: {max_retries}".format(
                    task_name=self.task_name, task_id=self.task_id, max_retries=max_retries))
        logger.info(
            'Task %s[%s] failed and to retry, time spent(sec): %.2f, memory consumed(byte): %s',
            self.task_name, self.task_id, _end_time - self._start_time, _end_mem - self._start_mem
        )

        self._emit_event(TaskEventNames.RETRY, _end_time, error=exc, time_for_retry=time_for_retry)
        return Retry(exc=exc, when=eta or countdown)

    def on_success(self, retval, task_id, args, kwargs):
        _end_time, _end_mem = self._runtime_stats()
        logger.info(
            'Task %s[%s] succeeded, time spent(sec): %.2f, memory consumed(byte): %s',
            self.task_name, self.task_id, _end_time - self._start_time, _end_mem - self._start_mem
        )
        self._emit_event(TaskEventNames.COMPLETE, self._end_time, result=retval)

    def on_failure(self, exc, task_id, args, kwargs, einfo):
        _end_time, _end_mem = self._runtime_stats()
        logger.info(
            'Task %s[%s] failed finally, time spent(sec): %.2f, memory consumed(byte): %s',
            self.task_name, self.task_id, _end_time - self._start_time, _end_mem - self._start_mem
        )
        self._emit_event(TaskEventNames.FAIL, _end_time, error=einfo)

    def on_retry(self, exc, task_id, args, kwargs, einfo):
        # not need for this celery hook, retry is handled by taskbay
        pass

    def _emit_event(self, event_name, event_at, result=None, error=None, time_for_retry=None):
        if self.task_id is None:
            # this only happen when we call the task function directly
            return
        event = TaskEvent(
            task_id=self.task_id,
            task_name=self.task_name,
            event_name=event_name,
            event_at=event_at,
            machine=self.machine,
            tag=self.request.tag,
            result=result, #TODO handle long result
            error=self._format_and_truncate_error(error),
            time_for_retry=time_for_retry
        )

        # TODO send event to event bus and other listeners
        pass

    @property
    def task_id(self):
        return int(self.request.id)

    @property
    def task_name(self):
        return self.name

    @property
    def machine(self):
        return socket.gethostname()

    @property
    def current_queue(self):
        if self.request.delivery_info:
            return self.request.delivery_info.get('exchange')
        return None

    @property
    def is_autoretry(self):
        return getattr(self, 'autoretry', False)

    @staticmethod
    def _format_and_truncate_error(error):
        # TODO
        return error

    @staticmethod
    def _runtime_stats():
        return datetime.now(), psutil.Process(os.getpid()).memory_info().rss
