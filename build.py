#!/usr/bin/env python3
from py_html.environment import init_environment, build_page

if __name__ == "__main__":
    print("Setting up environment...")
    
    # Setup the complete environment in output folder
    env_result = init_environment("output", "scripts")
    print(env_result)
    
    # Build single page application with navigation
    print("Generating single page application...")
    page_result = build_page("output/index.html", "scripts")
    print(page_result)
    
    print("Build complete! Open output/index.html in a web browser.")
    print("SPA Navigation: Use the navbar to navigate between pages without reloading!")
