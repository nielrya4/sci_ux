"""Layout macros for common page structures and grid systems."""

from ..elements import *


def page_template(*args, **kwargs):
    """Import page_template from components module."""
    from .components import page_template as _page_template
    return _page_template(*args, **kwargs)


def icon(*args, **kwargs):
    """Import icon from components module.""" 
    from .components import icon as _icon
    return _icon(*args, **kwargs)


def container(content=None, fluid=False, **kwargs):
    """Create a container for page content."""
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
    """Create a row with columns."""
    if "class_" in kwargs:
        kwargs["class_"] = f"row {kwargs['class_']}"
    else:
        kwargs["class_"] = "row"
    
    row_div = Div(**kwargs)
    row_div.add(*columns)
    return row_div


def col(content=None, size=None, sm=None, md=None, lg=None, xl=None, **kwargs):
    """Create a column with responsive sizing."""
    classes = []
    
    if size:
        classes.append(f"col-{size}")
    elif not any([sm, md, lg, xl]):
        classes.append("col")
    
    if sm:
        classes.append(f"col-sm-{sm}")
    if md:
        classes.append(f"col-md-{md}")
    if lg:
        classes.append(f"col-lg-{lg}")
    if xl:
        classes.append(f"col-xl-{xl}")
    
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


def grid_layout(layout, **kwargs):
    """Create a grid layout from a 2D array structure."""
    container_div = container(**kwargs)
    
    for row_data in layout:
        row_div = row()
        for col_data in row_data:
            if isinstance(col_data, dict):
                col_div = col(**col_data)
            else:
                col_div = col(col_data)
            row_div.add(col_div)
        container_div.add(row_div)
    
    return container_div


def sidebar_layout(sidebar_content, main_content, sidebar_position="left", sidebar_width=3, **kwargs):
    """Create a sidebar layout."""
    main_width = 12 - sidebar_width
    
    layout_container = container(**kwargs)
    layout_row = row()
    
    sidebar = col(sidebar_content, size=sidebar_width, class_="sidebar")
    main = col(main_content, size=main_width, class_="main-content")
    
    if sidebar_position == "left":
        layout_row.add(sidebar, main)
    else:
        layout_row.add(main, sidebar)
    
    layout_container.add(layout_row)
    return layout_container


def hero_section(title, subtitle=None, background_image=None, height="500px", **kwargs):
    """Create a hero section."""
    style = f"height: {height}; display: flex; align-items: center; justify-content: center;"
    if background_image:
        style += f" background-image: url('{background_image}'); background-size: cover; background-position: center;"
    
    if "style" in kwargs:
        kwargs["style"] = f"{style} {kwargs['style']}"
    else:
        kwargs["style"] = style
    
    if "class_" in kwargs:
        kwargs["class_"] = f"hero-section {kwargs['class_']}"
    else:
        kwargs["class_"] = "hero-section"
    
    hero = Section(**kwargs)
    hero_content = Div(class_="hero-content text-center")
    
    hero_content.add(H1(title, class_="hero-title"))
    if subtitle:
        hero_content.add(P(subtitle, class_="hero-subtitle"))
    
    hero.add(container(hero_content))
    return hero


def card(title=None, content=None, footer=None, image=None, **kwargs):
    """Create a card component."""
    if "class_" in kwargs:
        kwargs["class_"] = f"card {kwargs['class_']}"
    else:
        kwargs["class_"] = "card"
    card_div = Div(**kwargs)
    if image:
        if isinstance(image, str):
            card_div.add(Img(src=image, class_="card-img-top"))
        else:
            card_div.add(image)
    if title or content:
        card_body = Div(class_="card-body")
        if title:
            card_body.add(H5(title, class_="card-title"))
        if content:
            if isinstance(content, str):
                card_body.add(P(content, class_="card-text"))
            else:
                card_body.add(content)
        card_div.add(card_body)
    if footer:
        card_footer = Div(class_="card-footer")
        if isinstance(footer, str):
            card_footer.add(footer)
        else:
            card_footer.add(footer)
        card_div.add(card_footer)
    return card_div


