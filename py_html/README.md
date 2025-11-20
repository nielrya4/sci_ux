# PyHTML - Build HTML with Python

PyHTML is a Python library that provides a clean, Pythonic way to generate HTML using classes and method chaining. It includes comprehensive HTML element support, CSS generation capabilities, and a rich macro library for common patterns.

## Features

- **Fluent API**: Build HTML with intuitive Python syntax
- **Complete HTML5 Support**: All HTML elements with proper attributes
- **CSS Integration**: Built-in CSS generation with the CSS module
- **Macro Library**: High-level macros for common patterns
- **Method Chaining**: Chainable API for clean, readable code
- **Type Safety**: Proper attribute handling with validation

## Installation

```bash
# Clone the repository or copy the py_html folder to your project
from py_html import *
```

## Quick Start

### Basic HTML Elements

```python
from py_html import *

# Create a simple page
page = Html().add(
    Head().add(
        Title("My Page"),
        Meta(charset="utf-8")
    ),
    Body().add(
        H1("Welcome to PyHTML"),
        P("This is a paragraph with ", A("a link", href="/about")),
        Div(
            Span("Nested content"),
            class_="container"
        )
    )
)

print(page.to_html())
```

### Using Macros

```python
from py_html.macros import *

# Create a complete page with navbar and footer
page = full_page_layout(
    title="My Website",
    navbar_config={
        "brand": {"text": "MyBrand", "href": "/"},
        "items": [
            {"text": "Home", "href": "/", "active": True},
            {"text": "About", "href": "/about"},
            {"text": "Contact", "href": "/contact"}
        ]
    },
    main_content=container(
        hero_section(
            title="Welcome to Our Site",
            subtitle="Building amazing things with PyHTML"
        ),
        row(
            col(
                card(
                    title="Feature 1",
                    content="Description of feature 1"
                ),
                md=4
            ),
            col(
                card(
                    title="Feature 2", 
                    content="Description of feature 2"
                ),
                md=4
            ),
            col(
                card(
                    title="Feature 3",
                    content="Description of feature 3"
                ),
                md=4
            )
        )
    ),
    footer_config={
        "copyright_text": "© 2024 MyCompany. All rights reserved."
    }
)
```

### Form Building

```python
from py_html.macros.forms import *

# Create a contact form
form = contact_form(action="/submit-contact")

# Or build custom forms
custom_form = Form(action="/register", method="post").add(
    text_field("username", "Username", required=True),
    email_field("email", "Email Address", required=True),
    password_field("password", "Password", required=True),
    select_field(
        "country",
        [("us", "United States"), ("uk", "United Kingdom")],
        label="Country"
    ),
    checkbox_field("newsletter", "Subscribe to newsletter"),
    form_actions(
        submit_button("Register"),
        reset_button("Clear")
    )
)
```

### UI Components

```python
from py_html.macros.ui import *

# Create a modal dialog
login_modal = modal(
    "loginModal",
    "Login Required",
    login_form(),
    footer=[
        Button("Cancel", class_="btn btn-secondary", data={"dismiss": "modal"}),
        Button("Login", class_="btn btn-primary", type="submit")
    ]
)

# Create an accordion
faq = accordion("faqAccordion", [
    {
        "title": "What is PyHTML?",
        "content": "PyHTML is a Python library for generating HTML.",
        "show": True
    },
    {
        "title": "How do I get started?",
        "content": "Check out our documentation and examples."
    }
])

# Create a carousel
image_slider = carousel("imageCarousel", [
    {"image": "/img1.jpg", "caption": {"title": "Image 1", "text": "Description"}},
    {"image": "/img2.jpg", "caption": {"title": "Image 2", "text": "Description"}},
    {"image": "/img3.jpg", "caption": {"title": "Image 3", "text": "Description"}}
])
```

## Library Structure

```
py_html/
├── __init__.py           # Main exports
├── elements.py           # HTML element classes
├── css.py               # CSS generation
└── macros/              # High-level macros
    ├── __init__.py      # Macro exports
    ├── components.py    # Basic component macros
    ├── forms.py         # Form macros
    ├── layouts.py       # Layout macros
    ├── ui.py            # UI component macros
    └── examples.py      # Usage examples
```

