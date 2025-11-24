#!/usr/bin/env python3
import os
from py_html.environment import init_environment, build_page

def detect_script_directories(scripts_folder="scripts"):
    """Detect all directories in the scripts folder for dynamic module creation."""
    directories = []
    
    if not os.path.exists(scripts_folder):
        return directories
    
    for root, dirs, files in os.walk(scripts_folder):
        # Get relative path from scripts folder
        rel_path = os.path.relpath(root, ".")
        
        # Skip the root scripts folder itself
        if rel_path != scripts_folder:
            # Convert to forward slashes for consistency and prepend with /
            pyodide_path = "/" + rel_path.replace("\\", "/")
            directories.append(pyodide_path)
    
    return sorted(directories)

if __name__ == "__main__":
    print("Setting up environment...")
    
    # Detect directory structure
    script_dirs = detect_script_directories("scripts")
    print(f"Detected script directories: {script_dirs}")
    
    # Setup the complete environment in output folder
    env_result = init_environment("output", "scripts")
    print(env_result)
    
    # Build single page application with navigation
    print("Generating single page application...")
    page_result = build_page("output/index.html", "scripts", script_dirs)
    print(page_result)
    
    print("Build complete! Open output/index.html in a web browser.")
    print("SPA Navigation: Use the navbar to navigate between pages without reloading!")
