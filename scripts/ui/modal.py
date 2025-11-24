#!/usr/bin/env python3
"""
Reusable Modal System for Sci-UX

Provides a flexible modal dialog system that can be used throughout
the application for various purposes like file dialogs, confirmations, etc.
"""

import js
from pyodide.ffi import create_proxy
from py_html.elements import *
from py_html.css import CSS
from py_dom import events, on_click
from typing import Dict, List, Optional, Callable, Any


class Modal:
    """A flexible modal dialog component."""
    
    def __init__(self, 
                 modal_id: str, 
                 title: str = "Modal",
                 size: str = "medium",
                 closeable: bool = True):
        """
        Initialize a modal.
        
        Args:
            modal_id: Unique identifier for the modal
            title: Modal title
            size: Modal size - 'small', 'medium', 'large', or 'full'
            closeable: Whether the modal can be closed with X button
        """
        self.modal_id = modal_id
        self.title = title
        self.size = size
        self.closeable = closeable
        self.on_close_callback = None
        self.on_confirm_callback = None
        
    def set_on_close(self, callback: Callable):
        """Set callback for when modal is closed."""
        self.on_close_callback = callback
        
    def set_on_confirm(self, callback: Callable):
        """Set callback for confirm action."""
        self.on_confirm_callback = callback
    
    def create_header(self) -> Div:
        """Create modal header."""
        header_content = [H3(self.title, class_="modal-title")]
        
        if self.closeable:
            header_content.append(
                Button("×", class_="modal-close", id=f"{self.modal_id}-close")
            )
        
        return Div(class_="modal-header").add(*header_content)
    
    def create_body(self, content) -> Div:
        """Create modal body with custom content."""
        if isinstance(content, (list, tuple)):
            return Div(class_="modal-body").add(*content)
        else:
            return Div(class_="modal-body").add(content)
    
    def create_footer(self, buttons: List[Dict[str, Any]] = None) -> Div:
        """Create modal footer with custom buttons."""
        if not buttons:
            buttons = [{"text": "Close", "class": "modal-btn-secondary", "id": f"{self.modal_id}-close"}]
        
        button_elements = []
        for btn in buttons:
            button_elements.append(
                Button(
                    btn["text"], 
                    class_=f"modal-btn {btn.get('class', 'modal-btn-primary')}", 
                    id=btn["id"]
                )
            )
        
        return Div(class_="modal-footer").add(*button_elements)
    
    def render(self, body_content, footer_buttons: List[Dict[str, Any]] = None) -> Div:
        """Render the complete modal."""
        size_class = f"modal-{self.size}"
        
        return Div(class_="modal-overlay", id=self.modal_id, style="display: none;").add(
            Div(class_=f"modal-content {size_class}").add(
                self.create_header(),
                self.create_body(body_content),
                self.create_footer(footer_buttons)
            )
        )
    
    def show(self):
        """Show the modal."""
        modal_element = js.document.getElementById(self.modal_id)
        if modal_element:
            modal_element.style.display = "flex"
    
    def hide(self):
        """Hide the modal."""
        modal_element = js.document.getElementById(self.modal_id)
        if modal_element:
            modal_element.style.display = "none"
    
    def remove(self):
        """Remove the modal from DOM."""
        modal_element = js.document.getElementById(self.modal_id)
        if modal_element:
            modal_element.remove()
    
    def setup_handlers(self):
        """Set up event handlers for the modal."""
        def handle_close(event):
            if self.on_close_callback:
                self.on_close_callback()
            else:
                self.hide()
        
        def handle_confirm(event):
            if self.on_confirm_callback:
                self.on_confirm_callback()
            else:
                self.hide()
        
        def handle_overlay_click(event):
            if event.target.id == self.modal_id:
                handle_close(event)
        
        # Set up close button handlers
        if self.closeable:
            on_click(f"{self.modal_id}-close", handle_close)
        
        # Set up confirm button if it exists
        confirm_btn = js.document.getElementById(f"{self.modal_id}-confirm")
        if confirm_btn:
            on_click(f"{self.modal_id}-confirm", handle_confirm)
        
        # Set up cancel button if it exists
        cancel_btn = js.document.getElementById(f"{self.modal_id}-cancel")
        if cancel_btn:
            on_click(f"{self.modal_id}-cancel", handle_close)
        
        # Close on overlay click
        events.add_listener(self.modal_id, 'click', handle_overlay_click)