## Macro Categories

### Components (`macros.components`)
- `document()` - Complete HTML5 document
- `page_template()` - Page with head/body structure
- `breadcrumb()` - Navigation breadcrumbs
- `alert()` - Alert notifications
- `badge()` - Status badges
- `progress_bar()` - Progress indicators
- `dropdown()` - Dropdown menus
- `tabs()` - Tabbed interfaces
- `pagination()` - Page navigation

### Forms (`macros.forms`)
- `text_field()`, `email_field()`, `password_field()`
- `textarea_field()`, `select_field()`
- `checkbox_field()`, `radio_field()`
- `login_form()`, `contact_form()`, `search_form()`
- `form_group()`, `form_actions()`

### Layouts (`macros.layouts`)
- `container()`, `row()`, `col()` - Grid system
- `navbar()`, `footer()` - Page structure
- `hero_section()` - Hero banners
- `card()` - Content cards
- `sidebar_layout()` - Sidebar layouts
- `dashboard_layout()` - Admin dashboards

### UI (`macros.ui`)
- `modal()` - Modal dialogs
- `accordion()` - Collapsible content
- `carousel()` - Image/content sliders
- `tooltip()`, `popover()` - Overlays
- `offcanvas()` - Slide-out panels
- `toast()` - Notifications
- `timeline()` - Event timelines
- `spinner()` - Loading indicators

## CSS Integration

PyHTML includes a powerful CSS generation system:

```python
from py_html.css import *

# Create CSS rules
styles = CSSBuilder().add(
    CSSRule(".header").add(
        "background-color", "#f8f9fa"
    ).add(
        "padding", "1rem"
    ),
    CSSRule(".button").add(
        "background", "linear-gradient(45deg, #007bff, #0056b3)"
    ).add(
        "border", "none"
    ).add(
        "color", "white"
    )
)

# Add to page
page = page_template(
    title="Styled Page",
    body_content=[
        Style().add(styles),
        Div("Header", class_="header"),
        Button("Click me", class_="button")
    ]
)
```

## Examples

The `macros.examples` module contains complete examples:

- `example_login_page()` - Complete login page
- `example_dashboard()` - Admin dashboard with sidebar
- `example_landing_page()` - Modern landing page
- `example_modal_demo()` - Modal dialog showcase
- `example_form_showcase()` - Form components demo
- `example_component_showcase()` - UI components demo

```python
from py_html.macros.examples import example_landing_page

# Generate a complete landing page
page = example_landing_page()
with open("landing.html", "w") as f:
    f.write(page.to_html())
```

## Advanced Usage

### Custom Components

```python
def custom_card(title, content, variant="default"):
    \"\"\"Create a custom card component.\"\"\"
    classes = f"custom-card custom-card--{variant}"
    
    return Div(class_=classes).add(
        Div(class_="custom-card__header").add(
            H3(title, class_="custom-card__title")
        ),
        Div(class_="custom-card__body").add(content)
    )

# Usage
my_card = custom_card("My Title", "My content", variant="highlight")
```

### Extending Layouts

```python
def admin_page(title, sidebar_items, content):
    \"\"\"Create a consistent admin page layout.\"\"\"
    return full_page_layout(
        title=f"{title} - Admin Panel",
        navbar_config={
            "brand": {"text": "Admin", "href": "/admin"},
            "items": [
                {"text": "Dashboard", "href": "/admin"},
                {"text": "Users", "href": "/admin/users"},
                {"text": "Settings", "href": "/admin/settings"}
            ]
        },
        main_content=dashboard_layout(sidebar_items, content),
        footer_config={"copyright_text": "Admin Panel © 2024"}
    )
```

## Contributing

PyHTML is designed to be extensible. To add new macros:

1. Create functions in the appropriate macro module
2. Follow the existing naming conventions
3. Include proper documentation and type hints
4. Add examples demonstrating usage

## License

[Add your license information here]