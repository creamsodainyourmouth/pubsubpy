from abc import ABC, abstractmethod


class IChannel(ABC):

    @abstractmethod
    def add_event_listener(self, event_type, handler):
        pass

    @abstractmethod
    def remove_event_listener(self, event_type, handler):
        pass

    @abstractmethod
    def emit_event(self, event_type, payload):
        pass

    @abstractmethod
    def name(self):
        pass

    @abstractmethod
    def id(self):
        pass