def navbar(brand=None, items=None, fixed="top", color="light", background="light", **kwargs):
    """Create a navigation bar."""
    nav_classes = f"navbar navbar-expand-lg navbar-{color} bg-{background}"
    if fixed:
        nav_classes += f" fixed-{fixed}"
    
    if "class_" in kwargs:
        kwargs["class_"] = f"{nav_classes} {kwargs['class_']}"
    else:
        kwargs["class_"] = nav_classes
    
    navbar_nav = Nav(**kwargs)
    navbar_container = container(fluid=True)
    
    # Brand
    if brand:
        if isinstance(brand, dict):
            brand_link = A(brand["text"], class_="navbar-brand", href=brand.get("href", "#"))
        else:
            brand_link = A(brand, class_="navbar-brand", href="#")
        navbar_container.add(brand_link)
    
    # Toggle button for mobile
    navbar_container.add(
        Button(
            Span(class_="navbar-toggler-icon"),
            class_="navbar-toggler",
            type="button",
            data={"toggle": "collapse", "target": "#navbarNav"},
            aria={"controls": "navbarNav", "expanded": "false", "label": "Toggle navigation"}
        )
    )
    
    # Navigation items
    if items:
        nav_collapse = Div(class_="collapse navbar-collapse", id="navbarNav")
        nav_list = Ul(class_="navbar-nav")
        
        for item in items:
            nav_item = Li(class_="nav-item")
            
            if isinstance(item, dict):
                link = A(
                    item["text"],
                    class_="nav-link" + (" active" if item.get("active") else ""),
                    href=item.get("href", "#")
                )
            else:
                link = A(item, class_="nav-link", href="#")
            
            nav_item.add(link)
            nav_list.add(nav_item)
        
        nav_collapse.add(nav_list)
        navbar_container.add(nav_collapse)
    
    navbar_nav.add(navbar_container)
    return navbar_nav


def footer(content=None, copyright_text=None, links=None, **kwargs):
    """Create a footer section."""
    if "class_" in kwargs:
        kwargs["class_"] = f"footer {kwargs['class_']}"
    else:
        kwargs["class_"] = "footer"
    
    footer_element = Footer(**kwargs)
    footer_container = container()
    
    if content:
        footer_container.add(content)
    
    # Footer links
    if links:
        footer_row = row()
        for link_group in links:
            col_div = col(md=3)
            
            if isinstance(link_group, dict) and "title" in link_group:
                col_div.add(H6(link_group["title"]))
                link_list = Ul(class_="list-unstyled")
                for link in link_group.get("links", []):
                    if isinstance(link, dict):
                        link_item = Li(A(link["text"], href=link["href"]))
                    else:
                        link_item = Li(A(link, href="#"))
                    link_list.add(link_item)
                col_div.add(link_list)
            
            footer_row.add(col_div)
        
        footer_container.add(footer_row)
    
    # Copyright
    if copyright_text:
        copyright_row = row()
        copyright_col = col(class_="text-center")
        copyright_col.add(Hr(), P(copyright_text, class_="text-muted"))
        copyright_row.add(copyright_col)
        footer_container.add(copyright_row)
    
    footer_element.add(footer_container)
    return footer_element


def full_page_layout(title, navbar_config=None, main_content=None, footer_config=None, **kwargs):
    """Create a complete page layout with navbar, main content, and footer."""
    page = page_template(title=title, **kwargs)
    body = page.children[1]  # Get the body element
    
    # Add navbar
    if navbar_config:
        navbar_element = navbar(**navbar_config)
        body.add(navbar_element)
    
    # Add main content
    if main_content:
        main_element = Main(class_="main-content")
        main_element.add(main_content)
        body.add(main_element)
    
    # Add footer
    if footer_config:
        footer_element = footer(**footer_config)
        body.add(footer_element)
    
    return page


def dashboard_layout(sidebar_items, main_content, title="Dashboard", **kwargs):
    """Create a dashboard layout with sidebar navigation."""
    dashboard = Div(class_="dashboard")
    
    # Sidebar
    sidebar = Div(class_="sidebar")
    sidebar_nav = Nav(class_="sidebar-nav")
    
    sidebar_nav.add(H4(title, class_="sidebar-title"))
    
    nav_list = Ul(class_="nav flex-column")
    for item in sidebar_items:
        nav_item = Li(class_="nav-item")
        
        if isinstance(item, dict):
            link = A(
                item["text"],
                class_="nav-link" + (" active" if item.get("active") else ""),
                href=item.get("href", "#")
            )
            if "icon" in item:
                link.add(icon(item["icon"]), " ", item["text"])
        else:
            link = A(item, class_="nav-link", href="#")
        
        nav_item.add(link)
        nav_list.add(nav_item)
    
    sidebar_nav.add(nav_list)
    sidebar.add(sidebar_nav)
    
    # Main content
    main = Main(class_="main-content")
    main.add(main_content)
    
    dashboard.add(sidebar, main)
    return dashboard