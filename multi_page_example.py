#!/usr/bin/env python3
"""
Example showing how to build multiple pages with the Page class.
"""
from py_html.environment import init_environment, build_multiple_pages, Page

if __name__ == "__main__":
    print("Building multi-page application...")
    
    # Setup the complete environment in output folder
    print("Setting up environment...")
    env_result = init_environment("output", "scripts")
    print(env_result)
    
    # Define multiple pages
    pages = [
        Page("output/index.html", "main.py", "Home - PyHTML App"),
        Page("output/about.html", "about.py", "About Us - PyHTML App"),
        # You can add more pages here:
        # Page("output/contact.html", "contact.py", "Contact Us"),
        # Page("output/blog.html", "blog.py", "Blog")
    ]
    
    # Build all pages
    print("Generating multiple pages...")
    multi_result = build_multiple_pages(pages, "scripts")
    print(multi_result)
    
    print("\nBuild complete! You can now open:")
    print("  - output/index.html (Home page)")
    print("  - output/about.html (About page)")
    print("\nEach page runs its own Python script and shares the same environment.")