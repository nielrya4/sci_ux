"""Form macros for common form patterns and components."""

from ..elements import *


def form_group(label_text, input_element, help_text=None, required=False, **kwargs):
    """Create a form group with label, input, and optional help text."""
    group = Div(class_="form-group", **kwargs)
    
    # Create label
    label = Label(label_text, class_="form-label")
    if required:
        label.add(" ", Span("*", class_="text-danger"))
    
    # Set input classes
    if hasattr(input_element, 'class_'):
        input_element.class_ = f"{input_element.class_ or ''} form-control".strip()
    else:
        input_element.class_ = "form-control"
    
    if required and hasattr(input_element, 'required'):
        input_element.required = True
    
    group.add(label, input_element)
    
    # Add help text if provided
    if help_text:
        help_div = Small(help_text, class_="form-text text-muted")
        group.add(help_div)
    
    return group


def text_field(name, label=None, placeholder=None, value=None, required=False, **kwargs):
    """Create a text input field with label."""
    input_el = Input(
        type="text",
        name=name,
        placeholder=placeholder,
        value=value,
        required=required,
        **kwargs
    )
    
    if label:
        return form_group(label, input_el, required=required)
    
    return input_el


def email_field(name, label=None, placeholder=None, value=None, required=False, **kwargs):
    """Create an email input field with label."""
    input_el = Input(
        type="email",
        name=name,
        placeholder=placeholder or "Enter your email",
        value=value,
        required=required,
        **kwargs
    )
    
    if label:
        return form_group(label, input_el, required=required)
    
    return input_el


def password_field(name, label=None, placeholder=None, required=False, **kwargs):
    """Create a password input field with label."""
    input_el = Input(
        type="password",
        name=name,
        placeholder=placeholder or "Enter your password",
        required=required,
        **kwargs
    )
    
    if label:
        return form_group(label, input_el, required=required)
    
    return input_el


def textarea_field(name, label=None, placeholder=None, rows=3, value=None, required=False, **kwargs):
    """Create a textarea field with label."""
    textarea_el = Textarea(
        value or "",
        name=name,
        placeholder=placeholder,
        rows=rows,
        required=required,
        **kwargs
    )
    
    if label:
        return form_group(label, textarea_el, required=required)
    
    return textarea_el


def select_field(name, options, label=None, selected=None, required=False, **kwargs):
    """Create a select dropdown field with label."""
    select_el = Select(name=name, required=required, **kwargs)
    
    for option in options:
        if isinstance(option, dict):
            opt = Option(
                option["text"],
                value=option["value"],
                selected=option["value"] == selected
            )
        elif isinstance(option, (list, tuple)) and len(option) == 2:
            value, text = option
            opt = Option(text, value=value, selected=value == selected)
        else:
            opt = Option(option, value=option, selected=option == selected)
        
        select_el.add(opt)
    
    if label:
        return form_group(label, select_el, required=required)
    
    return select_el


def checkbox_field(name, label_text, checked=False, value="1", **kwargs):
    """Create a checkbox field with label."""
    group = Div(class_="form-check", **kwargs)
    
    checkbox = Input(
        type="checkbox",
        name=name,
        value=value,
        checked=checked,
        class_="form-check-input"
    )
    
    label = Label(label_text, class_="form-check-label")
    
    group.add(checkbox, label)
    return group


def radio_field(name, options, selected=None, **kwargs):
    """Create radio button group."""
    group = Div(class_="form-group", **kwargs)
    
    for option in options:
        radio_group = Div(class_="form-check")
        
        if isinstance(option, dict):
            value = option["value"]
            text = option["text"]
        elif isinstance(option, (list, tuple)) and len(option) == 2:
            value, text = option
        else:
            value = text = option
        
        radio = Input(
            type="radio",
            name=name,
            value=value,
            checked=value == selected,
            class_="form-check-input"
        )
        
        label = Label(text, class_="form-check-label")
        
        radio_group.add(radio, label)
        group.add(radio_group)
    
    return group


def file_field(name, label=None, accept=None, multiple=False, required=False, **kwargs):
    """Create a file upload field with label."""
    input_el = Input(
        type="file",
        name=name,
        accept=accept,
        multiple=multiple,
        required=required,
        class_="form-control-file",
        **kwargs
    )
    
    if label:
        return form_group(label, input_el, required=required)
    
    return input_el


def hidden_field(name, value, **kwargs):
    """Create a hidden input field."""
    return Input(type="hidden", name=name, value=value, **kwargs)


def submit_button(text="Submit", button_class="btn btn-primary", **kwargs):
    """Create a submit button."""
    return Button(text, type="submit", class_=button_class, **kwargs)


def reset_button(text="Reset", button_class="btn btn-secondary", **kwargs):
    """Create a reset button."""
    return Button(text, type="reset", class_=button_class, **kwargs)


def form_actions(*buttons, alignment="left"):
    """Create a form actions container with buttons."""
    classes = "form-actions"
    if alignment == "right":
        classes += " text-right"
    elif alignment == "center":
        classes += " text-center"
    
    actions = Div(class_=classes)
    actions.add(*buttons)
    return actions


def login_form(action="/login", method="post", **kwargs):
    """Create a standard login form."""
    form = Form(action=action, method=method, **kwargs)
    
    form.add(
        email_field("email", "Email", required=True),
        password_field("password", "Password", required=True),
        Div(
            checkbox_field("remember", "Remember me"),
            class_="mb-3"
        ),
        form_actions(
            submit_button("Login"),
            alignment="right"
        )
    )
    
    return form


def contact_form(action="/contact", method="post", **kwargs):
    """Create a standard contact form."""
    form = Form(action=action, method=method, **kwargs)
    
    form.add(
        text_field("name", "Name", required=True),
        email_field("email", "Email", required=True),
        text_field("subject", "Subject", required=True),
        textarea_field("message", "Message", rows=5, required=True),
        form_actions(
            submit_button("Send Message"),
            reset_button("Clear"),
            alignment="right"
        )
    )
    
    return form


def search_form(action="/search", placeholder="Search...", button_text="Search", **kwargs):
    """Create a search form."""
    form = Form(action=action, method="get", class_="form-inline", **kwargs)
    
    search_input = Input(
        type="search",
        name="q",
        placeholder=placeholder,
        class_="form-control mr-2"
    )
    
    search_button = Button(
        button_text,
        type="submit",
        class_="btn btn-outline-success"
    )
    
    form.add(search_input, search_button)
    return form


def inline_form(fields, action="#", method="post", **kwargs):
    """Create an inline form with multiple fields."""
    form = Form(action=action, method=method, class_="form-inline", **kwargs)
    
    for field in fields:
        if isinstance(field, dict):
            field_type = field.get("type", "text")
            if field_type == "text":
                form.add(text_field(**field))
            elif field_type == "email":
                form.add(email_field(**field))
            elif field_type == "select":
                form.add(select_field(**field))
            elif field_type == "button":
                form.add(Button(**field))
        else:
            form.add(field)
    
    return form