#!/usr/bin/env python3
from py_html.elements import *
from py_html.macros.layouts import *

def create_about_content():
    """Create the about page content without the full HTML structure."""
    return Div(class_="app-container").add(
        # About content
        Div(style="background: white; padding: 40px; border-radius: 10px; margin: 20px 0;").add(
            H1("About Us", style="color: #2c3e50; text-align: center; margin-bottom: 30px;"),
            
            H2("Our Mission"),
            P("We are passionate about making Python web development easier and more accessible. Our py_html library allows developers to create beautiful web applications using only Python."),
            
            H2("Why py_html?"),
            P("Traditional web development requires knowledge of HTML, CSS, and JavaScript. With py_html, you can create complete web applications using just Python - from the backend logic to the frontend presentation."),
            
            H2("Get Started"),
            P("Ready to build your next web application with Python? Check out our documentation and start creating amazing web experiences today!")
        ),
        
        Footer().add(
            Div(class_="footer").add(
                P("Built with py_html library"),
                P("© 2024 Python UX Application")
            )
        )
    )