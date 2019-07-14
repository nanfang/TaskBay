from abc import abstractmethod, ABC

from taskbay.event.base import TaskEvent


class BaseEventListener(ABC):

    def __init__(self, app):
        self.app = app

    @abstractmethod
    def on_event(self, event) -> None:
        raise NotImplementedError()


class EventLoggingListener(BaseEventListener):

    def on_event(self, event: TaskEvent) -> None:
        # TODO: impl
        pass


class InMemoryEventBrokerListener(BaseEventListener):
    """
    Call event bus eagerly, only useful for testing
    """
    def on_event(self, event: TaskEvent) -> None:
        # TODO: make below to work
        self.app.event_bus.handle(event)


class RemoteEventBrokerListener(BaseEventListener):
    """
    send the event to remote broker which connects to the event bus.
    """
    def on_event(self, event: TaskEvent) -> None:
        # TODO: impl
        pass
