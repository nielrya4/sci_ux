"""
PyHTML - A Python library for generating HTML with a fluent API.

This library provides a clean, Pythonic way to generate HTML using classes
and method chaining. It includes support for CSS generation and a comprehensive
set of HTML elements and macros.
"""

# Core HTML elements and CSS
from .elements import *
from .css import *

# Macro imports for convenience
from .macros import *

__version__ = "1.0.0"
__author__ = "PyHTML Contributors"
__description__ = "A Python library for generating HTML with a fluent API"

# Make common macros available at the top level for convenience
from .macros.components import (
    document, page_template, breadcrumb, alert, badge, 
    progress_bar, icon, dropdown, tabs, pagination
)
from .macros.forms import (
    text_field, email_field, password_field, textarea_field,
    select_field, checkbox_field, radio_field, login_form, 
    contact_form, search_form
)
from .macros.layouts import (
    container, row, col, grid_layout, sidebar_layout,
    hero_section, card, navbar, footer, full_page_layout
)
from .macros.ui import (
    modal, accordion, carousel, tooltip, popover,
    offcanvas, toast, collapse, timeline, spinner
)