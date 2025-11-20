"""Examples demonstrating custom PyHTML macros built without Bootstrap dependencies."""

from .custom_layouts import *
from .custom_forms import *
from .custom_ui import *


def custom_login_page():
    """Example of a complete login page using custom macros."""
    return page_template(
        title="Login - PyHTML Custom",
        body_content=container([
            row([
                col([
                    card(
                        title="Sign In",
                        content=Form([
                            text_field("username", "Username", placeholder="Enter your username", required=True),
                            password_field("password", "Password", placeholder="Enter your password", required=True),
                            checkbox_field("remember", "Remember me"),
                            form_actions(
                                submit_button("Sign In", "primary"),
                                alignment="center"
                            )
                        ], action="/auth/login", method="post")
                    )
                ], size=6, style="margin: 0 auto; margin-top: 3rem;")
            ])
        ])
    )


def custom_dashboard():
    """Example of a dashboard using custom macros."""
    sidebar_items = [
        {"text": "Dashboard", "href": "#dashboard", "active": True},
        {"text": "Users", "href": "#users"},
        {"text": "Settings", "href": "#settings"},
        {"text": "Reports", "href": "#reports"},
        {"text": "Logout", "href": "#logout"}
    ]
    
    main_content = container([
        H2("Welcome to Dashboard", style="margin-bottom: 2rem;"),
        
        # Stats row
        row([
            col([
                card(
                    title="Total Users",
                    content=H3("1,234", style="color: #007bff; margin: 0;")
                )
            ], size=3),
            col([
                card(
                    title="Active Sessions", 
                    content=H3("89", style="color: #28a745; margin: 0;")
                )
            ], size=3),
            col([
                card(
                    title="Revenue",
                    content=H3("$12,345", style="color: #ffc107; margin: 0;")
                )
            ], size=3),
            col([
                card(
                    title="Growth",
                    content=H3("+15%", style="color: #17a2b8; margin: 0;")
                )
            ], size=3)
        ]),
        
        # Timeline
        row([
            col([
                card(
                    title="Recent Activity",
                    content=timeline([
                        {
                            "title": "User Registration",
                            "date": "2024-01-15",
                            "description": "New user john@example.com registered"
                        },
                        {
                            "title": "System Update",
                            "date": "2024-01-14", 
                            "description": "System updated to version 2.1.0"
                        },
                        {
                            "title": "Database Backup",
                            "date": "2024-01-13",
                            "description": "Scheduled backup completed successfully"
                        }
                    ])
                )
            ])
        ])
    ])
    
    return page_template(
        title="Dashboard - PyHTML Custom",
        body_content=dashboard_layout(sidebar_items, main_content, title="Admin Dashboard")
    )


def custom_landing_page():
    """Example of a landing page using custom macros."""
    nav_items = [
        {"text": "Features", "href": "#features"},
        {"text": "Pricing", "href": "#pricing"},
        {"text": "Contact", "href": "#contact"}
    ]
    
    return page_template(
        title="PyHTML Custom Framework",
        body_content=[
            navbar("PyHTML", nav_items),
            
            # Hero section
            hero_section(
                "Build Beautiful Web Pages",
                "Create stunning HTML with our custom Python framework - no Bootstrap required!",
                background_color="linear-gradient(135deg, #667eea 0%, #764ba2 100%)",
                text_color="#fff"
            ),
            
            # Features section
            container([
                row([
                    col([
                        H2("Features", style="text-align: center; margin: 3rem 0;")
                    ])
                ]),
                row([
                    col([
                        card(
                            title="🎨 Custom Styled",
                            content="Beautiful components built from scratch with custom CSS - no external dependencies."
                        )
                    ], size=4),
                    col([
                        card(
                            title="🚀 Fast & Lightweight", 
                            content="Optimized for performance with minimal CSS and clean HTML output."
                        )
                    ], size=4),
                    col([
                        card(
                            title="🎯 Pythonic API",
                            content="Intuitive Python interface that feels natural for developers."
                        )
                    ], size=4)
                ])
            ], style="padding: 2rem 0;"),
            
            # Contact section
            container([
                row([
                    col([
                        card(
                            title="Get In Touch",
                            content=Form([
                                text_field("name", "Your Name", required=True),
                                email_field("email", "Email Address", required=True), 
                                textarea_field("message", "Message", rows=4, required=True),
                                form_actions(
                                    submit_button("Send Message", "primary"),
                                    alignment="center"
                                )
                            ])
                        )
                    ], size=8, style="margin: 0 auto;")
                ])
            ], style="padding: 3rem 0; background-color: #f8f9fa;"),
            
            footer(
                copyright_text="© 2024 PyHTML Custom. Built with ❤️ in Python."
            )
        ]
    )


