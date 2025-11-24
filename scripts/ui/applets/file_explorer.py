#!/usr/bin/env python3
"""
File Explorer Applet for Sci-UX

A Jupyter-like file browser interface that allows users to navigate,
create, rename, and delete files in a virtual file system using Pyodide.
"""

import js
from pyodide.ffi import create_proxy
from py_html.elements import *
from py_html.css import CSS
from py_dom import events, on_click
from typing import Dict, List, Optional
from datetime import datetime
import json


class PersistentStorage:
    """Handles persistent storage of the virtual file system using browser localStorage."""
    
    STORAGE_KEY = "sci_ux_filesystem"
    
    @staticmethod
    def save_filesystem(filesystem_data: dict):
        """Save filesystem data to browser localStorage."""
        try:
            json_data = json.dumps(filesystem_data)
            js.localStorage.setItem(PersistentStorage.STORAGE_KEY, json_data)
            return True
        except Exception as e:
            print(f"Error saving filesystem: {e}")
            return False
    
    @staticmethod
    def load_filesystem() -> dict:
        """Load filesystem data from browser localStorage."""
        try:
            json_data = js.localStorage.getItem(PersistentStorage.STORAGE_KEY)
            if json_data and json_data != "null":
                return json.loads(json_data)
            return None
        except Exception as e:
            print(f"Error loading filesystem: {e}")
            return None
    
    @staticmethod
    def clear_filesystem():
        """Clear filesystem data from browser localStorage."""
        try:
            js.localStorage.removeItem(PersistentStorage.STORAGE_KEY)
            return True
        except Exception as e:
            print(f"Error clearing filesystem: {e}")
            return False


