#!/usr/bin/env python3
"""
Text Editor Applet for Sci-UX

A full-featured code editor with syntax highlighting using CodeMirror,
supporting multiple programming languages and file types commonly used
in scientific computing.
"""

import js
from pyodide.ffi import create_proxy
from py_html.elements import *
from py_html.css import CSS
from py_dom import events, on_click
from typing import Dict, List, Optional
import json


class CodeMirrorHelper:
    """Helper class for CodeMirror integration."""
    
    @staticmethod
    def detect_mode(filename: str) -> str:
        """Detect CodeMirror mode from filename."""
        if not filename or '.' not in filename:
            return 'text'
            
        ext = filename.split('.')[-1].lower()
        
        mode_map = {
            'py': 'python',
            'js': 'javascript',
            'jsx': 'javascript',
            'ts': 'javascript', 
            'tsx': 'javascript',
            'html': 'htmlmixed',
            'htm': 'htmlmixed',
            'css': 'css',
            'scss': 'css',
            'sass': 'css',
            'json': 'javascript',
            'md': 'markdown',
            'txt': 'text',
            'log': 'text',
            'csv': 'text',
            'ipynb': 'javascript',
        }
        
        return mode_map.get(ext, 'text')
    
    @staticmethod
    def get_display_name(mode: str) -> str:
        """Get display name for mode."""
        display_map = {
            'python': 'Python',
            'javascript': 'JavaScript',
            'htmlmixed': 'HTML',
            'css': 'CSS',
            'markdown': 'Markdown',
            'text': 'Plain Text'
        }
        return display_map.get(mode, mode.title())



