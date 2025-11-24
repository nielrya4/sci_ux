"""DOM manipulation utilities for Pyodide/JavaScript integration."""
from .events import EventHandler, events, on_click, on_submit, on_keydown, on_escape

__all__ = ['EventHandler', 'events', 'on_click', 'on_submit', 'on_keydown', 'on_escape']