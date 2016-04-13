from nameko.events import EventDispatcher
from nameko.rpc import rpc


class EventDispatcher(object):
    name = "event_dispatcher"
    dispatch = EventDispatcher()

    @rpc
    def send_event(self, payload):
        self.dispatch(payload.get('type'), payload)