class FileExplorerModal(Modal):
    """Specialized modal for file exploration."""
    
    def __init__(self, modal_id: str = "file-explorer-modal", title: str = "Select File"):
        super().__init__(modal_id, title, size="large")
        self.selected_file = None
        self.on_file_select_callback = None
    
    def set_on_file_select(self, callback: Callable):
        """Set callback for when a file is selected."""
        self.on_file_select_callback = callback
    
    def create_with_file_explorer(self):
        """Create modal with embedded file explorer."""
        from ui.applets.file_explorer import create_file_explorer
        
        # Create file explorer instance for the modal
        modal_explorer = create_file_explorer(f"{self.modal_id}-fe")
        
        # Custom footer buttons for file selection
        footer_buttons = [
            {"text": "Cancel", "class": "modal-btn-secondary", "id": f"{self.modal_id}-cancel"},
            {"text": "Open Selected", "class": "modal-btn-primary", "id": f"{self.modal_id}-confirm", "disabled": True}
        ]
        
        return self.render(modal_explorer.render(), footer_buttons)
    
    def setup_file_selection_handlers(self):
        """Set up handlers specific to file selection."""
        # Set up basic modal handlers
        self.setup_handlers()
        
        # Set up file explorer handlers
        from ui.applets.file_explorer import FileExplorer
        explorer = FileExplorer(f"{self.modal_id}-fe")
        
        # Add file explorer styles
        if not js.document.getElementById('file-explorer-modal-styles'):
            fe_styles = explorer.get_styles()
            style_content = "\n".join(str(style) for style in fe_styles)
            style_element = f'<style id="file-explorer-modal-styles">{style_content}</style>'
            js.document.head.insertAdjacentHTML('beforeend', style_element)
        
        explorer.setup_event_handlers()
        
        # Override the file double-click to select instead of navigate
        def handle_file_selection(event):
            row = event.target.closest('.fe-item-row')
            if row:
                item_name = row.getAttribute('data-name')
                item_type = row.getAttribute('data-type')
                
                if item_type == 'file':
                    # Enable the Open button
                    open_btn = js.document.getElementById(f"{self.modal_id}-confirm")
                    if open_btn:
                        open_btn.disabled = False
                    
                    # Store selected file info
                    current_dir = explorer.fs.get_current_directory()
                    file_item = current_dir.get_child(item_name)
                    if file_item:
                        self.selected_file = {
                            'name': item_name,
                            'content': file_item.content,
                            'path': explorer.fs.get_path_string() + '/' + item_name if explorer.fs.get_path_string() != '/' else '/' + item_name
                        }
        
        # Override confirm handler to return selected file
        def handle_confirm_with_file(event):
            if self.selected_file and self.on_file_select_callback:
                self.on_file_select_callback(self.selected_file)
            self.hide()
        
        # Set up the overridden confirm handler
        on_click(f"{self.modal_id}-confirm", handle_confirm_with_file)
        
        # Add selection handler to file rows
        file_rows = js.document.querySelectorAll(f"#{self.modal_id}-fe .fe-item-row")
        for row in file_rows:
            click_proxy = create_proxy(handle_file_selection)
            row.addEventListener('click', click_proxy)