class TextEditor:
    """A full-featured text editor with syntax highlighting."""
    
    def __init__(self, container_id: str = "text-editor"):
        self.container_id = container_id
        self.current_file = None
        self.current_mode = 'text'
        self.is_modified = False
        self.content = ""
        self.editor_instance = None
        self.is_saving = False  # Prevent multiple save operations
        
    def create_toolbar(self) -> Div:
        """Create editor toolbar with file operations."""
        return Div(class_="te-toolbar").add(
            Button("New", class_="te-btn te-btn-new", id="te-new"),
            Button("Open", class_="te-btn te-btn-open", id="te-open"),
            Button("Save", class_="te-btn te-btn-save", id="te-save", disabled=True),
            Button("Save As", class_="te-btn te-btn-save-as", id="te-save-as"),
            Div(class_="te-separator"),
            Button("Undo", class_="te-btn te-btn-undo", id="te-undo"),
            Button("Redo", class_="te-btn te-btn-redo", id="te-redo"),
            Div(class_="te-separator"),
            Select(class_="te-language-select", id="te-language").add(
                Option("Auto-detect", value="auto", selected=True),
                Option("Plain Text", value="text"),
                Option("Python", value="python"),
                Option("JavaScript", value="javascript"),
                Option("HTML", value="htmlmixed"),
                Option("CSS", value="css"),
                Option("JSON", value="javascript")
            ),
            Span(class_="te-file-info", id="te-file-info").add("Untitled")
        )
    
    def create_editor_area(self) -> Div:
        """Create the main editor area for CodeMirror."""
        return Div(class_="te-editor-container").add(
            Div(class_="te-editor-wrapper", id="te-editor")
        )
    
    def create_status_bar(self) -> Div:
        """Create status bar showing cursor position and file info."""
        return Div(class_="te-status-bar").add(
            Span(class_="te-cursor-info", id="te-cursor-info").add("Line 1, Column 1"),
            Span(class_="te-file-status", id="te-file-status").add(""),
            Span(class_="te-language-info", id="te-language-info").add("Plain Text")
        )
    
    # Remove this method - we'll use the reusable modal system instead
    
    def render(self) -> Div:
        """Render the complete text editor."""
        return Div(class_="text-editor", id=self.container_id).add(
            self.create_toolbar(),
            self.create_editor_area(),
            self.create_status_bar()
        )
    
    def get_styles(self) -> List[CSS]:
        """Get CSS styles for the text editor."""
        return [
            # Main container
            CSS.class_("text-editor",
                border="1px solid #ddd",
                border_radius="8px",
                background="white",
                font_family="'Segoe UI', Tahoma, Geneva, Verdana, sans-serif",
                display="flex",
                flex_direction="column",
                height="600px",
                max_width="100%",
                box_shadow="0 2px 10px rgba(0,0,0,0.1)"
            ),
            
            # Toolbar
            CSS.class_("te-toolbar",
                padding="10px",
                border_bottom="1px solid #eee",
                background="#f8f9fa",
                display="flex",
                gap="8px",
                align_items="center",
                border_radius="7px 7px 0 0",
                flex_shrink="0"
            ),
            
            CSS.class_("te-btn",
                padding="6px 12px",
                border="1px solid #ccc",
                border_radius="4px",
                background="white",
                cursor="pointer",
                font_size="13px",
                transition="background 0.2s"
            ),
            
            CSS.selector(".te-btn:hover:not(:disabled)",
                background="#f0f0f0"
            ),
            
            CSS.selector(".te-btn:disabled",
                opacity="0.5",
                cursor="not-allowed",
                background="#f5f5f5"
            ),
            
            CSS.class_("te-separator",
                width="1px",
                height="20px",
                background="#ddd",
                margin="0 4px"
            ),
            
            CSS.class_("te-language-select",
                padding="6px 8px",
                border="1px solid #ccc",
                border_radius="4px",
                font_size="13px",
                background="white"
            ),
            
            CSS.class_("te-file-info",
                margin_left="auto",
                font_weight="500",
                color="#495057",
                font_size="14px"
            ),
            
            # Editor area
            CSS.class_("te-editor-container",
                display="flex",
                flex="1",
                overflow="hidden",
                min_height="0"
            ),
            
            CSS.class_("te-editor-wrapper",
                flex="1",
                overflow="hidden"
            ),
            
            # CodeMirror integration
            CSS.selector(".CodeMirror",
                height="100%",
                font_family="'Courier New', Consolas, monospace",
                font_size="14px",
                line_height="1.5"
            ),
            
            CSS.selector(".CodeMirror-scroll",
                overflow_y="auto",
                overflow_x="auto"
            ),
            
            # Status bar
            CSS.class_("te-status-bar",
                padding="8px 12px",
                border_top="1px solid #eee",
                background="#f8f9fa",
                display="flex",
                justify_content="space-between",
                align_items="center",
                font_size="12px",
                color="#666",
                border_radius="0 0 7px 7px",
                flex_shrink="0"
            ),
            
        ]
    
    def create_codemirror_instance(self):
        """Create CodeMirror instance."""
        try:
            # Check if CodeMirror is available
            if not hasattr(js, 'CodeMirror'):
                print("CodeMirror is not available")
                return
                
            editor_element = js.document.getElementById("te-editor")
            if editor_element and not self.editor_instance:
                # Clear the element first
                editor_element.innerHTML = ""
                
                config = {
                    "lineNumbers": True,
                    "mode": self.current_mode,
                    "theme": "default", 
                    "lineWrapping": True,
                    "indentUnit": 4,
                    "tabSize": 4,
                    "matchBrackets": True,
                    "autoCloseBrackets": True,
                    "value": self.content
                }
                self.editor_instance = js.CodeMirror(editor_element, config)
                
                # Set up change handler with create_proxy
                def on_change(cm, change):
                    self.content = cm.getValue()
                    self.is_modified = True
                    self.update_status_bar()
                    
                    # Enable save button
                    save_btn = js.document.getElementById("te-save")
                    if save_btn and self.current_file:
                        save_btn.disabled = False
                
                change_proxy = create_proxy(on_change)
                self.editor_instance.on("change", change_proxy)
                
                # Set up cursor activity handler with create_proxy
                def on_cursor_activity(cm):
                    self.update_cursor_info()
                
                cursor_proxy = create_proxy(on_cursor_activity)
                self.editor_instance.on("cursorActivity", cursor_proxy)
                
                print(f"CodeMirror instance created with mode: {self.current_mode}")
                
        except Exception as e:
            print(f"Error creating CodeMirror instance: {e}")
    
    def update_cursor_info(self):
        """Update cursor position from CodeMirror."""
        if self.editor_instance:
            cursor = self.editor_instance.getCursor()
            line = cursor.line + 1  # CodeMirror lines are 0-indexed
            column = cursor.ch + 1  # CodeMirror columns are 0-indexed
            
            cursor_info = js.document.getElementById("te-cursor-info")
            if cursor_info:
                cursor_info.textContent = f"Line {line}, Column {column}"
    
    def update_status_bar(self):
        """Update status bar information."""
        file_status = js.document.getElementById("te-file-status")
        language_info = js.document.getElementById("te-language-info")
        
        if file_status:
            status = "●" if self.is_modified else ""
            file_status.textContent = status
        
        if language_info:
            language_info.textContent = CodeMirrorHelper.get_display_name(self.current_mode)
    
    def set_content(self, content: str, filename: str = None):
        """Set editor content and update mode."""
        print(f"Setting content for file: {filename}")  # Debug
        self.content = content
        self.current_file = filename
        
        if filename:
            self.current_mode = CodeMirrorHelper.detect_mode(filename)
            print(f"Detected mode: {self.current_mode} for file: {filename}")  # Debug
        
        # Update CodeMirror if it exists
        if self.editor_instance:
            try:
                print(f"Updating existing CodeMirror with content length: {len(content)}")  # Debug
                self.editor_instance.setValue(content)
                self.editor_instance.setOption("mode", self.current_mode)
                print(f"Successfully updated CodeMirror with mode: {self.current_mode}")  # Debug
            except Exception as e:
                print(f"Error updating CodeMirror content: {e}")
                # Reset editor instance and try again
                self.editor_instance = None
                self.create_codemirror_instance()
        else:
            # Create CodeMirror instance if it doesn't exist
            print("Creating new CodeMirror instance")  # Debug
            self.create_codemirror_instance()
        
        # Update displays
        self.update_status_bar()
        
        # Update file info
        file_info = js.document.getElementById("te-file-info")
        if file_info:
            file_info.textContent = filename or "Untitled"
        
        # Update language select
        language_select = js.document.getElementById("te-language")
        if language_select:
            language_select.value = self.current_mode
        
        self.is_modified = False
    
    def set_mode(self, mode: str):
        """Set editor mode."""
        self.current_mode = mode
        if self.editor_instance:
            self.editor_instance.setOption("mode", mode)
        self.update_status_bar()
    
    def setup_event_handlers(self):
        """Setup all event handlers for the text editor."""
        
        # Check if DOM element exists and recreate CodeMirror if needed
        editor_element = js.document.getElementById("te-editor")
        if not editor_element:
            print("Warning: te-editor DOM element not found")
            return
        
        # If CodeMirror instance exists but DOM changed, reset it
        if self.editor_instance and not editor_element.querySelector('.CodeMirror'):
            print("DOM changed, resetting CodeMirror instance")
            self.editor_instance = None
        
        # Create CodeMirror instance if needed
        if not self.editor_instance:
            self.create_codemirror_instance()
        
        def handle_language_change(event):
            mode = event.target.value
            if mode == 'auto' and self.current_file:
                mode = CodeMirrorHelper.detect_mode(self.current_file)
            elif mode == 'auto':
                mode = 'text'
            
            self.set_mode(mode)
        def handle_new(event):
            if self.is_modified:
                if not js.confirm("You have unsaved changes. Are you sure you want to create a new file?"):
                    return
            
            self.set_content("", None)
        
        def handle_open(event):
            # Use the reusable modal system with file explorer
            try:
                from ui.modal import create_file_explorer_modal
                
                # Create and show file explorer modal
                modal = create_file_explorer_modal("te-file-open-modal")
                
                # Set up file selection callback
                def on_file_selected(file_data):
                    print(f"Selected file: {file_data}")  # Debug
                    self.set_content(file_data['content'], file_data['name'])
                
                modal.set_on_file_select(on_file_selected)
                modal.show()
                
            except Exception as e:
                print(f"Error opening file modal: {e}")  # Debug
                js.alert(f"Could not open file picker: {e}")
        
        
        def handle_save(event):
            print(f"Save called - current_file: {self.current_file}, is_saving: {self.is_saving}")  # Debug
            
            # Prevent multiple save operations
            if self.is_saving:
                print("Already saving, ignoring duplicate save call")
                return
                
            if not self.current_file:
                # No current file, use save as instead
                print("No current file, calling save as")  # Debug
                handle_save_as(event)
                return
            
            self.is_saving = True  # Set saving flag
            
            try:
                # Get current content from CodeMirror
                if self.editor_instance:
                    self.content = self.editor_instance.getValue()
                
                # Save to the virtual file system
                from ui.applets.file_explorer import VirtualFileSystem
                fs = VirtualFileSystem()
                
                # Parse the file path to navigate to the correct directory
                path_parts = self.current_file.split('/')
                filename = path_parts[-1]
                directory_path = path_parts[:-1] if len(path_parts) > 1 else []
                
                print(f"Saving file: {filename} in path: {directory_path}")  # Debug
                
                # Navigate to the correct directory
                current_dir = fs.root
                for part in directory_path:
                    if part:  # Skip empty parts from leading slash
                        current_dir = current_dir.get_child(part)
                        if not current_dir:
                            js.alert(f"Directory not found: {'/'.join(directory_path)}")
                            return
                
                # Update file content
                file_item = current_dir.get_child(filename)
                if file_item and file_item.is_file():
                    file_item.content = self.content
                    file_item.size = len(self.content)
                    file_item.modified = js.Date.new().toISOString()
                    
                    # Save the filesystem
                    fs._save_filesystem()
                    
                    print(f"Successfully saved {self.current_file}")  # Debug
                    js.alert(f"Saved {self.current_file}")
                    self.is_modified = False
                    self.update_status_bar()
                    
                    # Disable save button
                    save_btn = js.document.getElementById("te-save")
                    if save_btn:
                        save_btn.disabled = True
                else:
                    js.alert(f"File not found: {self.current_file}")
                    
            except Exception as e:
                print(f"Error in handle_save: {e}")  # Debug
                js.alert(f"Error saving file: {e}")
            finally:
                self.is_saving = False  # Reset saving flag
        
        def handle_save_as(event):
            print(f"Save As called - is_saving: {self.is_saving}")  # Debug
            
            # Prevent multiple save operations
            if self.is_saving:
                print("Already saving, ignoring duplicate save as call")
                return
            
            # Get current content from CodeMirror
            if self.editor_instance:
                self.content = self.editor_instance.getValue()
                
            # Always prompt for filename in save as, regardless of current file
            default_name = self.current_file if self.current_file else "untitled.txt"
            filename = js.prompt("Enter filename (use / for directories, e.g. 'scripts/new_file.py'):", default_name)
            if filename and filename.strip():
                self.is_saving = True  # Set saving flag
                try:
                    # Save to the virtual file system
                    from ui.applets.file_explorer import VirtualFileSystem
                    fs = VirtualFileSystem()
                    
                    # Parse the file path
                    path_parts = filename.split('/')
                    file_name = path_parts[-1]
                    directory_path = path_parts[:-1] if len(path_parts) > 1 else []
                    
                    # Navigate to the correct directory (create if needed)
                    current_dir = fs.root
                    for part in directory_path:
                        if part:  # Skip empty parts from leading slash
                            child_dir = current_dir.get_child(part)
                            if not child_dir:
                                # Directory doesn't exist, ask to create it
                                if js.confirm(f"Directory '{part}' doesn't exist. Create it?"):
                                    from ui.applets.file_explorer import FileSystemItem
                                    new_dir = FileSystemItem(part, "directory")
                                    current_dir.add_child(new_dir)
                                    current_dir = new_dir
                                else:
                                    return
                            else:
                                current_dir = child_dir
                    
                    # Create or update the file
                    from ui.applets.file_explorer import FileSystemItem
                    file_item = current_dir.get_child(file_name)
                    if file_item:
                        # File exists, update content
                        file_item.content = self.content
                        file_item.size = len(self.content)
                        file_item.modified = js.Date.new().toISOString()
                    else:
                        # Create new file
                        new_file = FileSystemItem(file_name, "file", len(self.content), content=self.content)
                        current_dir.add_child(new_file)
                    
                    # Save the filesystem
                    fs._save_filesystem()
                    
                    # Update editor state
                    self.current_file = filename
                    self.current_mode = CodeMirrorHelper.detect_mode(filename)
                    self.is_modified = False
                    
                    print(f"Save As completed - current_file set to: {self.current_file}")  # Debug
                    
                    # Update UI
                    file_info = js.document.getElementById("te-file-info")
                    if file_info:
                        file_info.textContent = filename
                    
                    # Update language select
                    language_select = js.document.getElementById("te-language")
                    if language_select:
                        language_select.value = self.current_mode
                    
                    self.update_status_bar()
                    
                    # Disable save button
                    save_btn = js.document.getElementById("te-save")
                    if save_btn:
                        save_btn.disabled = True
                    
                    js.alert(f"Saved as {filename}")
                    
                except Exception as e:
                    js.alert(f"Error saving file: {e}")
                finally:
                    self.is_saving = False  # Reset saving flag
        
        
        language_select = js.document.getElementById("te-language")
        if language_select:
            change_proxy = create_proxy(handle_language_change)
            language_select.addEventListener('change', change_proxy)
        
        # Setup toolbar button handlers - use direct event listener attachment
        # to ensure they work after navigation
        def setup_button_handlers():
            buttons = [
                ("te-new", handle_new),
                ("te-open", handle_open),
                ("te-save", handle_save),
                ("te-save-as", handle_save_as)
            ]
            
            for button_id, handler in buttons:
                button = js.document.getElementById(button_id)
                if button:
                    # Remove any existing listeners to prevent duplicates
                    if hasattr(self, f'_{button_id}_proxy'):
                        button.removeEventListener('click', getattr(self, f'_{button_id}_proxy'))
                    
                    # Create new proxy and attach
                    proxy = create_proxy(handler)
                    setattr(self, f'_{button_id}_proxy', proxy)
                    button.addEventListener('click', proxy)
                    print(f"Attached handler to {button_id}")  # Debug
                else:
                    print(f"Warning: Button {button_id} not found")  # Debug
        
        setup_button_handlers()
    


def create_text_editor(container_id: str = "text-editor") -> TextEditor:
    """Factory function to create a text editor instance."""
    return TextEditor(container_id)