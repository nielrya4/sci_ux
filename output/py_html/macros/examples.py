"""Examples demonstrating how to use the PyHTML macro library."""

from .components import *
from .forms import *
from .layouts import *
from .ui import *


def example_login_page():
    """Example of a complete login page using macros."""
    return page_template(
        title="Login - MyApp",
        stylesheets=["https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css"],
        body_content=container(
            row(
                col(
                    card(
                        title="Login to Your Account",
                        content=login_form(
                            action="/auth/login",
                            method="post"
                        )
                    ),
                    md=6,
                    class_="mx-auto mt-5"
                )
            ),
            class_="mt-5"
        ),
        scripts=["https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/js/bootstrap.min.js"]
    )


def example_dashboard():
    """Example of a dashboard layout with sidebar navigation."""
    sidebar_items = [
        {"text": "Dashboard", "href": "/dashboard", "active": True, "icon": "tachometer-alt"},
        {"text": "Users", "href": "/users", "icon": "users"},
        {"text": "Reports", "href": "/reports", "icon": "chart-bar"},
        {"text": "Settings", "href": "/settings", "icon": "cog"}
    ]
    
    main_content = container(
        row(
            col(
                card(
                    title="Welcome Back!",
                    content="This is your dashboard overview.",
                    footer=badge("Active", "success")
                ),
                md=4
            ),
            col(
                card(
                    title="Recent Activity",
                    content=timeline([
                        {
                            "title": "User registered",
                            "date": "2 hours ago",
                            "description": "New user john@example.com registered",
                            "icon": "user-plus"
                        },
                        {
                            "title": "Report generated",
                            "date": "4 hours ago", 
                            "description": "Monthly sales report was generated",
                            "icon": "file-alt"
                        }
                    ])
                ),
                md=8
            )
        )
    )
    
    return dashboard_layout(sidebar_items, main_content, title="Admin Dashboard")


def example_landing_page():
    """Example of a modern landing page."""
    nav_items = [
        {"text": "Home", "href": "#", "active": True},
        {"text": "Features", "href": "#features"},
        {"text": "Pricing", "href": "#pricing"},
        {"text": "Contact", "href": "#contact"}
    ]
    
    main_content = Div().add(
        # Hero section
        hero_section(
            title="Welcome to PyHTML",
            subtitle="Build beautiful HTML with Python",
            background_image="/static/hero-bg.jpg",
            height="600px"
        ),
        
        # Features section
        Section(
            container(
                row(
                    col(
                        H2("Features", class_="text-center mb-5"),
                        md=12
                    )
                ),
                row(
                    col(
                        card(
                            title="Easy to Use",
                            content="Simple, Pythonic API for generating HTML",
                            image=icon("code", class_="fa-3x text-primary mb-3")
                        ),
                        md=4
                    ),
                    col(
                        card(
                            title="Flexible",
                            content="Create complex layouts with our macro system",
                            image=icon("puzzle-piece", class_="fa-3x text-success mb-3")
                        ),
                        md=4
                    ),
                    col(
                        card(
                            title="Modern",
                            content="Built-in support for Bootstrap and modern CSS",
                            image=icon("rocket", class_="fa-3x text-info mb-3")
                        ),
                        md=4
                    )
                )
            ),
            id="features",
            class_="py-5"
        ),
        
        # Contact form section
        Section(
            container(
                row(
                    col(
                        H2("Get in Touch", class_="text-center mb-5"),
                        contact_form(action="/contact"),
                        md=8,
                        class_="mx-auto"
                    )
                )
            ),
            id="contact",
            class_="py-5 bg-light"
        )
    )
    
    footer_links = [
        {
            "title": "Product",
            "links": [
                {"text": "Features", "href": "#features"},
                {"text": "Pricing", "href": "#pricing"},
                {"text": "Documentation", "href": "/docs"}
            ]
        },
        {
            "title": "Company",
            "links": [
                {"text": "About", "href": "/about"},
                {"text": "Contact", "href": "/contact"},
                {"text": "Blog", "href": "/blog"}
            ]
        }
    ]
    
    return full_page_layout(
        title="PyHTML - Build HTML with Python",
        navbar_config={
            "brand": {"text": "PyHTML", "href": "/"},
            "items": nav_items
        },
        main_content=main_content,
        footer_config={
            "links": footer_links,
            "copyright_text": "© 2024 PyHTML. All rights reserved."
        }
    )


