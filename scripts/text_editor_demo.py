#!/usr/bin/env python3
"""
Text Editor Demo Page for Sci-UX

Demonstrates the text editor applet with syntax highlighting capabilities.
"""

import js
from pyodide.ffi import create_proxy
from py_html.elements import *
from py_html.css import CSS
from py_dom import events, on_click
from ui.applets.text_editor import create_text_editor


def create_text_editor_demo_content():
    """Create the text editor demo page content."""
    
    # Create text editor instance
    editor = create_text_editor("main-text-editor")
    
    return Div(class_="app-container").add(
        # Page header
        Div(class_="hero", style="margin-bottom: 30px;").add(
            H1("Sci-UX Text Editor"),
            P("A powerful code editor with syntax highlighting for scientific computing")
        ),
        
        # Description section
        Div(class_="demo-section", style="margin-bottom: 30px;").add(
            H2("Features"),
            Div(class_="feature-grid", style="display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 20px; margin: 20px 0;").add(
                Div(class_="card").add(
                    H3("🎨 Syntax Highlighting"),
                    P("Support for Python, JavaScript, HTML, CSS, JSON, and more with automatic language detection.")
                ),
                Div(class_="card").add(
                    H3("📝 Smart Editing"),
                    P("Line numbers, cursor position tracking, and real-time syntax highlighting as you type.")
                ),
                Div(class_="card").add(
                    H3("💾 File Operations"),
                    P("New, open, save, and save-as functionality with file type detection for optimal highlighting.")
                ),
                Div(class_="card").add(
                    H3("⚡ Responsive UI"),
                    P("Clean, modern interface with toolbar, status bar, and customizable language selection.")
                )
            )
        ),
        
        # Text editor demo
        Div(class_="demo-section").add(
            H2("Try It Out"),
            P("Use the text editor below to write code with syntax highlighting:"),
            Div(style="margin: 20px 0;").add(
                editor.render()
            )
        ),
        
        # Sample code section
        Div(class_="demo-section", style="margin-top: 30px;").add(
            H2("Sample Code"),
            P("Click on any sample below to load it into the editor:"),
            Div(class_="sample-code-grid", style="display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 20px; margin: 20px 0;").add(
                Div(class_="sample-card", data={"type": "python"}).add(
                    H4("Python Example"),
                    Pre(class_="sample-preview").add(
                        Code().add(
                            "# Scientific computing example\n"
                            "import numpy as np\n"
                            "import matplotlib.pyplot as plt\n\n"
                            "def analyze_data(data):\n"
                            "    mean = np.mean(data)\n"
                            "    std = np.std(data)\n"
                            "    return {'mean': mean, 'std': std}\n\n"
                            "# Generate sample data\n"
                            "data = np.random.normal(0, 1, 1000)\n"
                            "results = analyze_data(data)\n"
                            "print(f\"Mean: {results['mean']:.3f}\")"
                        )
                    )
                ),
                Div(class_="sample-card", data={"type": "javascript"}).add(
                    H4("JavaScript Example"),
                    Pre(class_="sample-preview").add(
                        Code().add(
                            "// Data visualization example\n"
                            "class DataVisualizer {\n"
                            "    constructor(containerId) {\n"
                            "        this.container = document.getElementById(containerId);\n"
                            "        this.data = [];\n"
                            "    }\n\n"
                            "    addData(points) {\n"
                            "        this.data = [...this.data, ...points];\n"
                            "        this.render();\n"
                            "    }\n\n"
                            "    render() {\n"
                            "        // Render visualization\n"
                            "        console.log('Rendering', this.data.length, 'points');\n"
                            "    }\n"
                            "}"
                        )
                    )
                ),
                Div(class_="sample-card", data={"type": "html"}).add(
                    H4("HTML Example"),
                    Pre(class_="sample-preview").add(
                        Code().add(
                            '<!DOCTYPE html>\n'
                            '<html lang="en">\n'
                            '<head>\n'
                            '    <meta charset="UTF-8">\n'
                            '    <meta name="viewport" content="width=device-width, initial-scale=1.0">\n'
                            '    <title>Scientific Dashboard</title>\n'
                            '    <!-- CSS would go here -->\n'
                            '</head>\n'
                            '<body>\n'
                            '    <header class="main-header">\n'
                            '        <h1>Data Analysis Dashboard</h1>\n'
                            '    </header>\n'
                            '    <main id="content">\n'
                            '        <div class="chart-container"></div>\n'
                            '    </main>\n'
                            '</body>\n'
                            '</html>'
                        )
                    )
                ),
                Div(class_="sample-card", data={"type": "json"}).add(
                    H4("JSON Configuration"),
                    Pre(class_="sample-preview").add(
                        Code().add(
                            '{\n'
                            '  "experiment": {\n'
                            '    "name": "Data Analysis Pipeline",\n'
                            '    "version": "1.2.0",\n'
                            '    "parameters": {\n'
                            '      "sample_size": 1000,\n'
                            '      "confidence_level": 0.95,\n'
                            '      "method": "bootstrap",\n'
                            '      "iterations": 10000\n'
                            '    },\n'
                            '    "outputs": [\n'
                            '      "summary_statistics",\n'
                            '      "confidence_intervals",\n'
                            '      "visualizations"\n'
                            '    ],\n'
                            '    "enabled": true\n'
                            '  }\n'
                            '}'
                        )
                    )
                )
            )
        ),
        
        # Usage instructions
        Div(class_="demo-section", style="margin-top: 30px;").add(
            H2("Usage Instructions"),
            Ul(style="line-height: 1.6; color: #555;").add(
                Li("📝 Start typing to see real-time syntax highlighting"),
                Li("🔤 Use the language selector to manually override auto-detection"),
                Li("📁 Click 'New' to start a fresh document"),
                Li("💾 Use 'Save As' to specify a filename and enable 'Save'"),
                Li("🎯 Click on sample code cards to load examples"),
                Li("📍 Watch the status bar for cursor position and file information"),
                Li("🎨 Syntax highlighting adapts automatically to file extensions"),
                Li("⌨️ Standard keyboard shortcuts work (Ctrl+A, Ctrl+C, etc.)")
            )
        ),
        
        Footer().add(
            Div(class_="footer").add(
                P("Text Editor Demo - Part of Sci-UX Framework"),
                P("Perfect for coding, documentation, and data analysis scripts")
            )
        )
    )


