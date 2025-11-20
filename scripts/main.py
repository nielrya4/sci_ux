#!/usr/bin/env python3
import js
from py_html.elements import *
from py_html.macros.components import *
from py_html.macros.layouts import *
from py_html.macros.forms import *
from py_html.macros.ui import *
from py_html.css import CSS
import include
from pyodide.ffi import create_proxy

def create_styles():
    return "\n".join(str(style) for style in [
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

def create_main_page():
    return Html(lang="en").add(
        Head().add(
            Meta(charset="utf-8"),
            Meta(name="viewport", content="width=device-width, initial-scale=1"),
            Title("Python UX Application"),
            Style(create_styles())
        ),
        Body().add(
            Div(class_="app-container").add(
                # Hero section
                Div(class_="hero").add(
                    H1("Welcome to Python UX Application"),
                    P("A modern web application built with Python and py_html")
                ),
                include.hi(),
                Div(class_="feature-grid").add(
                    card(
                        title="HTML Generation",
                        content=P("Generate clean, semantic HTML using Python code with a fluent API."),
                        footer=Button("Learn More", class_="btn-primary", id="btn-html")
                    ),
                    card(
                        title="CSS Styling", 
                        content=P("Create beautiful styles with Python, no separate CSS files needed."),
                        footer=Button("Learn More", class_="btn-primary", id="btn-css")
                    ),
                    card(
                        title="Interactive Components",
                        content=P("Build interactive UIs with forms, modals, and dynamic content."),
                        footer=Button("Learn More", class_="btn-primary", id="btn-interactive")
                    )
                ),
                Div(class_="form-section").add(
                    H2("Try it out!"),
                    contact_form(action="#", method="post")
                ),
                Div(class_="demo-section").add(
                    H2("Interactive Demo"),
                    Div(class_="demo-content").add(
                        P("This is a demonstration of the py_html library capabilities."),
                        P("You can create interactive web applications using Python!")
                    )
                ),
                Footer().add(
                    Div(class_="footer").add(
                        P("Built with py_html library"),
                        P("© 2024 Python UX Application")
                    )
                )
            )
        )
    )

def render_to_dom():
    try:
        page = create_main_page()
        html_content = str(page)
        content_div = js.document.getElementById('content')
        if content_div:
            content_div.innerHTML = html_content
        else:
            js.document.body.innerHTML = html_content
        setup_event_handlers()
            
    except Exception as e:
        print(f"Error rendering page: {e}")
        # Fallback content
        content_div = js.document.getElementById('content')
        if content_div:
            content_div.innerHTML = Div(style="padding: 20px; text-align: center;").add(
                H1("Python UX Application"),
                P("Application loaded successfully!"),
                P(f"Error: {e}", style="color: red;")
            )


def setup_event_handlers():
    
    def handle_html_click(event):
        show_feature('html')
    
    def handle_css_click(event):
        show_feature('css')
    
    def handle_interactive_click(event):
        show_feature('interactive')
    
    html_handler = create_proxy(handle_html_click)
    css_handler = create_proxy(handle_css_click)
    interactive_handler = create_proxy(handle_interactive_click)
    html_btn = js.document.getElementById('btn-html')
    if html_btn:
        html_btn.addEventListener('click', html_handler)
    css_btn = js.document.getElementById('btn-css')
    if css_btn:
        css_btn.addEventListener('click', css_handler)
    interactive_btn = js.document.getElementById('btn-interactive')
    if interactive_btn:
        interactive_btn.addEventListener('click', interactive_handler)

def create_modal_styles():
    return [
        CSS.class_("modal-overlay",
            position="fixed",
            top="0",
            left="0", 
            width="100%",
            height="100%",
            background="rgba(0,0,0,0.8)",
            display="flex",
            justify_content="center",
            align_items="center",
            z_index="1000"
        ),
        CSS.class_("modal-content",
            background="white",
            padding="30px",
            border_radius="10px",
            max_width="600px",
            max_height="80vh",
            overflow_y="auto",
            box_shadow="0 10px 30px rgba(0,0,0,0.3)"
        ),
        CSS.class_("modal-header",
            display="flex",
            justify_content="space-between",
            align_items="center",
            margin_bottom="20px"
        ),
        CSS.class_("modal-title",
            margin="0",
            color="#333"
        ),
        CSS.class_("modal-close",
            background="none",
            border="none",
            font_size="24px",
            cursor="pointer",
            color="#666"
        ),
        CSS.class_("modal-description",
            color="#666",
            font_size="16px",
            line_height="1.5"
        ),
        CSS.class_("modal-section-title",
            color="#333",
            margin_top="25px"
        ),
        CSS.class_("modal-features-list",
            color="#555",
            line_height="1.6"
        ),
        CSS.class_("modal-code-example",
            background="#f8f9fa",
            padding="15px",
            border_radius="5px",
            overflow_x="auto",
            border_left="4px solid #667eea"
        ),
        CSS.class_("modal-footer",
            text_align="right",
            margin_top="25px"
        ),
        CSS.class_("modal-button",
            background="#667eea",
            color="white",
            padding="10px 20px",
            border="none",
            border_radius="5px",
            cursor="pointer",
            font_size="14px"
        )
    ]

def create_modal(feature_info):
    return Div(class_="modal-overlay", id="feature-modal").add(
        Div(class_="modal-content").add(
            Div(class_="modal-header").add(
                H2(feature_info['title'], class_="modal-title"),
                Button("×", class_="modal-close", id="modal-close-btn")
            ),
            P(feature_info['description'], class_="modal-description"),
            H3("Key Features:", class_="modal-section-title"),
            Ul(class_="modal-features-list").add(
                *[Li(detail) for detail in feature_info['details']]
            ),
            H3("Example:", class_="modal-section-title"),
            Pre(
                Code(feature_info['code_example'].strip()), 
                class_="modal-code-example"
            ),
            Div(class_="modal-footer").add(
                Button("Got it!", class_="modal-button", id="modal-got-it-btn")
            )
        )
    )

def show_feature(feature_type):
    """Show detailed information about a feature."""
    
    # Feature information
    features = {
        'html': {
            'title': 'HTML Generation',
            'description': 'Generate clean, semantic HTML using Python code with a fluent API.',
            'details': [
                'Create HTML elements with Python classes',
                'Method chaining for building complex structures',
                'Automatic attribute handling and validation',
                'Support for all HTML5 elements',
                'Clean, readable Python code'
            ],
            'code_example': '''
# Create a card with py_html
card_element = Div(class_="card")
card_element.add(
    H3("Card Title"),
    P("Card content goes here"),
    Button("Click me", class_="btn")
)
'''
        },
        'css': {
            'title': 'CSS Styling',
            'description': 'Create beautiful styles with Python, no separate CSS files needed.',
            'details': [
                'Inline styles with Python dictionaries',
                'CSS classes generated programmatically',
                'Style objects for reusable styling',
                'Dynamic style generation',
                'Integration with popular CSS frameworks'
            ],
            'code_example': '''
# Add styles with py_html CSS module
from py_html.css import CSS

# Create CSS rules with Python
my_style = CSS.class_("my-class",
    background="linear-gradient(45deg, #blue, #purple)",
    padding="20px",
    border_radius="8px"
)

# Add to Style element
head.add(Style(str(my_style)))
'''
        },
        'interactive': {
            'title': 'Interactive Components',
            'description': 'Build interactive UIs with forms, modals, and dynamic content.',
            'details': [
                'Form components with validation',
                'Modal dialogs and overlays',
                'Dynamic content updates',
                'Event handling integration',
                'State management helpers'
            ],
            'code_example': '''
# Create interactive form
form = contact_form(
    action="/submit",
    method="post"
)
form.add_validation("email", "required|email")
'''
        }
    }
    
    feature_info = features.get(feature_type, features['html'])
    modal = create_modal(feature_info)
    if not js.document.getElementById('modal-styles'):
        modal_styles = create_modal_styles()
        style_content = "\n".join(str(style) for style in modal_styles)
        style_element = f'<style id="modal-styles">{style_content}</style>'
        js.document.head.insertAdjacentHTML('beforeend', style_element)
    js.document.body.insertAdjacentHTML('beforeend', str(modal))
    setup_modal_handlers()

def setup_modal_handlers():

    def close_modal(event):
        modal = js.document.getElementById('feature-modal')
        if modal:
            modal.remove()
    
    def handle_overlay_click(event):
        if event.target.id == 'feature-modal':
            close_modal(event)
    
    def handle_escape_key(event):
        if event.key == 'Escape':
            close_modal(event)
    
    # Create proxies for event handlers
    close_handler = create_proxy(close_modal)
    overlay_handler = create_proxy(handle_overlay_click)
    escape_handler = create_proxy(handle_escape_key)
    
    # Add event listeners
    close_btn = js.document.getElementById('modal-close-btn')
    if close_btn:
        close_btn.addEventListener('click', close_handler)
    
    got_it_btn = js.document.getElementById('modal-got-it-btn')
    if got_it_btn:
        got_it_btn.addEventListener('click', close_handler)
    
    modal = js.document.getElementById('feature-modal')
    if modal:
        modal.addEventListener('click', overlay_handler)
    
    js.document.addEventListener('keydown', escape_handler)

# Main execution
if __name__ == "__main__":
    render_to_dom()