def example_modal_demo():
    """Example showing various modal dialogs."""
    return page_template(
        title="Modal Examples",
        stylesheets=["https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css"],
        body_content=container([
            H1("Modal Examples", class_="text-center my-5"),
            
            row(
                col(
                    button_group([
                        {
                            "text": "Basic Modal",
                            "class_": "btn btn-primary",
                            "data": {"toggle": "modal", "target": "#basicModal"}
                        },
                        {
                            "text": "Large Modal", 
                            "class_": "btn btn-success",
                            "data": {"toggle": "modal", "target": "#largeModal"}
                        },
                        {
                            "text": "Confirmation Modal",
                            "class_": "btn btn-danger", 
                            "data": {"toggle": "modal", "target": "#confirmModal"}
                        }
                    ]),
                    class_="text-center"
                )
            ),
            
            # Modals
            modal(
                "basicModal",
                "Basic Modal",
                "This is a basic modal dialog with some content.",
                footer=[
                    Button("Close", class_="btn btn-secondary", data={"dismiss": "modal"}),
                    Button("Save changes", class_="btn btn-primary")
                ]
            ),
            
            modal(
                "largeModal", 
                "Large Modal",
                P("This is a large modal with more content space."),
                size="lg",
                footer=[
                    Button("Cancel", class_="btn btn-secondary", data={"dismiss": "modal"}),
                    Button("Confirm", class_="btn btn-success")
                ]
            ),
            
            modal(
                "confirmModal",
                "Confirm Action",
                "Are you sure you want to delete this item? This action cannot be undone.",
                footer=[
                    Button("Cancel", class_="btn btn-secondary", data={"dismiss": "modal"}),
                    Button("Delete", class_="btn btn-danger")
                ]
            )
        ]),
        scripts=[
            "https://code.jquery.com/jquery-3.5.1.min.js",
            "https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/js/bootstrap.min.js"
        ]
    )


def example_form_showcase():
    """Example showcasing various form components."""
    return page_template(
        title="Form Components Showcase",
        stylesheets=["https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css"],
        body_content=container([
            H1("Form Components", class_="text-center my-5"),
            
            row(
                col(
                    card(
                        title="User Registration Form",
                        content=Form([
                            text_field("first_name", "First Name", required=True),
                            text_field("last_name", "Last Name", required=True),
                            email_field("email", "Email Address", required=True),
                            password_field("password", "Password", required=True),
                            
                            select_field(
                                "country",
                                [
                                    {"value": "us", "text": "United States"},
                                    {"value": "uk", "text": "United Kingdom"}, 
                                    {"value": "ca", "text": "Canada"}
                                ],
                                label="Country",
                                required=True
                            ),
                            
                            radio_field(
                                "gender",
                                [
                                    {"value": "male", "text": "Male"},
                                    {"value": "female", "text": "Female"},
                                    {"value": "other", "text": "Other"}
                                ]
                            ),
                            
                            checkbox_field("newsletter", "Subscribe to newsletter"),
                            checkbox_field("terms", "I agree to the terms and conditions", required=True),
                            
                            textarea_field("bio", "Bio", placeholder="Tell us about yourself...", rows=4),
                            
                            form_actions(
                                submit_button("Register"),
                                reset_button("Clear Form"),
                                alignment="right"
                            )
                        ])
                    ),
                    md=8,
                    class_="mx-auto"
                )
            )
        ])
    )


def example_component_showcase():
    """Example showcasing various UI components."""
    return page_template(
        title="UI Components Showcase",
        stylesheets=["https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css"],
        body_content=container([
            H1("UI Components", class_="text-center my-5"),
            
            # Alerts
            row(
                col([
                    H3("Alerts"),
                    alert("This is a success alert!", "success"),
                    alert("This is a warning alert!", "warning"),
                    alert("This is a danger alert!", "danger", dismissible=True)
                ], md=6),
                col([
                    H3("Badges & Progress"),
                    P().add(
                        "Status: ", badge("Active", "success"), " ",
                        badge("Premium", "gold")
                    ),
                    progress_bar(75, label="75% Complete"),
                    Br(),
                    progress_bar(45, color="warning", label="45%")
                ], md=6)
            ),
            
            # Accordion
            row(
                col([
                    H3("Accordion"),
                    accordion("exampleAccordion", [
                        {
                            "title": "Section 1",
                            "content": "This is the content for the first accordion section.",
                            "show": True
                        },
                        {
                            "title": "Section 2", 
                            "content": "This is the content for the second accordion section."
                        },
                        {
                            "title": "Section 3",
                            "content": "This is the content for the third accordion section."
                        }
                    ])
                ], md=6),
                col([
                    H3("Tabs"),
                    tabs([
                        {
                            "id": "home",
                            "title": "Home",
                            "content": P("Home tab content goes here.")
                        },
                        {
                            "id": "profile",
                            "title": "Profile", 
                            "content": P("Profile tab content goes here.")
                        },
                        {
                            "id": "contact",
                            "title": "Contact",
                            "content": P("Contact tab content goes here.")
                        }
                    ])
                ], md=6)
            )
        ]),
        scripts=[
            "https://code.jquery.com/jquery-3.5.1.min.js",
            "https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/js/bootstrap.min.js"
        ]
    )