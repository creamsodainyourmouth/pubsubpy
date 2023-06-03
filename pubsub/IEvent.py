from dataclasses import dataclass, field
from abc import ABC, abstractmethod
from typing import TypeVar

T = TypeVar('T')
EventType = T
EventPayload = dict


@dataclass
class IEvent(ABC):
    _type: EventType
    _payload: EventPayload

    @abstractmethod
    @property
    def type(self):
        pass

    @property
    @abstractmethod
    def payload(self):
        pass

