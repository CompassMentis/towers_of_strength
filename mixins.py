class MouseEventHandlerMixin:
    "Base class/Interface for handling mouse-button-1 events."
    def handle_mousedown(self):
        raise NotImplementedError

    def handle_mouseup(self):
        raise NotImplementedError
