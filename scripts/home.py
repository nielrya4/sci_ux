#!/usr/bin/env python3
import js
from py_html.elements import *
from py_html.macros.components import *
from py_html.macros.layouts import *
from py_html.macros.forms import *
from py_html.macros.ui import *
from py_html.css import CSS
from py_dom import events, on_click, on_escape
import include

def create_home_content():
    """Create the home page content without the full HTML structure."""
    return Div(class_="app-container").add(
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
    # Use a small delay to ensure modal DOM is ready
    from pyodide.ffi import create_proxy
    setup_handler_proxy = create_proxy(setup_modal_handlers)
    js.setTimeout(setup_handler_proxy, 10)

def setup_modal_handlers():

    def close_modal(event):
        modal = js.document.getElementById('feature-modal')
        if modal:
            modal.remove()
    
    def handle_overlay_click(event):
        if event.target.id == 'feature-modal':
            close_modal(event)
    
    # Add event listeners using py_dom
    on_click('modal-close-btn', close_modal)
    on_click('modal-got-it-btn', close_modal)
    events.add_listener('feature-modal', 'click', handle_overlay_click)

def setup_home_event_handlers():
    """Set up event handlers specific to the home page."""
    
    def handle_html_click(event):
        show_feature('html')
    
    def handle_css_click(event):
        show_feature('css')
    
    def handle_interactive_click(event):
        show_feature('interactive')
    
    # Set up feature button handlers using py_dom
    on_click('btn-html', handle_html_click)
    on_click('btn-css', handle_css_click)
    on_click('btn-interactive', handle_interactive_click)
    
    # Set up global escape key handler
    setup_global_modal_handlers()

def setup_global_modal_handlers():
    """Set up global modal handlers that persist across page navigations."""
    
    def handle_escape_key_global(event):
        modal = js.document.getElementById('feature-modal')
        if modal:
            modal.remove()
    
    # Remove any existing global escape handler
    events.remove_document_listener('keydown')
    
    # Add new global escape handler using py_dom
    on_escape(handle_escape_key_global)