class FileSystemItem:
    """Represents a file or directory in the virtual file system."""
    
    def __init__(self, name: str, item_type: str, size: int = 0, 
                 modified: Optional[str] = None, content: str = ""):
        self.name = name
        self.type = item_type  # 'file' or 'directory'
        self.size = size
        self.modified = modified or datetime.now().isoformat()
        self.content = content
        self.children: Dict[str, 'FileSystemItem'] = {}
    
    def is_directory(self) -> bool:
        return self.type == 'directory'
    
    def is_file(self) -> bool:
        return self.type == 'file'
    
    def add_child(self, item: 'FileSystemItem'):
        """Add a child item (for directories)."""
        if self.is_directory():
            self.children[item.name] = item
    
    def get_child(self, name: str) -> Optional['FileSystemItem']:
        """Get a child item by name."""
        return self.children.get(name)
    
    def remove_child(self, name: str) -> bool:
        """Remove a child item."""
        if name in self.children:
            del self.children[name]
            return True
        return False
    
    def get_extension(self) -> str:
        """Get file extension."""
        if self.is_file() and '.' in self.name:
            return self.name.split('.')[-1].lower()
        return ""
    
    def to_dict(self) -> dict:
        """Convert FileSystemItem to dictionary for serialization."""
        return {
            'name': self.name,
            'type': self.type,
            'size': self.size,
            'modified': self.modified,
            'content': self.content,
            'children': {name: child.to_dict() for name, child in self.children.items()}
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> 'FileSystemItem':
        """Create FileSystemItem from dictionary."""
        item = cls(
            name=data['name'],
            item_type=data['type'],
            size=data.get('size', 0),
            modified=data.get('modified'),
            content=data.get('content', '')
        )
        
        # Recursively create children
        if 'children' in data:
            for child_name, child_data in data['children'].items():
                child_item = cls.from_dict(child_data)
                item.add_child(child_item)
        
        return item


class VirtualFileSystem:
    """Manages a virtual file system for the browser environment with persistent storage."""
    
    def __init__(self):
        self.current_path = []
        self._load_or_create_filesystem()
    
    def _load_or_create_filesystem(self):
        """Load filesystem from storage or create default if none exists."""
        # Try to load from persistent storage
        stored_data = PersistentStorage.load_filesystem()
        
        if stored_data:
            # Load from storage
            self.root = FileSystemItem.from_dict(stored_data)
            print("Loaded filesystem from browser storage")
        else:
            # Create new filesystem with defaults
            self.root = FileSystemItem("root", "directory")
            self._setup_default_files()
            self._save_filesystem()
            print("Created new filesystem with default files")
    
    def _setup_default_files(self):
        """Create some default files and directories."""
        # Create sample notebooks
        notebooks_dir = FileSystemItem("notebooks", "directory")
        self.root.add_child(notebooks_dir)
        
        sample_nb = FileSystemItem("sample.ipynb", "file", 1024, 
                                  content='{"cells": [], "metadata": {}, "nbformat": 4}')
        notebooks_dir.add_child(sample_nb)
        
        # Create data directory
        data_dir = FileSystemItem("data", "directory")
        self.root.add_child(data_dir)
        
        csv_file = FileSystemItem("sample.csv", "file", 512,
                                content="name,age,city\nJohn,25,NYC\nJane,30,LA")
        data_dir.add_child(csv_file)
        
        # Create scripts directory
        scripts_dir = FileSystemItem("scripts", "directory")
        self.root.add_child(scripts_dir)
        
        py_file = FileSystemItem("analysis.py", "file", 256,
                                content="# Sample Python script\nimport pandas as pd\nprint('Hello Sci-UX!')")
        scripts_dir.add_child(py_file)
    
    def _save_filesystem(self):
        """Save the current filesystem to persistent storage."""
        PersistentStorage.save_filesystem(self.root.to_dict())
    
    def get_current_directory(self) -> FileSystemItem:
        """Get the current directory."""
        current = self.root
        for part in self.current_path:
            current = current.get_child(part)
            if not current or not current.is_directory():
                # Reset to root if path is invalid
                self.current_path = []
                return self.root
        return current
    
    def navigate_to(self, path: List[str]) -> bool:
        """Navigate to a specific path."""
        # Test if path exists
        current = self.root
        for part in path:
            current = current.get_child(part)
            if not current or not current.is_directory():
                return False
        
        self.current_path = path[:]
        return True
    
    def go_up(self) -> bool:
        """Navigate to parent directory."""
        if self.current_path:
            self.current_path.pop()
            return True
        return False
    
    def create_file(self, name: str, content: str = "") -> bool:
        """Create a new file in current directory."""
        current_dir = self.get_current_directory()
        if current_dir.get_child(name):
            return False  # File already exists
        
        file_item = FileSystemItem(name, "file", len(content), content=content)
        current_dir.add_child(file_item)
        self._save_filesystem()  # Save after change
        return True
    
    def create_directory(self, name: str) -> bool:
        """Create a new directory in current directory."""
        current_dir = self.get_current_directory()
        if current_dir.get_child(name):
            return False  # Directory already exists
        
        dir_item = FileSystemItem(name, "directory")
        current_dir.add_child(dir_item)
        self._save_filesystem()  # Save after change
        return True
    
    def delete_item(self, name: str) -> bool:
        """Delete a file or directory."""
        current_dir = self.get_current_directory()
        success = current_dir.remove_child(name)
        if success:
            self._save_filesystem()  # Save after change
        return success
    
    def get_current_items(self) -> List[FileSystemItem]:
        """Get items in current directory."""
        current_dir = self.get_current_directory()
        return list(current_dir.children.values())
    
    def get_path_string(self) -> str:
        """Get current path as string."""
        if not self.current_path:
            return "/"
        return "/" + "/".join(self.current_path)
    
    def reset_filesystem(self):
        """Reset the filesystem to defaults and clear storage."""
        PersistentStorage.clear_filesystem()
        self.root = FileSystemItem("root", "directory")
        self.current_path = []
        self._setup_default_files()
        self._save_filesystem()
        print("Filesystem reset to defaults")


class FileExplorer:
    """File Explorer UI component."""
    
    def __init__(self, container_id: str = "file-explorer"):
        self.container_id = container_id
        self.fs = VirtualFileSystem()
        self.selected_item = None
        print(f"Created FileExplorer instance with ID: {container_id}")  # Debug
        
    def get_file_icon(self, item: FileSystemItem) -> str:
        """Get appropriate icon for file type."""
        if item.is_directory():
            return "[DIR]"
        
        ext = item.get_extension()
        icons = {
            'py': '[PY]',
            'ipynb': '[NB]',
            'csv': '[CSV]',
            'json': '[JSON]',
            'txt': '[TXT]',
            'md': '[MD]',
            'html': '[HTML]',
            'css': '[CSS]',
            'js': '[JS]',
        }
        return icons.get(ext, '[FILE]')
    
    def format_file_size(self, size: int) -> str:
        """Format file size in human readable format."""
        if size < 1024:
            return f"{size} B"
        elif size < 1024 * 1024:
            return f"{size // 1024} KB"
        else:
            return f"{size // (1024 * 1024)} MB"
    
    def create_toolbar(self) -> Div:
        """Create file explorer toolbar."""
        return Div(class_="fe-toolbar").add(
            Button("+ New Folder", class_="fe-btn fe-btn-new-folder", id="fe-new-folder"),
            Button("+ New File", class_="fe-btn fe-btn-new-file", id="fe-new-file"),
            Button("Delete", class_="fe-btn fe-btn-delete", id="fe-delete", disabled=True),
            Button("Up", class_="fe-btn fe-btn-up", id="fe-up"),
            Button("Reset", class_="fe-btn fe-btn-reset", id="fe-reset", 
                   style="background: #dc3545; color: white; margin-left: 10px;"),
            Span(class_="fe-path-display", id="fe-path", content=self.fs.get_path_string())
        )
    
    def create_file_item_row(self, item: FileSystemItem) -> Tr:
        """Create a table row for a file system item."""
        return Tr(class_="fe-item-row", 
                 data={'name': item.name, 'type': item.type}).add(
            Td(class_="fe-item-icon").add(self.get_file_icon(item)),
            Td(class_="fe-item-name").add(item.name),
            Td(class_="fe-item-size").add(
                self.format_file_size(item.size) if item.is_file() else "-"
            ),
            Td(class_="fe-item-modified").add(
                item.modified[:19].replace('T', ' ') if item.modified else "-"
            )
        )
    
    def create_file_list(self) -> Div:
        """Create the file list table."""
        items = self.fs.get_current_items()
        
        # Sort items: directories first, then files, both alphabetically
        sorted_items = sorted(items, key=lambda x: (not x.is_directory(), x.name.lower()))
        
        table = Table(class_="fe-file-table").add(
            Thead().add(
                Tr().add(
                    Th("Type"),
                    Th("Name"),
                    Th("Size"),
                    Th("Modified")
                )
            ),
            Tbody(id="fe-file-list").add(
                *[self.create_file_item_row(item) for item in sorted_items]
            )
        )
        
        return Div(class_="fe-file-list-container").add(table)
    
    # Context menu disabled - removed to clean up UI
    
    def render(self) -> Div:
        """Render the complete file explorer."""
        return Div(class_="file-explorer", id=self.container_id).add(
            self.create_toolbar(),
            self.create_file_list()
        )
    
    def get_styles(self) -> List[CSS]:
        """Get CSS styles for the file explorer."""
        return [
            # Main container
            CSS.class_("file-explorer",
                border="1px solid #ddd",
                border_radius="8px",
                background="white",
                font_family="'Segoe UI', Tahoma, Geneva, Verdana, sans-serif",
                max_width="800px",
                box_shadow="0 2px 10px rgba(0,0,0,0.1)"
            ),
            
            # Toolbar
            CSS.class_("fe-toolbar",
                padding="10px",
                border_bottom="1px solid #eee",
                background="#f8f9fa",
                display="flex",
                gap="10px",
                align_items="center",
                border_radius="7px 7px 0 0"
            ),
            
            CSS.class_("fe-btn",
                padding="8px 12px",
                border="1px solid #ccc",
                border_radius="4px",
                background="white",
                cursor="pointer",
                font_size="14px",
                transition="background 0.2s"
            ),
            
            CSS.selector(".fe-btn:hover",
                background="#f0f0f0"
            ),
            
            CSS.selector(".fe-btn:disabled",
                opacity="0.5",
                cursor="not-allowed",
                background="#f5f5f5"
            ),
            
            CSS.class_("fe-path-display",
                margin_left="auto",
                font_family="monospace",
                background="#e9ecef",
                padding="6px 10px",
                border_radius="4px",
                color="#495057",
                font_size="14px"
            ),
            
            # File list
            CSS.class_("fe-file-list-container",
                max_height="400px",
                overflow_y="auto"
            ),
            
            CSS.class_("fe-file-table",
                width="100%",
                border_collapse="collapse"
            ),
            
            CSS.selector(".fe-file-table th",
                padding="12px 8px",
                border_bottom="2px solid #dee2e6",
                background="#f8f9fa",
                text_align="left",
                font_weight="600",
                color="#495057",
                font_size="14px"
            ),
            
            CSS.selector(".fe-file-table td",
                padding="10px 8px",
                border_bottom="1px solid #dee2e6",
                font_size="14px"
            ),
            
            CSS.class_("fe-item-row",
                cursor="pointer",
                transition="background 0.2s"
            ),
            
            CSS.selector(".fe-item-row:hover",
                background="#f8f9fa"
            ),
            
            CSS.selector(".fe-item-row.selected",
                background="#e3f2fd"
            ),
            
            CSS.class_("fe-item-icon",
                width="80px",
                text_align="center",
                font_size="12px",
                font_family="monospace",
                color="#666"
            ),
            
            CSS.class_("fe-item-name",
                font_weight="500",
                color="#212529"
            ),
            
            CSS.class_("fe-item-size",
                width="80px",
                text_align="right",
                color="#6c757d",
                font_family="monospace",
                font_size="13px"
            ),
            
            CSS.class_("fe-item-modified",
                width="150px",
                color="#6c757d",
                font_family="monospace",
                font_size="13px"
            ),
            
            # Context menu
            CSS.class_("fe-context-menu",
                position="absolute",
                background="white",
                border="1px solid #ccc",
                border_radius="4px",
                box_shadow="0 2px 10px rgba(0,0,0,0.15)",
                z_index="1000",
                min_width="150px"
            ),
            
            CSS.class_("fe-context-item",
                padding="8px 12px",
                cursor="pointer",
                font_size="14px",
                border_bottom="1px solid #f0f0f0"
            ),
            
            CSS.selector(".fe-context-item:hover",
                background="#f8f9fa"
            ),
            
            CSS.selector(".fe-context-item:last-child",
                border_bottom="none"
            ),
            
            CSS.class_("fe-context-separator",
                margin="4px 0",
                border_color="#e9ecef"
            )
        ]
    
    def refresh_file_list(self):
        """Refresh the file list display."""
        file_list = js.document.getElementById("fe-file-list")
        if file_list:
            # Clear current list
            file_list.innerHTML = ""
            
            # Add updated items
            items = self.fs.get_current_items()
            sorted_items = sorted(items, key=lambda x: (not x.is_directory(), x.name.lower()))
            
            for item in sorted_items:
                row_html = str(self.create_file_item_row(item))
                file_list.insertAdjacentHTML('beforeend', row_html)
        
        # Update path display
        path_display = js.document.getElementById("fe-path")
        if path_display:
            path_display.textContent = self.fs.get_path_string()
        
        # Clear selection
        self.clear_selection()
        
        # Note: Event handlers use delegation, no need to re-attach
    
    def clear_selection(self):
        """Clear current selection."""
        selected_rows = js.document.querySelectorAll('.fe-item-row.selected')
        for row in selected_rows:
            row.classList.remove('selected')
        
        self.selected_item = None
        
        # Update delete button state
        delete_btn = js.document.getElementById("fe-delete")
        if delete_btn:
            delete_btn.disabled = True
    
    def setup_event_handlers(self):
        """Setup all event handlers for the file explorer."""
        
        def handle_new_folder(event):
            name = js.prompt("Enter folder name:")
            if name and name.strip():
                if self.fs.create_directory(name.strip()):
                    self.refresh_file_list()
                else:
                    js.alert(f"Folder '{name}' already exists!")
        
        def handle_new_file(event):
            name = js.prompt("Enter file name:")
            if name and name.strip():
                if self.fs.create_file(name.strip()):
                    self.refresh_file_list()
                else:
                    js.alert(f"File '{name}' already exists!")
        
        def handle_delete(event):
            if self.selected_item:
                if js.confirm(f"Delete '{self.selected_item}'?"):
                    if self.fs.delete_item(self.selected_item):
                        self.refresh_file_list()
        
        def handle_up(event):
            if self.fs.go_up():
                self.refresh_file_list()
        
        def handle_reset(event):
            if js.confirm("Reset filesystem to defaults? This will delete all your files and folders."):
                self.fs.reset_filesystem()
                self.refresh_file_list()
        
        # Setup toolbar button handlers
        on_click("fe-new-folder", handle_new_folder)
        on_click("fe-new-file", handle_new_file)
        on_click("fe-delete", handle_delete)
        on_click("fe-up", handle_up)
        on_click("fe-reset", handle_reset)
        
        # Setup file list handlers
        self.setup_file_list_handlers()
        
        # Hide context menu on document click
        def hide_context_menu(event):
            context_menu = js.document.getElementById("fe-context-menu")
            if context_menu:
                context_menu.hidden = True
        
        events.add_document_listener('click', hide_context_menu)
    
    def setup_file_list_handlers(self):
        """Setup event handlers for file list items using delegation."""
        
        # Remove existing handlers first to prevent duplicates
        if hasattr(self, '_handlers_attached'):
            table_container = js.document.querySelector(f"#{self.container_id} .fe-file-list-container")
            if table_container and hasattr(self, '_click_proxy'):
                table_container.removeEventListener('click', self._click_proxy)
                table_container.removeEventListener('dblclick', self._dblclick_proxy)
                table_container.removeEventListener('contextmenu', self._contextmenu_proxy)
        
        def handle_table_click(event):
            # Find the closest row
            row = event.target.closest('.fe-item-row')
            if not row:
                return
                
            # Clear previous selection
            self.clear_selection()
            
            # Select the row
            row.classList.add('selected')
            self.selected_item = row.getAttribute('data-name')
            
            # Enable delete button
            delete_btn = js.document.getElementById("fe-delete")
            if delete_btn:
                delete_btn.disabled = False
        
        def handle_table_double_click(event):
            # Prevent event bubbling and default behavior
            event.preventDefault()
            event.stopPropagation()
            
            # Find the closest row
            row = event.target.closest('.fe-item-row')
            if not row:
                return
                
            print("Double click detected!")  # Debug
            item_name = row.getAttribute('data-name')
            item_type = row.getAttribute('data-type')
            print(f"Double-clicked item: {item_name}, type: {item_type}")  # Debug
            
            # Prevent rapid double-clicks
            if hasattr(self, '_last_double_click'):
                time_diff = js.Date.new().getTime() - self._last_double_click
                if time_diff < 500:  # 500ms debounce
                    print("Double-click too rapid, ignoring")  # Debug
                    return
            
            self._last_double_click = js.Date.new().getTime()
            
            if item_type == 'directory':
                # Navigate into directory
                new_path = self.fs.current_path + [item_name]
                if self.fs.navigate_to(new_path):
                    self.refresh_file_list()
            else:
                # Open file in text editor
                try:
                    # Get file content
                    current_dir = self.fs.get_current_directory()
                    file_item = current_dir.get_child(item_name)
                    
                    if file_item and file_item.is_file():
                        # Store file info globally for text editor access
                        js.window.sci_ux_file_data = {
                            'name': item_name,
                            'content': file_item.content,
                            'path': self.fs.get_path_string() + '/' + item_name if self.fs.get_path_string() != '/' else '/' + item_name
                        }
                        
                        # Navigate to text editor by triggering main navigation
                        # We'll use a custom event to trigger navigation
                        print(f"Dispatching navigation event for file: {item_name}")  # Debug
                        
                        # Use setTimeout to ensure file data is properly set before navigation
                        def delayed_navigation():
                            nav_event = js.CustomEvent.new('sci-ux-navigate', {
                                'detail': {'page': 'text-editor-open'}
                            })
                            js.window.dispatchEvent(nav_event)
                            print("Navigation event dispatched (delayed)")  # Debug
                        
                        nav_proxy = create_proxy(delayed_navigation)
                        js.setTimeout(nav_proxy, 50)  # 50ms delay
                    else:
                        js.alert(f"Could not open file: {item_name}")
                except Exception as e:
                    js.alert(f"Error opening file: {e}")
        
        def handle_table_context_menu(event):
            # Disable context menu on table rows
            if event.target.closest('.fe-item-row'):
                event.preventDefault()
                return False
        
        # Use delegation - attach to the table container instead of individual rows
        table_container = js.document.querySelector(f"#{self.container_id} .fe-file-list-container")
        if table_container:
            # Store proxy references for cleanup
            self._click_proxy = create_proxy(handle_table_click)
            self._dblclick_proxy = create_proxy(handle_table_double_click)
            self._contextmenu_proxy = create_proxy(handle_table_context_menu)
            
            table_container.addEventListener('click', self._click_proxy)
            table_container.addEventListener('dblclick', self._dblclick_proxy)
            table_container.addEventListener('contextmenu', self._contextmenu_proxy)
            
            # Mark that handlers are attached
            self._handlers_attached = True
            print("File list handlers attached using delegation")  # Debug
        else:
            print(f"Warning: Could not find table container for {self.container_id}")  # Debug


def create_file_explorer(container_id: str = "file-explorer") -> FileExplorer:
    """Factory function to create a file explorer instance."""
    return FileExplorer(container_id)