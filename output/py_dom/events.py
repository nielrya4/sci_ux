"""Event handling utilities for Pyodide/JavaScript integration."""
import js
from pyodide.ffi import create_proxy

class EventHandler:
    """Utility class for managing event handlers with automatic proxy creation."""
    
    def __init__(self):
        self._handlers = {}
    
    def add_listener(self, element_id, event_type, handler):
        """Add event listener to element with automatic proxy creation."""
        element = js.document.getElementById(element_id)
        if element:
            proxy = create_proxy(handler)
            element.addEventListener(event_type, proxy)
            # Store proxy to prevent garbage collection
            self._handlers[f"{element_id}_{event_type}"] = proxy
            return proxy
        return None
    
    def add_document_listener(self, event_type, handler):
        """Add document-level event listener with automatic proxy creation."""
        proxy = create_proxy(handler)
        js.document.addEventListener(event_type, proxy)
        self._handlers[f"document_{event_type}"] = proxy
        return proxy
    
    def remove_listener(self, element_id, event_type):
        """Remove event listener and clean up proxy."""
        key = f"{element_id}_{event_type}"
        if key in self._handlers:
            element = js.document.getElementById(element_id)
            if element:
                element.removeEventListener(event_type, self._handlers[key])
            del self._handlers[key]
    
    def remove_document_listener(self, event_type):
        """Remove document-level event listener and clean up proxy."""
        key = f"document_{event_type}"
        if key in self._handlers:
            js.document.removeEventListener(event_type, self._handlers[key])
            del self._handlers[key]
    
    def clear_all(self):
        """Remove all event listeners and clean up proxies."""
        self._handlers.clear()

# Global event handler instance
events = EventHandler()

# Convenience functions for common patterns
def on_click(element_id, handler):
    """Add click event listener to element."""
    return events.add_listener(element_id, 'click', handler)

def on_submit(element_id, handler):
    """Add submit event listener to element."""
    return events.add_listener(element_id, 'submit', handler)

def on_keydown(handler, element_id=None):
    """Add keydown event listener (document-level if no element_id)."""
    if element_id:
        return events.add_listener(element_id, 'keydown', handler)
    else:
        return events.add_document_listener('keydown', handler)

def on_escape(handler):
    """Add escape key handler (document-level)."""
    def escape_handler(event):
        if event.key == 'Escape':
            handler(event)
    return events.add_document_listener('keydown', escape_handler)