#!/usr/bin/env python3
import js
from py_html.elements import *
from py_html.css import CSS
from pyodide.ffi import create_proxy
from sci_ux_components import NavItem, navbar, get_navbar_css
from home import create_home_content, setup_home_event_handlers
from about import create_about_content

def create_styles():
    # Include navbar styles
    navbar_css = get_navbar_css()
    
    return "\n".join(str(style) for style in [
        navbar_css.to_css(),
        CSS.class_("app-container",
            max_width="1200px",
            margin="0 auto", 
            padding="20px"
        ),
        CSS.class_("hero",
            background="linear-gradient(135deg, #667eea 0%, #764ba2 100%)",
            color="white",
            padding="60px 0",
            text_align="center",
            border_radius="10px",
            margin_bottom="30px"
        ),
        CSS.class_("feature-grid",
            display="grid",
            grid_template_columns="repeat(auto-fit, minmax(300px, 1fr))",
            gap="20px",
            margin="30px 0"
        ),
        CSS.class_("card",
            background="white",
            padding="20px",
            border_radius="8px",
            box_shadow="0 2px 10px rgba(0,0,0,0.1)",
            transition="transform 0.3s ease"
        ),
        CSS.selector(".card:hover",
            transform="translateY(-5px)"
        ),
        CSS.class_("btn-primary",
            background="#667eea",
            color="white",
            padding="12px 24px",
            border="none",
            border_radius="6px",
            cursor="pointer",
            font_size="16px",
            transition="background 0.3s ease"
        ),
        CSS.selector(".btn-primary:hover",
            background="#5a6fd8"
        ),
        CSS.class_("footer",
            text_align="center",
            margin_top="50px",
            padding_top="30px",
            border_top="1px solid #eee",
            color="#666"
        ),
        CSS.class_("form-section",
            margin="40px 0"
        ),
        CSS.class_("demo-section",
            margin="40px 0"
        ),
        CSS.class_("demo-content",
            background="white",
            padding="20px",
            border_radius="8px",
            box_shadow="0 2px 10px rgba(0,0,0,0.1)"
        )
    ] if str(style))

def create_navbar():
    """Create the navigation bar with consistent structure."""
    return navbar([
        NavItem("Home", "home"),
        NavItem("About", "about"),
        NavItem("Features", "#", children=[
            NavItem("HTML Generation", "home"),
            NavItem("CSS Styling", "home"),
            NavItem("Interactive Components", "home")
        ]),
        NavItem("Documentation", "#", children=[
            NavItem("Getting Started", "home"),
            NavItem("API Reference", "home"),
            NavItem("Examples", "about")
        ]),
        NavItem("Contact", "about")
    ])


def render_page_content(page_content):
    """Render page content with navbar to the DOM."""
    try:
        # Ensure styles are in the head
        if not js.document.getElementById('app-styles'):
            style_element = f'<style id="app-styles">{create_styles()}</style>'
            js.document.head.insertAdjacentHTML('beforeend', style_element)
        
        # Create the complete page structure
        full_content = Div().add(
            create_navbar(),
            page_content
        )
        
        # Render to DOM
        html_content = str(full_content)
        js.document.body.innerHTML = html_content
        
        # Re-setup event handlers after page change
        setup_event_handlers()
            
    except Exception as e:
        print(f"Error rendering page: {e}")
        # Fallback content
        js.document.body.innerHTML = str(Div(style="padding: 20px; text-align: center;").add(
            H1("Error Loading Page"),
            P("Application encountered an error!"),
            P(f"Error: {e}", style="color: red;")
        ))

def render_home():
    """Render the home page content."""
    home_content = create_home_content()
    render_page_content(home_content)
    # Set up home-specific event handlers with a small delay to ensure DOM is ready
    home_handler_proxy = create_proxy(setup_home_event_handlers)
    js.setTimeout(home_handler_proxy, 50)

def render_about():
    """Render the about page content."""
    about_content = create_about_content()
    render_page_content(about_content)


def setup_event_handlers():
    
    def handle_nav_click(event):
        if event.target.classList.contains('spa-link'):
            event.preventDefault()
            page = event.target.getAttribute('data-page')
            if page == 'home':
                render_home()
            elif page == 'about':
                render_about()
    
    # Create proxies
    nav_handler = create_proxy(handle_nav_click)
    
    # Set up navigation handlers
    nav_links = js.document.querySelectorAll('.spa-link')
    for link in nav_links:
        link.addEventListener('click', nav_handler)


# Main execution
if __name__ == "__main__":
    render_home()
