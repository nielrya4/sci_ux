#!/usr/bin/env python3
import js
from py_html.elements import *
from py_html.css import CSS

def create_about_page():
    """Create an about page using py_html elements."""
    
    # Simple styles for the about page
    styles = [
        CSS.class_("container",
            max_width="600px",
            margin="50px auto",
            padding="20px",
            font_family="Arial, sans-serif",
            text_align="center"
        ),
        CSS.class_("header",
            color="#2c3e50",
            border_bottom="2px solid #3498db",
            padding_bottom="20px",
            margin_bottom="30px"
        ),
        CSS.class_("content",
            line_height="1.6",
            font_size="16px",
            color="#333"
        )
    ]
    
    # Add styles to head
    style_element = f'<style>{"".join(str(style) for style in styles)}</style>'
    js.document.head.insertAdjacentHTML('beforeend', style_element)
    
    # Create the about page content
    about_content = Div(class_="container").add(
        Div(class_="header").add(
            H1("About Us"),
            P("Learn more about our mission and team")
        ),
        
        Div(class_="content").add(
            H2("Our Mission"),
            P("We are passionate about making Python web development easier and more accessible. Our py_html library allows developers to create beautiful web applications using only Python."),
            
            H2("Why py_html?"),
            P("Traditional web development requires knowledge of HTML, CSS, and JavaScript. With py_html, you can create complete web applications using just Python - from the backend logic to the frontend presentation."),
            
            H2("Get Started"),
            P("Ready to build your next web application with Python? Check out our documentation and start creating amazing web experiences today!"),
            
            P(A("← Back to Home", href="index.html", style="color: #3498db; text-decoration: none;"))
        )
    )
    
    return about_content

def render_to_dom():
    """Render the about page to the DOM."""
    try:
        page_content = create_about_page()
        html_content = str(page_content)
        
        # Find the content div and render our page
        content_div = js.document.getElementById('content')
        if content_div:
            content_div.innerHTML = html_content
            print("About page rendered successfully!")
        else:
            print("Could not find content div")
            
    except Exception as e:
        print(f"Error rendering about page: {e}")
        content_div = js.document.getElementById('content')
        if content_div:
            content_div.innerHTML = f'<div style="color: red; padding: 20px;">Error: {e}</div>'

# Main execution
print("Starting about.py in browser...")
render_to_dom()