# Sci-UX
### A framework for building single-page front-end-only Python web apps for science and education
#### Required: knowledge of  Python and DOM elements
### How it works:
* Python files are written in the scripts folder
  * py_html is a homebrewed library that eliminates the need for writing any HTML
  * Scripts are written to target Pyodide, a web-assembly Python interpreter
* Build.py is configured and executed (on a local interpreter) to gather dependencies and set up the app
* The folder specified in build.py then houses a fully self-contained Python web app

### Future steps:
* Tools and macros for building spreadsheets, graphs, etc.
* Leaflet maps
* Data request forms
* In-browser Python scripting 

### To download this code and run the example:
```shell
git clone https://www.github.com/nielrya4/sci_ux.git
cd sci_ux
python3 -m venv venv
. venv/bin/activate
python build.py
python -m http.server 8000
# Then, in your web browser of choice, navigate to http://127.0.0.1:8000
```


## The following examples are snippets from ./scripts/main.py
### Example py_html code:
```python
from py_html.macros.layouts import *
from py_html.macros.forms import *
from py_html.macros.ui import *

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
```
* DOM elements are capitalized
* Macros defined by the library or the developer are lower-case
* py_html supports chaining methods to give a feel similar to HTML while avoiding redundant closing tags
* Pythonic, declarative syntax for frontend development
* This becomes very powerful when coupled with Pyodide's js library for manipulating the DOM

### Pyodide example:
```python
# This code snippet targets the Pyodide interpreter, 
# which comes pre-loaded with pyodide.ffi and js libraries
from pyodide.ffi import create_proxy
import js

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
```
