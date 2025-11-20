"""Custom layout macros built from the ground up without Bootstrap dependencies."""

from ..elements import *
from ..styles.framework import create_custom_framework


def get_framework_css():
    """Get the CSS for our custom framework."""
    return create_custom_framework()


def container(content=None, fluid=False, **kwargs):
    """Create a container for page content using custom CSS."""
    class_name = "container-fluid" if fluid else "container"
    if "class_" in kwargs:
        kwargs["class_"] = f"{class_name} {kwargs['class_']}"
    else:
        kwargs["class_"] = class_name
    
    container_div = Div(**kwargs)
    if content:
        if isinstance(content, (list, tuple)):
            container_div.add(*content)
        else:
            container_div.add(content)
    
    return container_div


def row(*columns, **kwargs):
    """Create a row with columns using custom CSS."""
    if "class_" in kwargs:
        kwargs["class_"] = f"row {kwargs['class_']}"
    else:
        kwargs["class_"] = "row"
    
    row_div = Div(**kwargs)
    row_div.add(*columns)
    return row_div


def col(content=None, size=None, **kwargs):
    """Create a column with custom CSS grid system."""
    classes = []
    
    if size:
        classes.append(f"col-{size}")
    else:
        classes.append("col")
    
    class_str = " ".join(classes)
    if "class_" in kwargs:
        kwargs["class_"] = f"{class_str} {kwargs['class_']}"
    else:
        kwargs["class_"] = class_str
    
    col_div = Div(**kwargs)
    if content:
        if isinstance(content, (list, tuple)):
            col_div.add(*content)
        else:
            col_div.add(content)
    
    return col_div


def card(title=None, content=None, footer=None, **kwargs):
    """Create a card component using custom CSS."""
    if "class_" in kwargs:
        kwargs["class_"] = f"card {kwargs['class_']}"
    else:
        kwargs["class_"] = "card"
    
    card_div = Div(**kwargs)
    
    # Card header with title
    if title:
        card_header = Div(class_="card-header")
        card_header.add(H5(title, class_="card-title"))
        card_div.add(card_header)
    
    # Card body
    if content:
        card_body = Div(class_="card-body")
        if isinstance(content, str):
            card_body.add(P(content))
        else:
            card_body.add(content)
        card_div.add(card_body)
    
    # Card footer
    if footer:
        card_footer = Div(class_="card-footer")
        if isinstance(footer, str):
            card_footer.add(footer)
        else:
            card_footer.add(footer)
        card_div.add(card_footer)
    
    return card_div


def page_template(title="", stylesheets=None, scripts=None, body_content=None, **kwargs):
    """Create a complete HTML page template with custom CSS."""
    page = Html(lang="en")
    
    # Head section
    head = Head()
    head.add(
        Meta(charset="UTF-8"),
        Meta(name="viewport", content="width=device-width, initial-scale=1.0"),
        Title(title),
        Style(get_framework_css())  # Add our custom CSS framework
    )
    
    # Add external stylesheets
    if stylesheets:
        for stylesheet in stylesheets:
            if isinstance(stylesheet, str):
                head.add(Link(rel="stylesheet", href=stylesheet))
            else:
                head.add(stylesheet)
    
    page.add(head)
    
    # Body section
    body = Body(**kwargs)
    if body_content:
        body.add(body_content)
    
    # Add scripts
    if scripts:
        for script in scripts:
            if isinstance(script, str):
                body.add(Script(src=script))
            else:
                body.add(script)
    
    page.add(body)
    return page


def hero_section(title, subtitle=None, background_color="#f8f9fa", text_color="#333", **kwargs):
    """Create a hero section using custom CSS."""
    style = (
        f"background-color: {background_color}; "
        f"color: {text_color}; "
        f"padding: 4rem 0; "
        f"text-align: center; "
        f"min-height: 400px; "
        f"display: flex; "
        f"align-items: center;"
    )
    
    if "style" in kwargs:
        kwargs["style"] = f"{style} {kwargs['style']}"
    else:
        kwargs["style"] = style
    
    if "class_" in kwargs:
        kwargs["class_"] = f"hero-section {kwargs['class_']}"
    else:
        kwargs["class_"] = "hero-section"
    
    hero = Section(**kwargs)
    hero_content = container([
        H1(title, style="font-size: 3rem; margin-bottom: 1rem; font-weight: bold;"),
        P(subtitle, style="font-size: 1.25rem; margin-bottom: 0;") if subtitle else ""
    ])
    
    hero.add(hero_content)
    return hero


