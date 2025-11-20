#!/usr/bin/env python3
from py_html.environment import init_environment, build_page, build_multiple_pages, Page

if __name__ == "__main__":
    print("Setting up environment...")
    
    # Setup the complete environment in output folder
    env_result = init_environment("output", "scripts")
    print(env_result)
    
    # Option 1: Build a single page
    print("Generating single page...")
    page_result = build_page("output/index.html", "scripts")
    print(page_result)
    
    # Option 2: Build multiple pages (uncomment to use)
    # print("Generating multiple pages...")
    # pages = [
    #     Page("output/home.html", "main.py", "Home Page"),
    #     Page("output/about.html", "about.py", "About Us"),
    #     Page("output/contact.html", "contact.py", "Contact")
    # ]
    # multi_result = build_multiple_pages(pages, "scripts")
    # print(multi_result)
    
    print("Build complete! Open output/index.html in a web browser.")
