from abc import ABC, abstractmethod

from pubsub.IEvent import IEvent


class IChannel(ABC):

    @abstractmethod
    def add_event_listener(self, event_type, handler):
        pass

    @abstractmethod
    def remove_event_listener(self, event_type, handler):
        pass

    @abstractmethod
    def emit_event(self, event: IEvent):
        pass

    @abstractmethod
    def name(self):
        pass

    @abstractmethod
    def id(self):
        pass
