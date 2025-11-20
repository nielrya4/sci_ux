"""Custom form component macros built without Bootstrap dependencies."""

from ..elements import *


def form_group(label_text, input_element, help_text=None, **kwargs):
    """Create a form group with label, input, and optional help text."""
    if "class_" in kwargs:
        kwargs["class_"] = f"form-group {kwargs['class_']}"
    else:
        kwargs["class_"] = "form-group"
    
    group = Div(**kwargs)
    
    # Label
    if label_text:
        label = Label(label_text, class_="form-label")
        if hasattr(input_element, 'id'):
            label.for_ = input_element.id
        group.add(label)
    
    # Input
    group.add(input_element)
    
    # Help text
    if help_text:
        help_div = Div(help_text, 
                      style="font-size: 0.875rem; color: #6c757d; margin-top: 0.25rem;")
        group.add(help_div)
    
    return group


def text_field(name, label=None, placeholder="", required=False, **kwargs):
    """Create a text input field."""
    if "class_" in kwargs:
        kwargs["class_"] = f"form-control {kwargs['class_']}"
    else:
        kwargs["class_"] = "form-control"
    
    input_attrs = {
        "type": "text",
        "name": name,
        "id": name,
        "placeholder": placeholder,
        **kwargs
    }
    
    if required:
        input_attrs["required"] = True
    
    text_input = Input(**input_attrs)
    
    if label:
        return form_group(label, text_input)
    
    return text_input


def email_field(name, label=None, placeholder="", required=False, **kwargs):
    """Create an email input field."""
    if "class_" in kwargs:
        kwargs["class_"] = f"form-control {kwargs['class_']}"
    else:
        kwargs["class_"] = "form-control"
    
    input_attrs = {
        "type": "email",
        "name": name,
        "id": name,
        "placeholder": placeholder or "Enter your email",
        **kwargs
    }
    
    if required:
        input_attrs["required"] = True
    
    email_input = Input(**input_attrs)
    
    if label:
        return form_group(label, email_input)
    
    return email_input


def password_field(name, label=None, placeholder="", required=False, **kwargs):
    """Create a password input field."""
    if "class_" in kwargs:
        kwargs["class_"] = f"form-control {kwargs['class_']}"
    else:
        kwargs["class_"] = "form-control"
    
    input_attrs = {
        "type": "password",
        "name": name,
        "id": name,
        "placeholder": placeholder or "Enter password",
        **kwargs
    }
    
    if required:
        input_attrs["required"] = True
    
    password_input = Input(**input_attrs)
    
    if label:
        return form_group(label, password_input)
    
    return password_input


def textarea_field(name, label=None, rows=3, placeholder="", required=False, **kwargs):
    """Create a textarea field."""
    if "class_" in kwargs:
        kwargs["class_"] = f"form-control {kwargs['class_']}"
    else:
        kwargs["class_"] = "form-control"
    
    textarea_attrs = {
        "name": name,
        "id": name,
        "rows": rows,
        "placeholder": placeholder,
        **kwargs
    }
    
    if required:
        textarea_attrs["required"] = True
    
    textarea_input = Textarea(**textarea_attrs)
    
    if label:
        return form_group(label, textarea_input)
    
    return textarea_input


def select_field(name, options, label=None, placeholder="Choose...", required=False, **kwargs):
    """Create a select dropdown field."""
    if "class_" in kwargs:
        kwargs["class_"] = f"form-control {kwargs['class_']}"
    else:
        kwargs["class_"] = "form-control"
    
    select_attrs = {
        "name": name,
        "id": name,
        **kwargs
    }
    
    if required:
        select_attrs["required"] = True
    
    select_input = Select(**select_attrs)
    
    # Add placeholder option
    if placeholder:
        select_input.add(Option(placeholder, value="", disabled=True, selected=True))
    
    # Add options
    for option in options:
        if isinstance(option, dict):
            opt = Option(option["text"], value=option.get("value", option["text"]))
            if option.get("selected"):
                opt.selected = True
        else:
            opt = Option(option, value=option)
        
        select_input.add(opt)
    
    if label:
        return form_group(label, select_input)
    
    return select_input


def checkbox_field(name, label, checked=False, **kwargs):
    """Create a checkbox field."""
    checkbox_style = (
        "margin-right: 0.5rem; "
        "transform: scale(1.2); "
        "accent-color: #007bff;"
    )
    
    if "style" in kwargs:
        kwargs["style"] = f"{checkbox_style} {kwargs['style']}"
    else:
        kwargs["style"] = checkbox_style
    
    input_attrs = {
        "type": "checkbox",
        "name": name,
        "id": name,
        **kwargs
    }
    
    if checked:
        input_attrs["checked"] = True
    
    checkbox_input = Input(**input_attrs)
    
    # Create wrapper with label
    wrapper = Div(style="margin-bottom: 1rem;")
    label_element = Label(
        [checkbox_input, " ", label],
        for_=name,
        style="display: flex; align-items: center; cursor: pointer; font-weight: 400;"
    )
    
    wrapper.add(label_element)
    return wrapper


