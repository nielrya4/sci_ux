"""Custom UI component macros built without Bootstrap dependencies."""

from ..elements import *


def alert(message, alert_type="info", dismissible=False, **kwargs):
    """Create an alert/notification component using custom CSS."""
    if "class_" in kwargs:
        kwargs["class_"] = f"alert alert-{alert_type} {kwargs['class_']}"
    else:
        kwargs["class_"] = f"alert alert-{alert_type}"
    
    alert_div = Div(**kwargs)
    alert_div.add(message)
    
    if dismissible:
        close_button = Button(
            "×",
            style=(
                "background: none; border: none; font-size: 1.5rem; "
                "font-weight: bold; line-height: 1; color: inherit; "
                "opacity: 0.5; cursor: pointer; float: right; padding: 0; "
                "margin-left: 1rem;"
            ),
            onclick="this.parentElement.style.display='none'"
        )
        alert_div.add(close_button)
    
    return alert_div


def badge(text, badge_type="secondary", **kwargs):
    """Create a badge component using custom CSS."""
    if "class_" in kwargs:
        kwargs["class_"] = f"badge badge-{badge_type} {kwargs['class_']}"
    else:
        kwargs["class_"] = f"badge badge-{badge_type}"
    
    return Span(text, **kwargs)


def progress_bar(percentage, label=None, color="primary", **kwargs):
    """Create a progress bar using custom CSS."""
    # Progress container
    progress_style = (
        "display: flex; height: 1rem; background-color: #e9ecef; "
        "border-radius: 0.375rem; overflow: hidden; margin-bottom: 1rem;"
    )
    
    progress = Div(class_="progress", style=progress_style)
    
    # Progress bar
    bar_colors = {
        "primary": "#007bff",
        "secondary": "#6c757d", 
        "success": "#28a745",
        "danger": "#dc3545",
        "warning": "#ffc107",
        "info": "#17a2b8"
    }
    
    bg_color = bar_colors.get(color, bar_colors["primary"])
    
    bar_style = (
        f"width: {percentage}%; background-color: {bg_color}; "
        "display: flex; align-items: center; justify-content: center; "
        "color: white; font-size: 0.75rem; font-weight: bold; "
        "transition: width 0.6s ease;"
    )
    
    progress_bar_div = Div(
        label if label else f"{percentage}%",
        class_="progress-bar",
        style=bar_style,
        **kwargs
    )
    
    progress.add(progress_bar_div)
    return progress


def modal(modal_id, title, body, footer=None, size=None, **kwargs):
    """Create a modal dialog using custom CSS."""
    # Modal backdrop and container
    modal_style = (
        "position: fixed; top: 0; left: 0; z-index: 1050; "
        "width: 100%; height: 100%; background-color: rgba(0,0,0,0.5); "
        "display: none; align-items: center; justify-content: center;"
    )
    
    modal_div = Div(
        class_="modal",
        id=modal_id,
        style=modal_style,
        onclick="if(event.target === this) this.style.display='none'"
    )
    
    # Modal dialog sizing
    dialog_width = {
        "small": "300px",
        "large": "800px",
        "xl": "1200px"
    }.get(size, "500px")
    
    dialog_style = f"max-width: {dialog_width}; width: 90%; margin: auto;"
    
    modal_dialog = Div(class_="modal-dialog", style=dialog_style)
    
    # Modal content
    content_style = (
        "background-color: #fff; border-radius: 0.375rem; "
        "box-shadow: 0 0.5rem 1rem rgba(0,0,0,0.15); max-height: 90vh; "
        "overflow-y: auto;"
    )
    
    modal_content = Div(class_="modal-content", style=content_style)
    
    # Modal header
    header_style = (
        "display: flex; align-items: center; justify-content: space-between; "
        "padding: 1rem; border-bottom: 1px solid #dee2e6;"
    )
    
    modal_header = Div(class_="modal-header", style=header_style)
    modal_title = H5(title, style="margin: 0; font-weight: 500;")
    
    close_button = Button(
        "×",
        style=(
            "background: none; border: none; font-size: 1.5rem; "
            "font-weight: bold; line-height: 1; color: #6c757d; "
            "cursor: pointer; padding: 0;"
        ),
        onclick=f"document.getElementById('{modal_id}').style.display='none'"
    )
    
    modal_header.add(modal_title, close_button)
    
    # Modal body
    body_style = "padding: 1rem;"
    modal_body = Div(class_="modal-body", style=body_style)
    
    if isinstance(body, str):
        modal_body.add(P(body))
    else:
        modal_body.add(body)
    
    modal_content.add(modal_header, modal_body)
    
    # Modal footer
    if footer:
        footer_style = (
            "display: flex; align-items: center; justify-content: flex-end; "
            "padding: 1rem; border-top: 1px solid #dee2e6; gap: 0.5rem;"
        )
        
        modal_footer = Div(class_="modal-footer", style=footer_style)
        
        if isinstance(footer, list):
            modal_footer.add(*footer)
        else:
            modal_footer.add(footer)
        
        modal_content.add(modal_footer)
    
    modal_dialog.add(modal_content)
    modal_div.add(modal_dialog)
    
    return modal_div