def navbar(brand=None, items=None, background_color="#fff", text_color="#333", **kwargs):
    """Create a navigation bar using custom CSS."""
    nav_style = (
        f"background-color: {background_color}; "
        f"color: {text_color}; "
        f"padding: 1rem 0; "
        f"border-bottom: 1px solid #dee2e6; "
        f"box-shadow: 0 2px 4px rgba(0,0,0,0.1);"
    )
    
    if "style" in kwargs:
        kwargs["style"] = f"{nav_style} {kwargs['style']}"
    else:
        kwargs["style"] = nav_style
    
    if "class_" in kwargs:
        kwargs["class_"] = f"navbar {kwargs['class_']}"
    else:
        kwargs["class_"] = "navbar"
    
    nav = Nav(**kwargs)
    nav_container = container([
        row([
            col([
                # Brand
                A(brand if brand else "Brand", 
                  href="#",
                  style=f"font-size: 1.5rem; font-weight: bold; text-decoration: none; color: {text_color};"),
            ], size=6),
            col([
                # Navigation items
                Div([
                    A(item["text"] if isinstance(item, dict) else str(item),
                      href=item.get("href", "#") if isinstance(item, dict) else "#",
                      style=f"margin-left: 2rem; text-decoration: none; color: {text_color}; font-weight: 500;")
                    for item in (items or [])
                ], style="text-align: right;")
            ], size=6)
        ])
    ])
    
    nav.add(nav_container)
    return nav


def sidebar_layout(sidebar_content, main_content, sidebar_width=3, **kwargs):
    """Create a sidebar layout using custom CSS."""
    main_width = 12 - sidebar_width
    
    layout_container = container([
        row([
            col([
                Div(sidebar_content,
                    style="background-color: #f8f9fa; padding: 2rem; min-height: 100vh; border-right: 1px solid #dee2e6;")
            ], size=sidebar_width),
            col([
                Div(main_content, style="padding: 2rem;")
            ], size=main_width)
        ])
    ])
    
    return layout_container


def footer(content=None, copyright_text=None, background_color="#f8f9fa", text_color="#6c757d", **kwargs):
    """Create a footer section using custom CSS."""
    footer_style = (
        f"background-color: {background_color}; "
        f"color: {text_color}; "
        f"padding: 3rem 0 1rem 0; "
        f"margin-top: auto; "
        f"border-top: 1px solid #dee2e6;"
    )
    
    if "style" in kwargs:
        kwargs["style"] = f"{footer_style} {kwargs['style']}"
    else:
        kwargs["style"] = footer_style
    
    if "class_" in kwargs:
        kwargs["class_"] = f"footer {kwargs['class_']}"
    else:
        kwargs["class_"] = "footer"
    
    footer_element = Footer(**kwargs)
    footer_container = container()
    
    if content:
        footer_container.add(content)
    
    # Copyright
    if copyright_text:
        copyright_row = row([
            col([
                Hr(style="margin: 2rem 0 1rem 0; border-color: #dee2e6;"),
                P(copyright_text, 
                  style=f"text-align: center; margin: 0; color: {text_color}; font-size: 0.9rem;")
            ])
        ])
        footer_container.add(copyright_row)
    
    footer_element.add(footer_container)
    return footer_element


def dashboard_layout(sidebar_items, main_content, title="Dashboard", **kwargs):
    """Create a dashboard layout with sidebar navigation using custom CSS."""
    dashboard_style = "min-height: 100vh; display: flex; flex-direction: column;"
    
    # Create the dashboard container
    dashboard = Div(style=dashboard_style, class_="dashboard")
    
    # Create sidebar content
    sidebar_content = [
        H4(title, style="margin-bottom: 2rem; color: #333; padding-bottom: 1rem; border-bottom: 2px solid #007bff;")
    ]
    
    # Add navigation items
    nav_list = []
    for item in sidebar_items:
        if isinstance(item, dict):
            nav_item = A(
                item["text"],
                href=item.get("href", "#"),
                style=(
                    "display: block; padding: 0.75rem 0; text-decoration: none; "
                    f"color: {'#007bff' if item.get('active') else '#6c757d'}; "
                    f"font-weight: {'600' if item.get('active') else '400'}; "
                    "border-bottom: 1px solid #e9ecef; transition: color 0.2s;"
                )
            )
        else:
            nav_item = A(
                item,
                href="#",
                style=(
                    "display: block; padding: 0.75rem 0; text-decoration: none; "
                    "color: #6c757d; font-weight: 400; border-bottom: 1px solid #e9ecef; "
                    "transition: color 0.2s;"
                )
            )
        nav_list.append(nav_item)
    
    sidebar_content.extend(nav_list)
    
    # Create the layout
    layout = sidebar_layout(sidebar_content, main_content, sidebar_width=3)
    dashboard.add(layout)
    
    return dashboard