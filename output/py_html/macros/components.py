"""Basic HTML component macros for common patterns."""

from ..elements import *


def document(title="", lang="en", **kwargs):
    """Create a complete HTML5 document structure."""
    head = Head().add(
        Meta(charset="utf-8"),
        Meta(name="viewport", content="width=device-width, initial-scale=1"),
        Title(title) if title else None
    )
    
    body = Body(**kwargs)
    
    return Html(lang=lang).add(head, body)


def page_template(title="", stylesheets=None, scripts=None, body_content=None, **kwargs):
    """Create a complete page with common head elements."""
    head = Head().add(
        Meta(charset="utf-8"),
        Meta(name="viewport", content="width=device-width, initial-scale=1"),
        Title(title) if title else None
    )
    
    # Add stylesheets
    if stylesheets:
        for stylesheet in stylesheets:
            if isinstance(stylesheet, str):
                head.add(Link(rel="stylesheet", href=stylesheet))
            elif isinstance(stylesheet, dict):
                head.add(Link(rel="stylesheet", **stylesheet))
    
    body = Body()
    if body_content:
        if isinstance(body_content, (list, tuple)):
            body.add(*body_content)
        else:
            body.add(body_content)
    
    # Add scripts
    if scripts:
        for script in scripts:
            if isinstance(script, str):
                body.add(Script(src=script))
            elif isinstance(script, dict):
                body.add(Script(**script))
    
    return Html(lang=kwargs.get('lang', 'en')).add(head, body)


def breadcrumb(items):
    """Create a breadcrumb navigation."""
    nav = Nav(aria={"label": "breadcrumb"})
    ol = Ol(class_="breadcrumb")
    
    for i, item in enumerate(items):
        li = Li(class_="breadcrumb-item")
        
        if i == len(items) - 1:
            # Last item (current page)
            li.add(Span(item["text"], aria={"current": "page"}))
        else:
            # Regular link
            if "href" in item:
                li.add(A(item["text"], href=item["href"]))
            else:
                li.add(Span(item["text"]))
        
        ol.add(li)
    
    return nav.add(ol)


def alert(message, alert_type="info", dismissible=False):
    """Create an alert/notification component."""
    classes = f"alert alert-{alert_type}"
    if dismissible:
        classes += " alert-dismissible"
    
    alert_div = Div(class_=classes, role="alert")
    alert_div.add(message)
    
    if dismissible:
        alert_div.add(
            Button(
                Span("&times;", aria={"hidden": "true"}),
                type="button",
                class_="close",
                data={"dismiss": "alert"},
                aria={"label": "Close"}
            )
        )
    
    return alert_div


def badge(text, badge_type="secondary"):
    """Create a badge component."""
    return Span(text, class_=f"badge badge-{badge_type}")


def progress_bar(value, max_value=100, label=None, color="primary"):
    """Create a progress bar."""
    percentage = (value / max_value) * 100
    
    progress = Div(class_="progress")
    progress_bar_div = Div(
        class_=f"progress-bar bg-{color}",
        role="progressbar",
        style=f"width: {percentage}%",
        aria={"valuenow": str(value), "valuemin": "0", "valuemax": str(max_value)}
    )
    
    if label:
        progress_bar_div.add(label)
    
    progress.add(progress_bar_div)
    return progress


def icon(icon_name, library="fa", **kwargs):
    """Create an icon element."""
    if library == "fa":
        classes = f"fas fa-{icon_name}"
    elif library == "feather":
        classes = f"feather feather-{icon_name}"
    else:
        classes = f"{library}-{icon_name}"
    
    if "class_" in kwargs:
        classes += f" {kwargs['class_']}"
        kwargs["class_"] = classes
    else:
        kwargs["class_"] = classes
    
    return I(aria={"hidden": "true"}, **kwargs)


def button_group(buttons, **kwargs):
    """Create a group of buttons."""
    group = Div(class_="btn-group", role="group", **kwargs)
    
    for button in buttons:
        if isinstance(button, dict):
            btn = Button(**button)
        else:
            btn = button
        group.add(btn)
    
    return group


