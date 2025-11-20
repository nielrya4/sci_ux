"""UI component macros for advanced interactive elements."""

from ..elements import *
from .components import icon


def modal(id, title, body, footer=None, size=None, **kwargs):
    """Create a modal dialog."""
    modal_classes = "modal fade"
    dialog_classes = "modal-dialog"
    
    if size:
        dialog_classes += f" modal-{size}"
    
    # Modal backdrop
    modal_div = Div(
        class_=modal_classes,
        id=id,
        tabindex="-1",
        aria={"hidden": "true", "labelledby": f"{id}Label"},
        **kwargs
    )
    
    # Modal dialog
    modal_dialog = Div(class_=dialog_classes)
    modal_content = Div(class_="modal-content")
    
    # Modal header
    modal_header = Div(class_="modal-header")
    modal_title = H5(title, class_="modal-title", id=f"{id}Label")
    close_button = Button(
        Span("&times;", aria={"hidden": "true"}),
        type="button",
        class_="close",
        data={"dismiss": "modal"},
        aria={"label": "Close"}
    )
    modal_header.add(modal_title, close_button)
    
    # Modal body
    modal_body = Div(class_="modal-body")
    if isinstance(body, str):
        modal_body.add(P(body))
    else:
        modal_body.add(body)
    
    modal_content.add(modal_header, modal_body)
    
    # Modal footer
    if footer:
        modal_footer = Div(class_="modal-footer")
        if isinstance(footer, (list, tuple)):
            modal_footer.add(*footer)
        else:
            modal_footer.add(footer)
        modal_content.add(modal_footer)
    
    modal_dialog.add(modal_content)
    modal_div.add(modal_dialog)
    
    return modal_div


def accordion(id, items, **kwargs):
    """Create an accordion component."""
    accordion_div = Div(class_="accordion", id=id, **kwargs)
    
    for i, item in enumerate(items):
        card = Div(class_="card")
        
        # Card header
        card_header = Div(class_="card-header", id=f"heading{i}")
        button = Button(
            item["title"],
            class_="btn btn-link",
            type="button",
            data={"toggle": "collapse", "target": f"#collapse{i}"},
            aria={"expanded": "false", "controls": f"collapse{i}"}
        )
        card_header.add(button)
        
        # Card body
        collapse_div = Div(
            class_="collapse" + (" show" if item.get("show", False) else ""),
            id=f"collapse{i}",
            aria={"labelledby": f"heading{i}"},
            data={"parent": f"#{id}"}
        )
        card_body = Div(class_="card-body")
        
        if isinstance(item["content"], str):
            card_body.add(P(item["content"]))
        else:
            card_body.add(item["content"])
        
        collapse_div.add(card_body)
        card.add(card_header, collapse_div)
        accordion_div.add(card)
    
    return accordion_div


def carousel(id, items, controls=True, indicators=True, **kwargs):
    """Create a carousel/slider component."""
    carousel_div = Div(
        class_="carousel slide",
        id=id,
        data={"ride": "carousel"},
        **kwargs
    )
    
    # Indicators
    if indicators:
        indicators_ol = Ol(class_="carousel-indicators")
        for i in range(len(items)):
            indicator = Li(
                data={"target": f"#{id}", "slide-to": str(i)},
                class_="active" if i == 0 else ""
            )
            indicators_ol.add(indicator)
        carousel_div.add(indicators_ol)
    
    # Carousel inner
    inner = Div(class_="carousel-inner")
    
    for i, item in enumerate(items):
        carousel_item = Div(class_="carousel-item" + (" active" if i == 0 else ""))
        
        if isinstance(item, dict):
            if "image" in item:
                carousel_item.add(Img(src=item["image"], class_="d-block w-100"))
            
            if "caption" in item:
                caption = Div(class_="carousel-caption d-none d-md-block")
                if "title" in item["caption"]:
                    caption.add(H5(item["caption"]["title"]))
                if "text" in item["caption"]:
                    caption.add(P(item["caption"]["text"]))
                carousel_item.add(caption)
        else:
            carousel_item.add(item)
        
        inner.add(carousel_item)
    
    carousel_div.add(inner)
    
    # Controls
    if controls:
        prev_control = A(
            Span(class_="carousel-control-prev-icon", aria={"hidden": "true"}),
            Span("Previous", class_="sr-only"),
            class_="carousel-control-prev",
            href=f"#{id}",
            role="button",
            data={"slide": "prev"}
        )
        
        next_control = A(
            Span(class_="carousel-control-next-icon", aria={"hidden": "true"}),
            Span("Next", class_="sr-only"),
            class_="carousel-control-next",
            href=f"#{id}",
            role="button",
            data={"slide": "next"}
        )
        
        carousel_div.add(prev_control, next_control)
    
    return carousel_div