def button_group(buttons, **kwargs):
    """Create a group of buttons."""
    group_style = "display: flex; gap: 0.5rem; margin-bottom: 1rem;"
    
    if "style" in kwargs:
        kwargs["style"] = f"{group_style} {kwargs['style']}"
    else:
        kwargs["style"] = group_style
    
    group = Div(class_="button-group", **kwargs)
    
    for button_config in buttons:
        if isinstance(button_config, dict):
            btn_text = button_config.get("text", "Button")
            btn_class = button_config.get("class_", "btn btn-primary")
            btn_data = button_config.get("data", {})
            btn_onclick = button_config.get("onclick", "")
            
            # Handle data attributes
            data_attrs = {}
            for key, value in btn_data.items():
                if key == "toggle" and value == "modal":
                    target = btn_data.get("target", "")
                    btn_onclick = f"document.querySelector('{target}').style.display='flex'"
                data_attrs[f"data-{key}"] = value
            
            btn = Button(
                btn_text,
                class_=btn_class,
                onclick=btn_onclick,
                **data_attrs
            )
        else:
            btn = button_config
        
        group.add(btn)
    
    return group


def accordion(accordion_id, items, **kwargs):
    """Create an accordion component."""
    accordion_style = "border: 1px solid #dee2e6; border-radius: 0.375rem; margin-bottom: 1rem;"
    
    accordion = Div(
        class_="accordion",
        id=accordion_id,
        style=accordion_style,
        **kwargs
    )
    
    for i, item in enumerate(items):
        item_id = f"{accordion_id}-item-{i}"
        
        # Accordion item
        item_style = "border-bottom: 1px solid #dee2e6;" if i < len(items) - 1 else ""
        accordion_item = Div(class_="accordion-item", style=item_style)
        
        # Accordion header
        header_style = (
            "padding: 0; margin: 0; background-color: #f8f9fa; "
            "border-bottom: 1px solid #dee2e6;" if item.get("show") else "border-bottom: none;"
        )
        
        accordion_header = Div(class_="accordion-header", style=header_style)
        
        # Accordion button
        button_style = (
            "width: 100%; padding: 1rem; text-align: left; "
            "background-color: transparent; border: none; "
            "font-size: 1rem; font-weight: 500; cursor: pointer; "
            "display: flex; justify-content: space-between; align-items: center;"
        )
        
        toggle_script = f"""
            var content = document.getElementById('{item_id}');
            var icon = this.querySelector('.accordion-icon');
            if (content.style.display === 'block') {{
                content.style.display = 'none';
                icon.textContent = '+';
                this.parentElement.style.borderBottom = 'none';
            }} else {{
                content.style.display = 'block';
                icon.textContent = '−';
                this.parentElement.style.borderBottom = '1px solid #dee2e6';
            }}
        """
        
        icon_text = "−" if item.get("show") else "+"
        
        accordion_button = Button(
            [
                item["title"],
                Span(icon_text, 
                    class_="accordion-icon",
                    style="font-weight: bold; font-size: 1.2rem;")
            ],
            style=button_style,
            onclick=toggle_script
        )
        
        accordion_header.add(accordion_button)
        
        # Accordion content
        content_display = "block" if item.get("show") else "none"
        content_style = f"padding: 1rem; display: {content_display};"
        
        accordion_content = Div(
            item["content"],
            id=item_id,
            class_="accordion-content",
            style=content_style
        )
        
        accordion_item.add(accordion_header, accordion_content)
        accordion.add(accordion_item)
    
    return accordion