def custom_modal_demo():
    """Example showing various modal dialogs using custom macros."""
    return page_template(
        title="Modal Examples - PyHTML Custom",
        body_content=container([
            H1("Custom Modal Examples", style="text-align: center; margin: 2rem 0;"),
            
            row([
                col([
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
                            "text": "Confirmation",
                            "class_": "btn btn-danger",
                            "data": {"toggle": "modal", "target": "#confirmModal"}
                        }
                    ], style="text-align: center;")
                ])
            ]),
            
            # Modals
            modal(
                "basicModal",
                "Basic Modal",
                "This is a basic modal dialog with some content using our custom framework.",
                footer=[
                    button("Close", "secondary", onclick="document.getElementById('basicModal').style.display='none'"),
                    button("Save changes", "primary")
                ]
            ),
            
            modal(
                "largeModal",
                "Large Modal",
                P("This is a large modal with more content space. Our custom modal system is flexible and responsive."),
                footer=[
                    button("Cancel", "secondary", onclick="document.getElementById('largeModal').style.display='none'"),
                    button("Confirm", "success")
                ],
                size="large"
            ),
            
            modal(
                "confirmModal", 
                "Confirm Action",
                "Are you sure you want to delete this item? This action cannot be undone.",
                footer=[
                    button("Cancel", "secondary", onclick="document.getElementById('confirmModal').style.display='none'"),
                    button("Delete", "danger")
                ]
            )
        ])
    )


def custom_form_showcase():
    """Example showcasing various form components using custom macros.""" 
    return page_template(
        title="Form Components - PyHTML Custom",
        body_content=container([
            H1("Custom Form Components", style="text-align: center; margin: 2rem 0;"),
            
            row([
                col([
                    card(
                        title="User Registration Form",
                        content=Form([
                            text_field("first_name", "First Name", required=True),
                            text_field("last_name", "Last Name", required=True),
                            email_field("email", "Email Address", required=True),
                            password_field("password", "Password", required=True),
                            select_field("country", [
                                "United States",
                                "Canada", 
                                "United Kingdom",
                                "Australia"
                            ], "Country"),
                            checkbox_field("newsletter", "Subscribe to newsletter"),
                            radio_field("account_type", [
                                {"text": "Personal", "value": "personal", "checked": True},
                                {"text": "Business", "value": "business"}
                            ], "Account Type"),
                            textarea_field("bio", "Bio", placeholder="Tell us about yourself..."),
                            range_field("experience", 0, 10, 5, "Years of Experience"),
                            file_field("avatar", "Profile Picture", accept="image/*"),
                            form_actions(
                                submit_button("Register"),
                                reset_button("Clear Form"),
                                alignment="right"
                            )
                        ])
                    )
                ], size=8, style="margin: 0 auto;")
            ])
        ])
    )


def custom_component_showcase():
    """Example showcasing various UI components using custom macros."""
    return page_template(
        title="UI Components - PyHTML Custom", 
        body_content=container([
            H1("Custom UI Components", style="text-align: center; margin: 2rem 0;"),
            
            # Alerts
            row([
                col([
                    H3("Alerts"),
                    alert("This is a success alert!", "success"),
                    alert("This is a warning alert!", "warning"), 
                    alert("This is a danger alert!", "danger", dismissible=True)
                ], size=6),
                col([
                    H3("Badges & Progress"),
                    P([
                        "Status: ", badge("Active", "success"), " ",
                        badge("Premium", "warning")
                    ]),
                    progress_bar(75, label="75% Complete"),
                    progress_bar(45, color="warning", label="45%")
                ], size=6)
            ]),
            
            # Accordion
            row([
                col([
                    H3("Accordion"),
                    accordion("customAccordion", [
                        {
                            "title": "Section 1",
                            "content": "This is the content for the first accordion section using our custom framework.",
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
                ], size=6),
                col([
                    H3("Tabs"),
                    tabs([
                        {
                            "id": "home",
                            "title": "Home",
                            "content": P("Home tab content goes here with custom styling.")
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
                ], size=6)
            ]),
            
            # Toasts
            row([
                col([
                    H3("Notifications"),
                    toast("This is an info notification", "info", "Information"),
                    toast("Operation completed successfully!", "success", "Success"),
                    toast("Please check your input", "warning", "Warning")
                ])
            ])
        ])
    )