def get_modal_styles() -> List[CSS]:
    """Get CSS styles for the modal system."""
    return [
        # Base modal styles
        CSS.class_("modal-overlay",
            position="fixed",
            top="0",
            left="0",
            width="100%", 
            height="100%",
            background="rgba(0, 0, 0, 0.5)",
            display="flex",
            justify_content="center",
            align_items="center",
            z_index="1000"
        ),
        
        CSS.class_("modal-content",
            background="white",
            border_radius="8px",
            box_shadow="0 4px 20px rgba(0, 0, 0, 0.3)",
            display="flex",
            flex_direction="column",
            max_height="90vh",
            overflow="hidden"
        ),
        
        # Modal sizes
        CSS.class_("modal-small",
            width="400px",
            max_width="90vw"
        ),
        
        CSS.class_("modal-medium",
            width="600px",
            max_width="90vw"
        ),
        
        CSS.class_("modal-large",
            width="900px",
            max_width="95vw"
        ),
        
        CSS.class_("modal-full",
            width="95vw",
            height="90vh"
        ),
        
        # Modal components
        CSS.class_("modal-header",
            padding="20px",
            border_bottom="1px solid #eee",
            display="flex",
            justify_content="space-between",
            align_items="center",
            background="#f8f9fa"
        ),
        
        CSS.selector(".modal-header h3",
            margin="0",
            color="#333",
            font_size="18px"
        ),
        
        CSS.class_("modal-close",
            background="none",
            border="none",
            font_size="24px",
            cursor="pointer",
            color="#666",
            padding="0",
            width="30px",
            height="30px",
            display="flex",
            align_items="center",
            justify_content="center",
            border_radius="50%"
        ),
        
        CSS.selector(".modal-close:hover",
            color="#000",
            background="#e9ecef"
        ),
        
        CSS.class_("modal-body",
            padding="20px",
            overflow="auto",
            flex="1"
        ),
        
        CSS.class_("modal-footer",
            padding="20px",
            border_top="1px solid #eee",
            display="flex",
            justify_content="flex-end",
            gap="10px",
            background="#f8f9fa"
        ),
        
        # Modal buttons
        CSS.class_("modal-btn",
            padding="8px 16px",
            border="none",
            border_radius="4px",
            cursor="pointer",
            font_size="14px",
            transition="background 0.2s"
        ),
        
        CSS.class_("modal-btn-primary",
            background="#007bff",
            color="white"
        ),
        
        CSS.selector(".modal-btn-primary:hover:not(:disabled)",
            background="#0056b3"
        ),
        
        CSS.class_("modal-btn-secondary",
            background="#6c757d",
            color="white"
        ),
        
        CSS.selector(".modal-btn-secondary:hover",
            background="#545b62"
        ),
        
        CSS.selector(".modal-btn:disabled",
            opacity="0.5",
            cursor="not-allowed"
        )
    ]


def ensure_modal_styles():
    """Ensure modal styles are loaded in the document."""
    if not js.document.getElementById('modal-system-styles'):
        styles = get_modal_styles()
        style_content = "\n".join(str(style) for style in styles)
        style_element = f'<style id="modal-system-styles">{style_content}</style>'
        js.document.head.insertAdjacentHTML('beforeend', style_element)


def create_simple_modal(modal_id: str, title: str, content, buttons: List[Dict[str, Any]] = None) -> Modal:
    """Helper function to create a simple modal quickly."""
    ensure_modal_styles()
    modal = Modal(modal_id, title)
    modal_html = modal.render(content, buttons)
    js.document.body.insertAdjacentHTML('beforeend', str(modal_html))
    modal.setup_handlers()
    return modal


def create_file_explorer_modal(modal_id: str = "file-explorer-modal") -> FileExplorerModal:
    """Helper function to create a file explorer modal."""
    ensure_modal_styles()
    modal = FileExplorerModal(modal_id)
    modal_html = modal.create_with_file_explorer()
    js.document.body.insertAdjacentHTML('beforeend', str(modal_html))
    modal.setup_file_selection_handlers()
    return modal