def tabs(tab_items, **kwargs):
    """Create a tabbed interface."""
    tabs_container = Div(class_="tabs-container", **kwargs)
    
    # Tab navigation
    nav_style = (
        "display: flex; border-bottom: 1px solid #dee2e6; "
        "margin-bottom: 1rem; background-color: #f8f9fa;"
    )
    
    tab_nav = Div(class_="tab-nav", style=nav_style)
    
    # Tab content container
    content_style = "min-height: 200px;"
    tab_content = Div(class_="tab-content", style=content_style)
    
    for i, item in enumerate(tab_items):
        tab_id = item["id"]
        is_active = i == 0  # First tab is active by default
        
        # Tab button
        button_style = (
            f"padding: 0.75rem 1rem; border: none; background-color: transparent; "
            f"cursor: pointer; border-bottom: 2px solid "
            f"{'#007bff' if is_active else 'transparent'}; "
            f"color: {'#007bff' if is_active else '#6c757d'}; "
            f"font-weight: {'600' if is_active else '400'}; "
            "transition: all 0.2s ease;"
        )
        
        tab_button = Button(
            item["title"],
            style=button_style,
            onclick=f"showTab('{tab_id}')"
        )
        
        tab_nav.add(tab_button)
        
        # Tab pane
        pane_style = f"display: {'block' if is_active else 'none'};"
        
        tab_pane = Div(
            item["content"],
            id=tab_id,
            class_="tab-pane",
            style=pane_style
        )
        
        tab_content.add(tab_pane)
    
    # Add JavaScript for tab functionality
    script = Script(f"""
        function showTab(tabId) {{
            // Hide all tab panes
            var panes = document.querySelectorAll('.tab-pane');
            panes.forEach(function(pane) {{
                pane.style.display = 'none';
            }});
            
            // Remove active styling from all buttons
            var buttons = document.querySelectorAll('.tab-nav button');
            buttons.forEach(function(button) {{
                button.style.borderBottomColor = 'transparent';
                button.style.color = '#6c757d';
                button.style.fontWeight = '400';
            }});
            
            // Show selected tab pane
            document.getElementById(tabId).style.display = 'block';
            
            // Add active styling to clicked button
            event.target.style.borderBottomColor = '#007bff';
            event.target.style.color = '#007bff';
            event.target.style.fontWeight = '600';
        }}
    """)
    
    tabs_container.add(tab_nav, tab_content, script)
    return tabs_container


def toast(message, toast_type="info", title=None, **kwargs):
    """Create a toast notification."""
    toast_colors = {
        "info": {"bg": "#d1ecf1", "border": "#bee5eb", "color": "#0c5460"},
        "success": {"bg": "#d4edda", "border": "#c3e6cb", "color": "#155724"},
        "warning": {"bg": "#fff3cd", "border": "#ffeaa7", "color": "#856404"},
        "danger": {"bg": "#f8d7da", "border": "#f5c6cb", "color": "#721c24"}
    }
    
    colors = toast_colors.get(toast_type, toast_colors["info"])
    
    toast_style = (
        f"background-color: {colors['bg']}; "
        f"border: 1px solid {colors['border']}; "
        f"color: {colors['color']}; "
        "border-radius: 0.375rem; padding: 1rem; margin-bottom: 1rem; "
        "box-shadow: 0 0.125rem 0.25rem rgba(0,0,0,0.075); "
        "position: relative;"
    )
    
    toast_div = Div(class_=f"toast toast-{toast_type}", style=toast_style, **kwargs)
    
    if title:
        toast_header = Div(
            style="font-weight: 600; margin-bottom: 0.5rem; font-size: 0.9rem;"
        )
        toast_header.add(title)
        toast_div.add(toast_header)
    
    toast_div.add(message)
    
    # Close button
    close_button = Button(
        "×",
        style=(
            "position: absolute; top: 0.5rem; right: 0.5rem; "
            "background: none; border: none; font-size: 1.2rem; "
            "font-weight: bold; color: inherit; opacity: 0.7; "
            "cursor: pointer; padding: 0;"
        ),
        onclick="this.parentElement.style.display='none'"
    )
    
    toast_div.add(close_button)
    return toast_div


def timeline(events, **kwargs):
    """Create a timeline component."""
    timeline_style = (
        "position: relative; padding-left: 2rem; "
        "border-left: 2px solid #dee2e6; margin: 2rem 0;"
    )
    
    timeline_div = Div(class_="timeline", style=timeline_style, **kwargs)
    
    for event in events:
        # Timeline item
        item_style = (
            "position: relative; margin-bottom: 2rem; "
            "padding-left: 1rem; background-color: #fff;"
        )
        
        timeline_item = Div(class_="timeline-item", style=item_style)
        
        # Timeline marker
        marker_style = (
            "position: absolute; left: -2.5rem; top: 0; "
            "width: 1rem; height: 1rem; background-color: #007bff; "
            "border: 2px solid #fff; border-radius: 50%; "
            "box-shadow: 0 0 0 2px #dee2e6;"
        )
        
        marker = Div(class_="timeline-marker", style=marker_style)
        timeline_item.add(marker)
        
        # Event content
        if "title" in event:
            timeline_item.add(H6(event["title"], style="margin-bottom: 0.5rem; font-weight: 600;"))
        
        if "date" in event:
            timeline_item.add(Small(event["date"], style="color: #6c757d; margin-bottom: 0.5rem; display: block;"))
        
        if "description" in event:
            timeline_item.add(P(event["description"], style="margin-bottom: 0;"))
        
        timeline_div.add(timeline_item)
    
    return timeline_div