def setup_text_editor_demo_handlers():
    """Set up event handlers for the text editor demo page."""
    
    # Get the text editor instance and set up its handlers
    editor_element = js.document.getElementById("main-text-editor")
    if editor_element:
        # Check if we already have a text editor instance
        if not hasattr(js.window, 'sci_ux_text_editor') or js.window.sci_ux_text_editor is None:
            # Create a new instance to set up handlers
            from ui.applets.text_editor import TextEditor
            editor = TextEditor("main-text-editor")
            js.window.sci_ux_text_editor = editor
            print("Created new text editor instance")  # Debug
        else:
            editor = js.window.sci_ux_text_editor
            print("Reusing existing text editor instance")  # Debug
        
        # Add styles to page if not already present
        if not js.document.getElementById('text-editor-styles'):
            styles = editor.get_styles()
            style_content = "\n".join(str(style) for style in styles)
            style_element = f'<style id="text-editor-styles">{style_content}</style>'
            js.document.head.insertAdjacentHTML('beforeend', style_element)
        
        # Always setup event handlers to ensure they work after navigation
        # This will check if CodeMirror DOM element exists and recreate if needed
        editor.setup_event_handlers()
        print("Event handlers set up for text editor")  # Debug
        
        # Check if a file is being opened from file explorer
        if hasattr(js.window, 'sci_ux_file_data') and js.window.sci_ux_file_data:
            file_data = js.window.sci_ux_file_data
            print(f"Loading file: {file_data}")  # Debug
            editor.set_content(file_data['content'], file_data['name'])
            # Clear the file data
            js.window.sci_ux_file_data = None
        
        # Setup sample code click handlers
        def handle_sample_click(event):
            card = event.target.closest('.sample-card')
            if card:
                sample_type = card.getAttribute('data-type')
                sample_code = card.querySelector('code').textContent
                
                # Set content in editor
                editor.set_content(sample_code, f"sample.{get_extension_for_type(sample_type)}")
        
        def get_extension_for_type(sample_type):
            extensions = {
                'python': 'py',
                'javascript': 'js', 
                'html': 'html',
                'json': 'json'
            }
            return extensions.get(sample_type, 'txt')
        
        # Add click handlers to sample cards
        sample_cards = js.document.querySelectorAll('.sample-card')
        for card in sample_cards:
            click_proxy = create_proxy(handle_sample_click)
            card.addEventListener('click', click_proxy)


def get_text_editor_demo_styles():
    """Get additional CSS styles for the demo page."""
    return [
        CSS.class_("sample-code-grid",
            display="grid",
            grid_template_columns="repeat(auto-fit, minmax(300px, 1fr))",
            gap="20px",
            margin="20px 0"
        ),
        
        CSS.class_("sample-card",
            border="1px solid #ddd",
            border_radius="8px",
            padding="15px",
            background="white",
            cursor="pointer",
            transition="all 0.2s ease",
            box_shadow="0 2px 4px rgba(0,0,0,0.1)"
        ),
        
        CSS.selector(".sample-card:hover",
            border_color="#007acc",
            box_shadow="0 4px 12px rgba(0,0,0,0.15)",
            transform="translateY(-2px)"
        ),
        
        CSS.selector(".sample-card h4",
            margin="0 0 10px 0",
            color="#333",
            font_size="16px"
        ),
        
        CSS.class_("sample-preview",
            background="#f8f9fa",
            border="1px solid #e9ecef",
            border_radius="4px",
            padding="12px",
            margin="0",
            font_family="'Courier New', Consolas, monospace",
            font_size="13px",
            line_height="1.4",
            overflow="auto",
            max_height="200px"
        ),
        
        CSS.selector(".sample-preview code",
            background="transparent",
            padding="0",
            color="#333"
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