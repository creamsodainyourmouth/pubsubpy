import types
from typing import Any, Callable, TypeVar, ClassVar
from dataclasses import dataclass, field

from pubsub.IChannel import IChannel
from pubsub.exceptions import ListenerDecoratorIsNotApplied


T = TypeVar('T')
EventType = T
EventPayload = dict
Receiver = Callable[[EventType, EventPayload, IChannel], None]
ReceiverId = str


def get_object_id(obj: T) -> str:
    return str(id(obj))


@dataclass
class Channel(IChannel):
    _name: str
    _listeners: dict[EventType, dict[ReceiverId, Receiver]] = field(default_factory=dict, init=False)
    _id: str = field(init=False)
    _INNER_RECEIVING_EVENTS: ClassVar[str] = "__receiving_events__"

    def __post_init__(self):
        self._id = get_object_id(self)

    def remove_event_listener(self, event_type: EventType, receiver: Receiver):
        if not self._listeners.get(event_type):
            return
        self._listeners[event_type].pop(get_object_id(receiver), None)

    def emit_event(self, event_type: EventType, payload: EventPayload):
        if not self._listeners.get(event_type):
            return
        for receiver in self._listeners[event_type].values():
            receiver(event_type, payload, self)

    def add_event_listener(self, event_type: EventType, receiver: Receiver):
        if not self._listeners.get(event_type):
            self._listeners[event_type] = dict()
        self._listeners[event_type][get_object_id(receiver)] = receiver

    def listen(self, event_type: EventType):
        def decorator(method: Receiver):
            receiving_events_by_channel = getattr(method, self._INNER_RECEIVING_EVENTS, {})
            if not receiving_events_by_channel.get(self._id):
                receiving_events_by_channel[self._id] = []
            receiving_events_by_channel[self._id].append(event_type)
            setattr(method, self._INNER_RECEIVING_EVENTS, receiving_events_by_channel)
            return method

        return decorator

    def listener(self, init_method):
        def init_wrapper(instance, *args, **kwargs):
            init_method(instance, *args, **kwargs)
            for method_name in dir(instance):
                method = getattr(instance, method_name)
                if not hasattr(method, self._INNER_RECEIVING_EVENTS):
                    continue
                receiving_events: dict = getattr(method, self._INNER_RECEIVING_EVENTS)
                receiving_events_by_channel = receiving_events.get(self._id, None)
                if receiving_events_by_channel is None:
                    continue
                for event_type in receiving_events_by_channel:
                    self.add_event_listener(event_type, method)

        return init_wrapper

    @property
    def name(self) -> str:
        return self._name

    @property
    def id(self) -> str:
        return self._id

    def __str__(self) -> str:
        return f"Channel ({self._id}): {self._name}"
