#!/usr/bin/env python3
"""
File Explorer Demo Page for Sci-UX

Demonstrates the file explorer applet integrated with the main application.
"""

import js
from py_html.elements import *
from py_html.css import CSS
from py_dom import events, on_click
from ui.applets.file_explorer import create_file_explorer


def create_file_explorer_demo_content():
    """Create the file explorer demo page content."""
    
    explorer = create_file_explorer("main-file-explorer")
    js.window.sci_ux_file_explorer = explorer
    print("Created new file explorer instance in create_content")  # Debug

    return Div(class_="app-container").add(
        # Page header
        Div(class_="hero", style="margin-bottom: 30px;").add(
            H1("Sci-UX File Explorer"),
            P("A Jupyter-like file browser for managing your projects and notebooks")
        ),
        
        # Description section
        Div(class_="demo-section", style="margin-bottom: 30px;").add(
            H2("Features"),
            Div(class_="feature-grid", style="display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 20px; margin: 20px 0;").add(
                Div(class_="card").add(
                    H3("📁 File Management"),
                    P("Create, delete, and organize files and folders with an intuitive interface.")
                ),
                Div(class_="card").add(
                    H3("💾 Persistent Storage"),
                    P("Files and folders persist across browser sessions using localStorage. Your work is automatically saved!")
                ),
                Div(class_="card").add(
                    H3("🔍 File Type Support"),
                    P("Recognizes common file types with appropriate icons: Python scripts, Jupyter notebooks, CSV data, and more.")
                ),
                Div(class_="card").add(
                    H3("⚡ Quick Actions"),
                    P("Right-click context menus and toolbar buttons for efficient file operations.")
                )
            )
        ),
        
        # File explorer demo
        Div(class_="demo-section").add(
            H2("Try It Out"),
            P("Use the file explorer below to navigate, create files and folders, and explore the virtual file system:"),
            Div(style="margin: 20px 0; display: flex; justify-content: center;").add(
                explorer.render()
            )
        ),
        
        # Usage instructions
        Div(class_="demo-section", style="margin-top: 30px;").add(
            H2("Usage Instructions"),
            Ul(style="line-height: 1.6; color: #555;").add(
                Li("🖱️ Single-click to select files and folders"),
                Li("🖱️ Double-click folders to navigate into them"),
                Li("🖱️ Right-click for context menu options"),
                Li("📁 Use '+ New Folder' to create directories"),
                Li("📄 Use '+ New File' to create new files"),
                Li("🗑️ Select items and click 'Delete' to remove them"),
                Li("⬆️ Click 'Up' to navigate to the parent directory"),
                Li("🔄 Click 'Reset' to restore default files (clears all custom data)"),
                Li("💾 All changes are automatically saved to browser storage")
            )
        ),
        
        Footer().add(
            Div(class_="footer").add(
                P("File Explorer Demo - Part of Sci-UX Framework"),
                P("Ready for integration with notebook editors and data analysis tools")
            )
        )
    )


def setup_file_explorer_demo_handlers():
    """Set up event handlers for the file explorer demo page."""
    
    # Get the file explorer instance and set up its handlers
    explorer_element = js.document.getElementById("main-file-explorer")
    if explorer_element:
        # Use the same persistence logic as create_file_explorer_demo_content
        if hasattr(js.window, 'sci_ux_file_explorer') and js.window.sci_ux_file_explorer is not None:
            explorer = js.window.sci_ux_file_explorer
            print("Using existing file explorer instance for handlers")  # Debug
        else:
            # Fallback - create new instance if somehow not found
            from ui.applets.file_explorer import FileExplorer
            explorer = FileExplorer("main-file-explorer")
            js.window.sci_ux_file_explorer = explorer
            print("Created fallback file explorer instance")  # Debug
        
        # Add styles to page if not already present
        if not js.document.getElementById('file-explorer-styles'):
            styles = explorer.get_styles()
            style_content = "\n".join(str(style) for style in styles)
            style_element = f'<style id="file-explorer-styles">{style_content}</style>'
            js.document.head.insertAdjacentHTML('beforeend', style_element)
        
        # Always setup event handlers to ensure they work after navigation
        explorer.setup_event_handlers()
        print("Event handlers set up for file explorer")  # Debug


def get_file_explorer_demo_styles():
    """Get additional CSS styles for the demo page."""
    return [
        CSS.class_("feature-grid",
            display="grid",
            grid_template_columns="repeat(auto-fit, minmax(250px, 1fr))",
            gap="20px",
            margin="20px 0"
        ),
        
        CSS.selector(".demo-section",
            margin="40px 0"
        ),
        
        CSS.selector(".demo-section h2",
            color="#333",
            margin_bottom="15px"
        ),
        
        CSS.selector(".demo-section p",
            color="#555",
            line_height="1.6"
        ),
        
        CSS.selector(".demo-section ul",
            max_width="600px",
            margin="20px auto"
        ),
        
        CSS.selector(".demo-section li",
            margin="10px 0"
        )
    ]