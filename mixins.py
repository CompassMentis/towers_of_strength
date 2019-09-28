from pygame import (
    MOUSEBUTTONDOWN,
    MOUSEBUTTONUP,
    MOUSEMOTION,
)


class MouseEventHandlerMixin:
    """
    Base class/Interface for handling mouse-events.
    """
    def _handle_mousedown(self, event):
        raise NotImplementedError

    def _handle_mouseup(self, event):
        raise NotImplementedError

    def _handle_mousemove(self, event):
        raise NotImplementedError

    def handle_mouse_event(self, event):
        handler_map = {
            MOUSEBUTTONDOWN: self._handle_mousedown,
            MOUSEBUTTONUP: self._handle_mouseup,
            MOUSEMOTION: self._handle_mousemove,
        }

        handler_map[event.type](event)