def tooltip(target_element, tooltip_text, placement="top", **kwargs):
    """Add tooltip functionality to an element."""
    target_element.data = target_element.data or {}
    target_element.data.update({
        "toggle": "tooltip",
        "placement": placement
    })
    target_element.title = tooltip_text
    
    return target_element


def popover(target_element, title, content, placement="top", trigger="click", **kwargs):
    """Add popover functionality to an element."""
    target_element.data = target_element.data or {}
    target_element.data.update({
        "toggle": "popover",
        "placement": placement,
        "trigger": trigger
    })
    target_element.title = title
    target_element.data["content"] = content
    
    return target_element


def offcanvas(id, title, body, placement="start", **kwargs):
    """Create an offcanvas sidebar."""
    offcanvas_div = Div(
        class_=f"offcanvas offcanvas-{placement}",
        tabindex="-1",
        id=id,
        aria={"labelledby": f"{id}Label"},
        **kwargs
    )
    
    # Offcanvas header
    header = Div(class_="offcanvas-header")
    header_title = H5(title, class_="offcanvas-title", id=f"{id}Label")
    close_button = Button(
        type="button",
        class_="btn-close text-reset",
        data={"bs-dismiss": "offcanvas"},
        aria={"label": "Close"}
    )
    header.add(header_title, close_button)
    
    # Offcanvas body
    body_div = Div(class_="offcanvas-body")
    if isinstance(body, str):
        body_div.add(P(body))
    else:
        body_div.add(body)
    
    offcanvas_div.add(header, body_div)
    return offcanvas_div


def toast(id, title, message, timestamp=None, **kwargs):
    """Create a toast notification."""
    toast_div = Div(
        class_="toast",
        id=id,
        role="alert",
        aria={"live": "assertive", "atomic": "true"},
        **kwargs
    )
    
    # Toast header
    toast_header = Div(class_="toast-header")
    toast_header.add(Strong(title, class_="me-auto"))
    
    if timestamp:
        toast_header.add(Small(timestamp, class_="text-muted"))
    
    close_button = Button(
        type="button",
        class_="btn-close",
        data={"bs-dismiss": "toast"},
        aria={"label": "Close"}
    )
    toast_header.add(close_button)
    
    # Toast body
    toast_body = Div(message, class_="toast-body")
    
    toast_div.add(toast_header, toast_body)
    return toast_div


def collapse(id, content, trigger_text="Toggle", **kwargs):
    """Create a collapsible content area."""
    # Trigger button
    trigger = Button(
        trigger_text,
        class_="btn btn-primary",
        type="button",
        data={"bs-toggle": "collapse", "bs-target": f"#{id}"},
        aria={"expanded": "false", "controls": id}
    )
    
    # Collapsible content
    collapse_div = Div(
        class_="collapse",
        id=id,
        **kwargs
    )
    
    content_div = Div(class_="card card-body")
    if isinstance(content, str):
        content_div.add(P(content))
    else:
        content_div.add(content)
    
    collapse_div.add(content_div)
    
    return Div().add(trigger, collapse_div)


def breadcrumb_advanced(items, separator="/"):
    """Create an advanced breadcrumb with custom separator."""
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
                link = A(item["text"], href=item["href"])
                if "icon" in item:
                    link.add(icon(item["icon"]), " ", item["text"])
                li.add(link)
            else:
                li.add(Span(item["text"]))
        
        ol.add(li)
    
    nav.add(ol)
    return nav


def timeline(events, **kwargs):
    """Create a timeline component."""
    timeline_div = Div(class_="timeline", **kwargs)
    
    for event in events:
        timeline_item = Div(class_="timeline-item")
        
        # Timeline marker
        marker = Div(class_="timeline-marker")
        if "icon" in event:
            marker.add(icon(event["icon"]))
        timeline_item.add(marker)
        
        # Timeline content
        content = Div(class_="timeline-content")
        
        if "title" in event:
            content.add(H6(event["title"], class_="timeline-title"))
        
        if "date" in event:
            content.add(Small(event["date"], class_="timeline-date text-muted"))
        
        if "description" in event:
            content.add(P(event["description"], class_="timeline-description"))
        
        timeline_item.add(content)
        timeline_div.add(timeline_item)
    
    return timeline_div


def spinner(type="border", size=None, color="primary", **kwargs):
    """Create a loading spinner."""
    classes = [f"spinner-{type}"]
    
    if size:
        classes.append(f"spinner-{type}-{size}")
    
    if color:
        classes.append(f"text-{color}")
    
    if "class_" in kwargs:
        kwargs["class_"] = f"{' '.join(classes)} {kwargs['class_']}"
    else:
        kwargs["class_"] = " ".join(classes)
    
    kwargs["role"] = "status"
    kwargs["aria"] = {"hidden": "true"}
    
    spinner_div = Div(**kwargs)
    
    if type == "border":
        spinner_div.add(Span("Loading...", class_="sr-only"))
    
    return spinner_div