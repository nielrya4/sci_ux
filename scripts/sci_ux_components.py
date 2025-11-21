from py_html.macros.layouts import *
from py_html.macros.forms import *
from py_html.macros.ui import *
from py_html.css import CSS, CSSBuilder
from typing import List, Optional

class NavItem:
    def __init__(self, label: str, url: str, children: Optional[List['NavItem']]=None):
        self.label = label
        self.url = url
        self.children = children



def navbar(items: List[NavItem]):
    navbar_div = Div(class_="sci_ux_navbar")
    for item in items:
        if item.children is None:
            # Use data-page attribute for SPA navigation instead of href
            page_name = item.url.lstrip('/') if item.url != '#' else ''
            link = A(href="#", 
                    class_="sci_ux_navbar_link spa-link", 
                    content=item.label,
                    data={'page': page_name})
            navbar_div.add(link)
        else:
            dropdown_content = Div(class_="sci_ux_dropdown_content")
            for child in item.children:
                child_page_name = child.url.lstrip('/') if child.url != '#' else ''
                child_link = A(href="#", 
                              class_="sci_ux_navbar_link spa-link", 
                              content=child.label,
                              data={'page': child_page_name})
                dropdown_content.add(child_link)
            
            navbar_div.add(Div(class_="sci_ux_dropdown").add(
                Button(class_="sci_ux_dropbtn", content=item.label + " ▼"),
                dropdown_content
            ))
    return navbar_div


def get_navbar_css():
    """Generate CSS for the navbar component using the CSS library."""
    css = CSSBuilder()
    
    # Main navbar container
    css.add(
        CSS.class_("sci_ux_navbar",
            overflow="hidden",
            background_color="#333"
        )
    )
    
    # Navbar links
    css.add(
        CSS.class_("sci_ux_navbar_link",
            float="left",
            display="block",
            color="white",
            text_align="center",
            padding="14px 20px",
            text_decoration="none"
        ),
        
        CSS.selector(".sci_ux_navbar_link:hover",
            background_color="#ddd",
            color="black"
        )
    )
    
    # Dropdown container
    css.add(
        CSS.class_("sci_ux_dropdown",
            float="left",
            overflow="hidden"
        )
    )
    
    # Dropdown button
    css.add(
        CSS.class_("sci_ux_dropbtn",
            font_size="16px",
            border="none",
            outline="none",
            color="white",
            padding="14px 16px",
            background_color="inherit",
            font_family="inherit",
            margin="0",
            cursor="pointer"
        ),
        
        CSS.selector(".sci_ux_dropdown:hover .sci_ux_dropbtn",
            background_color="#ddd",
            color="black"
        )
    )
    
    # Dropdown content
    css.add(
        CSS.class_("sci_ux_dropdown_content",
            display="none",
            position="absolute",
            background_color="#f9f9f9",
            min_width="160px",
            box_shadow="0px 8px 16px 0px rgba(0,0,0,0.2)",
            z_index="1"
        ),
        
        CSS.selector(".sci_ux_dropdown_content a",
            float="none",
            color="black",
            padding="12px 16px",
            text_decoration="none",
            display="block",
            text_align="left"
        ),
        
        CSS.selector(".sci_ux_dropdown_content a:hover",
            background_color="#ddd"
        ),
        
        CSS.selector(".sci_ux_dropdown:hover .sci_ux_dropdown_content",
            display="block"
        )
    )
    
    return css