def dropdown(label, items, **kwargs):
    """Create a dropdown menu."""
    dropdown_div = Div(class_="dropdown")
    
    # Dropdown button
    button = Button(
        label,
        class_="btn btn-secondary dropdown-toggle",
        type="button",
        data={"toggle": "dropdown"},
        aria={"haspopup": "true", "expanded": "false"},
        **kwargs
    )
    
    # Dropdown menu
    menu = Div(class_="dropdown-menu", aria={"labelledby": button.id or "dropdownMenuButton"})
    
    for item in items:
        if item is None or item == "---":
            menu.add(Div(class_="dropdown-divider"))
        elif isinstance(item, dict):
            if "href" in item:
                menu.add(A(item["text"], class_="dropdown-item", href=item["href"]))
            else:
                menu.add(Button(item["text"], class_="dropdown-item", type="button"))
        else:
            menu.add(A(item, class_="dropdown-item", href="#"))
    
    dropdown_div.add(button, menu)
    return dropdown_div


def tabs(tab_items, active_tab=0):
    """Create a tabbed interface."""
    tab_container = Div()
    
    # Tab navigation
    nav = Nav()
    tab_list = Div(class_="nav nav-tabs", role="tablist")
    
    # Tab content
    content = Div(class_="tab-content")
    
    for i, tab in enumerate(tab_items):
        tab_id = tab.get("id", f"tab-{i}")
        is_active = i == active_tab
        
        # Tab link
        tab_link = A(
            tab["title"],
            class_=f"nav-link{'active' if is_active else ''}",
            id=f"{tab_id}-tab",
            data={"toggle": "tab"},
            href=f"#{tab_id}",
            role="tab",
            aria={"controls": tab_id, "selected": str(is_active).lower()}
        )
        tab_list.add(Div(tab_link, class_="nav-item"))
        
        # Tab content panel
        panel = Div(
            class_=f"tab-pane fade{'show active' if is_active else ''}",
            id=tab_id,
            role="tabpanel",
            aria={"labelledby": f"{tab_id}-tab"}
        )
        
        if "content" in tab:
            panel.add(tab["content"])
        
        content.add(panel)
    
    nav.add(tab_list)
    tab_container.add(nav, content)
    return tab_container


def pagination(current_page, total_pages, show_pages=5):
    """Create a pagination component."""
    nav = Nav(aria={"label": "Page navigation"})
    ul = Ul(class_="pagination")
    
    # Previous button
    prev_disabled = current_page <= 1
    prev_li = Li(class_="page-item" + (" disabled" if prev_disabled else ""))
    prev_link = A(
        "Previous",
        class_="page-link",
        href="#" if not prev_disabled else None,
        aria={"label": "Previous"}
    )
    if prev_disabled:
        prev_link = Span("Previous", class_="page-link")
    prev_li.add(prev_link)
    ul.add(prev_li)
    
    # Page numbers
    start_page = max(1, current_page - show_pages // 2)
    end_page = min(total_pages, start_page + show_pages - 1)
    
    for page in range(start_page, end_page + 1):
        li = Li(class_="page-item" + (" active" if page == current_page else ""))
        link = A(
            str(page),
            class_="page-link",
            href="#" if page != current_page else None
        )
        if page == current_page:
            link = Span(str(page), class_="page-link")
            li.aria = {"current": "page"}
        li.add(link)
        ul.add(li)
    
    # Next button
    next_disabled = current_page >= total_pages
    next_li = Li(class_="page-item" + (" disabled" if next_disabled else ""))
    next_link = A(
        "Next",
        class_="page-link",
        href="#" if not next_disabled else None,
        aria={"label": "Next"}
    )
    if next_disabled:
        next_link = Span("Next", class_="page-link")
    next_li.add(next_link)
    ul.add(next_li)
    
    nav.add(ul)
    return nav