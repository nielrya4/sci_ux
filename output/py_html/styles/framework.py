"""Custom CSS framework for PyHTML macros using our CSS library."""

from ..css import CSSBuilder, CSS


def create_custom_framework():
    """Create a custom CSS framework using our CSS library."""
    
    css = CSSBuilder()
    
    # Reset and base styles
    css.add(
        CSS.selector("*", 
            margin="0",
            padding="0",
            box_sizing="border-box"
        ),
        
        CSS.element("body",
            font_family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif",
            line_height="1.6",
            color="#333",
            background_color="#fff"
        )
    )
    
    # Layout System - Grid
    css.add(
        CSS.class_("container",
            max_width="1200px",
            margin="0 auto",
            padding="0 15px",
            width="100%"
        ),
        
        CSS.class_("container-fluid",
            width="100%",
            padding="0 15px"
        ),
        
        CSS.class_("row",
            display="flex",
            flex_wrap="wrap",
            margin="0 -15px"
        ),
        
        CSS.class_("col",
            flex="1",
            padding="0 15px"
        )
    )
    
    # Column system - generate all 12 columns
    for i in range(1, 13):
        width = (i / 12) * 100
        css.add(
            CSS.class_(f"col-{i}",
                flex=f"0 0 {width:.6f}%",
                max_width=f"{width:.6f}%",
                padding="0 15px"
            )
        )
    
    # Button System
    css.add(
        CSS.class_("btn",
            display="inline-block",
            padding="0.5rem 1rem",
            margin_bottom="0",
            font_size="1rem",
            font_weight="400",
            line_height="1.5",
            text_align="center",
            text_decoration="none",
            vertical_align="middle",
            cursor="pointer",
            border="1px solid transparent",
            border_radius="0.375rem",
            transition="all 0.15s ease-in-out",
            background_color="transparent"
        )
    )
    
    # Button variants
    button_variants = {
        "primary": {"bg": "#007bff", "border": "#007bff", "color": "#fff", "hover_bg": "#0056b3"},
        "secondary": {"bg": "#6c757d", "border": "#6c757d", "color": "#fff", "hover_bg": "#545b62"},
        "success": {"bg": "#28a745", "border": "#28a745", "color": "#fff", "hover_bg": "#1e7e34"},
        "danger": {"bg": "#dc3545", "border": "#dc3545", "color": "#fff", "hover_bg": "#c82333"},
        "warning": {"bg": "#ffc107", "border": "#ffc107", "color": "#212529", "hover_bg": "#e0a800"},
        "info": {"bg": "#17a2b8", "border": "#17a2b8", "color": "#fff", "hover_bg": "#138496"}
    }
    
    for variant, styles in button_variants.items():
        css.add(
            CSS.class_(f"btn-{variant}",
                background_color=styles["bg"],
                border_color=styles["border"],
                color=styles["color"]
            ),
            
            CSS.selector(f".btn-{variant}:hover",
                background_color=styles["hover_bg"],
                border_color=styles["hover_bg"],
                transform="translateY(-1px)",
                box_shadow="0 4px 8px rgba(0,0,0,0.1)"
            )
        )
    
    # Form Controls
    css.add(
        CSS.class_("form-control",
            display="block",
            width="100%",
            padding="0.5rem 0.75rem",
            font_size="1rem",
            line_height="1.5",
            color="#495057",
            background_color="#fff",
            border="1px solid #ced4da",
            border_radius="0.375rem",
            transition="border-color 0.15s ease-in-out, box-shadow 0.15s ease-in-out"
        ),
        
        CSS.selector(".form-control:focus",
            border_color="#80bdff",
            outline="0",
            box_shadow="0 0 0 0.2rem rgba(0, 123, 255, 0.25)"
        ),
        
        CSS.class_("form-group",
            margin_bottom="1rem"
        ),
        
        CSS.class_("form-label",
            display="block",
            margin_bottom="0.5rem",
            font_weight="500",
            color="#212529"
        )
    )
    
    # Alert System
    css.add(
        CSS.class_("alert",
            padding="0.75rem 1rem",
            margin_bottom="1rem",
            border="1px solid transparent",
            border_radius="0.375rem",
            position="relative"
        )
    )
    
    alert_variants = {
        "success": {"bg": "#d4edda", "border": "#c3e6cb", "color": "#155724"},
        "info": {"bg": "#d1ecf1", "border": "#bee5eb", "color": "#0c5460"},
        "warning": {"bg": "#fff3cd", "border": "#ffeaa7", "color": "#856404"},
        "danger": {"bg": "#f8d7da", "border": "#f5c6cb", "color": "#721c24"}
    }
    
    for variant, styles in alert_variants.items():
        css.add(
            CSS.class_(f"alert-{variant}",
                background_color=styles["bg"],
                border_color=styles["border"],
                color=styles["color"]
            )
        )
    
    # Card System
    css.add(
        CSS.class_("card",
            background_color="#fff",
            border="1px solid rgba(0,0,0,0.125)",
            border_radius="0.375rem",
            box_shadow="0 0.125rem 0.25rem rgba(0,0,0,0.075)",
            margin_bottom="1rem"
        ),
        
        CSS.class_("card-header",
            padding="0.75rem 1rem",
            background_color="rgba(0,0,0,0.03)",
            border_bottom="1px solid rgba(0,0,0,0.125)",
            border_radius="0.375rem 0.375rem 0 0"
        ),
        
        CSS.class_("card-body",
            padding="1rem"
        ),
        
        CSS.class_("card-title",
            margin_bottom="0.5rem",
            font_size="1.25rem",
            font_weight="500"
        ),
        
        CSS.class_("card-footer",
            padding="0.75rem 1rem",
            background_color="rgba(0,0,0,0.03)",
            border_top="1px solid rgba(0,0,0,0.125)",
            border_radius="0 0 0.375rem 0.375rem"
        )
    )
    
    # Modal System
    css.add(
        CSS.class_("modal",
            position="fixed",
            top="0",
            left="0",
            z_index="1050",
            width="100%",
            height="100%",
            background_color="rgba(0,0,0,0.5)",
            display="none"
        ),
        
        CSS.selector(".modal.show",
            display="flex",
            align_items="center",
            justify_content="center"
        ),
        
        CSS.class_("modal-dialog",
            max_width="500px",
            width="90%",
            margin="auto"
        ),
        
        CSS.class_("modal-content",
            background_color="#fff",
            border_radius="0.375rem",
            box_shadow="0 0.5rem 1rem rgba(0,0,0,0.15)"
        ),
        
        CSS.class_("modal-header",
            display="flex",
            align_items="center",
            justify_content="space-between",
            padding="1rem",
            border_bottom="1px solid #dee2e6",
            border_radius="0.375rem 0.375rem 0 0"
        ),
        
        CSS.class_("modal-body",
            padding="1rem"
        ),
        
        CSS.class_("modal-footer",
            display="flex",
            align_items="center",
            justify_content="flex-end",
            padding="1rem",
            border_top="1px solid #dee2e6",
            gap="0.5rem"
        )
    )
    
    # Badge System
    css.add(
        CSS.class_("badge",
            display="inline-block",
            padding="0.25em 0.4em",
            font_size="0.75em",
            font_weight="700",
            line_height="1",
            text_align="center",
            white_space="nowrap",
            vertical_align="baseline",
            border_radius="0.375rem"
        )
    )
    
    badge_variants = {
        "primary": {"bg": "#007bff", "color": "#fff"},
        "secondary": {"bg": "#6c757d", "color": "#fff"},
        "success": {"bg": "#28a745", "color": "#fff"},
        "danger": {"bg": "#dc3545", "color": "#fff"},
        "warning": {"bg": "#ffc107", "color": "#212529"},
        "info": {"bg": "#17a2b8", "color": "#fff"},
        "gold": {"bg": "#ffd700", "color": "#212529"}
    }
    
    for variant, styles in badge_variants.items():
        css.add(
            CSS.class_(f"badge-{variant}",
                background_color=styles["bg"],
                color=styles["color"]
            )
        )
    
    # Progress Bar System
    css.add(
        CSS.class_("progress",
            display="flex",
            height="1rem",
            background_color="#e9ecef",
            border_radius="0.375rem",
            overflow="hidden"
        ),
        
        CSS.class_("progress-bar",
            display="flex",
            flex_direction="column",
            justify_content="center",
            color="#fff",
            text_align="center",
            white_space="nowrap",
            background_color="#007bff",
            transition="width 0.6s ease"
        )
    )
    
    # Utility Classes
    css.add(
        CSS.class_("text-center", text_align="center"),
        CSS.class_("text-left", text_align="left"),
        CSS.class_("text-right", text_align="right")
    )
    
    # Spacing utilities
    for i in range(6):
        css.add(
            CSS.class_(f"m-{i}", margin=f"{i * 0.25}rem"),
            CSS.class_(f"p-{i}", padding=f"{i * 0.25}rem"),
            CSS.class_(f"mt-{i}", margin_top=f"{i * 0.25}rem"),
            CSS.class_(f"mb-{i}", margin_bottom=f"{i * 0.25}rem"),
            CSS.class_(f"pt-{i}", padding_top=f"{i * 0.25}rem"),
            CSS.class_(f"pb-{i}", padding_bottom=f"{i * 0.25}rem")
        )
    
    # Responsive breakpoints using media queries
    mobile = CSS.media("max-width: 768px")
    mobile.add(
        CSS.class_("container",
            padding="0 10px"
        ),
        CSS.selector(".col-1, .col-2, .col-3, .col-4, .col-5, .col-6, .col-7, .col-8, .col-9, .col-10, .col-11, .col-12",
            flex="0 0 100%",
            max_width="100%"
        )
    )
    css.add(mobile)
    
    tablet = CSS.media("min-width: 769px and max-width: 1024px")
    tablet.add(
        CSS.class_("container",
            max_width="750px"
        )
    )
    css.add(tablet)
    
    return css.to_css()