def radio_field(name, options, label=None, **kwargs):
    """Create a radio button group."""
    wrapper = Div(style="margin-bottom: 1rem;")
    
    if label:
        wrapper.add(Label(label, 
                         style="display: block; margin-bottom: 0.5rem; font-weight: 500; color: #212529;"))
    
    for i, option in enumerate(options):
        radio_style = (
            "margin-right: 0.5rem; "
            "transform: scale(1.2); "
            "accent-color: #007bff;"
        )
        
        if isinstance(option, dict):
            value = option.get("value", option["text"])
            text = option["text"]
            checked = option.get("checked", False)
        else:
            value = option
            text = option
            checked = False
        
        radio_id = f"{name}_{i}"
        radio_input = Input(
            type="radio",
            name=name,
            id=radio_id,
            value=value,
            checked=checked,
            style=radio_style
        )
        
        radio_label = Label(
            [radio_input, " ", text],
            for_=radio_id,
            style="display: flex; align-items: center; cursor: pointer; margin-bottom: 0.5rem; font-weight: 400;"
        )
        
        wrapper.add(radio_label)
    
    return wrapper


def submit_button(text="Submit", color="primary", **kwargs):
    """Create a submit button."""
    if "class_" in kwargs:
        kwargs["class_"] = f"btn btn-{color} {kwargs['class_']}"
    else:
        kwargs["class_"] = f"btn btn-{color}"
    
    return Button(text, type="submit", **kwargs)


def reset_button(text="Reset", color="secondary", **kwargs):
    """Create a reset button."""
    if "class_" in kwargs:
        kwargs["class_"] = f"btn btn-{color} {kwargs['class_']}"
    else:
        kwargs["class_"] = f"btn btn-{color}"
    
    return Button(text, type="reset", **kwargs)


def button(text, color="primary", button_type="button", **kwargs):
    """Create a general button."""
    if "class_" in kwargs:
        kwargs["class_"] = f"btn btn-{color} {kwargs['class_']}"
    else:
        kwargs["class_"] = f"btn btn-{color}"
    
    return Button(text, type=button_type, **kwargs)


def form_actions(*buttons, alignment="left", **kwargs):
    """Create a form actions container for buttons."""
    align_style = {
        "left": "text-align: left;",
        "center": "text-align: center;",
        "right": "text-align: right;"
    }.get(alignment, "text-align: left;")
    
    actions_style = (
        f"{align_style} "
        "margin-top: 1.5rem; "
        "padding-top: 1rem; "
        "border-top: 1px solid #dee2e6;"
    )
    
    if "style" in kwargs:
        kwargs["style"] = f"{actions_style} {kwargs['style']}"
    else:
        kwargs["style"] = actions_style
    
    actions = Div(**kwargs)
    
    for i, button in enumerate(buttons):
        if i > 0:
            # Add spacing between buttons
            button_style = "margin-left: 0.5rem;"
            if hasattr(button, 'style'):
                button.style = f"{button_style} {button.style}"
            else:
                button.style = button_style
        
        actions.add(button)
    
    return actions


def file_field(name, label=None, accept=None, multiple=False, **kwargs):
    """Create a file upload field."""
    file_style = (
        "display: block; "
        "width: 100%; "
        "padding: 0.5rem 0.75rem; "
        "font-size: 1rem; "
        "line-height: 1.5; "
        "color: #495057; "
        "background-color: #fff; "
        "border: 1px solid #ced4da; "
        "border-radius: 0.375rem; "
        "transition: border-color 0.15s ease-in-out, box-shadow 0.15s ease-in-out;"
    )
    
    if "style" in kwargs:
        kwargs["style"] = f"{file_style} {kwargs['style']}"
    else:
        kwargs["style"] = file_style
    
    input_attrs = {
        "type": "file",
        "name": name,
        "id": name,
        **kwargs
    }
    
    if accept:
        input_attrs["accept"] = accept
    
    if multiple:
        input_attrs["multiple"] = True
    
    file_input = Input(**input_attrs)
    
    if label:
        return form_group(label, file_input)
    
    return file_input


def search_field(name, label=None, placeholder="Search...", **kwargs):
    """Create a search input field."""
    if "class_" in kwargs:
        kwargs["class_"] = f"form-control {kwargs['class_']}"
    else:
        kwargs["class_"] = "form-control"
    
    input_attrs = {
        "type": "search",
        "name": name,
        "id": name,
        "placeholder": placeholder,
        **kwargs
    }
    
    search_input = Input(**input_attrs)
    
    if label:
        return form_group(label, search_input)
    
    return search_input


def range_field(name, min_val=0, max_val=100, value=50, label=None, **kwargs):
    """Create a range slider field."""
    range_style = (
        "width: 100%; "
        "height: 0.5rem; "
        "border-radius: 0.25rem; "
        "background: #dee2e6; "
        "outline: none; "
        "appearance: none; "
        "-webkit-appearance: none;"
    )
    
    if "style" in kwargs:
        kwargs["style"] = f"{range_style} {kwargs['style']}"
    else:
        kwargs["style"] = range_style
    
    input_attrs = {
        "type": "range",
        "name": name,
        "id": name,
        "min": min_val,
        "max": max_val,
        "value": value,
        **kwargs
    }
    
    range_input = Input(**input_attrs)
    
    if label:
        return form_group(label, range_input)
    
    return range_input