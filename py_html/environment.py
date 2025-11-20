def init_environment(output_folder: str, scripts_folder: str = "scripts") -> str:
    """Setup complete PyHTML environment by copying all necessary files to output folder."""
    import os
    import shutil
    from pathlib import Path
    
    output_path = Path(output_folder)
    
    # Create output directory
    output_path.mkdir(parents=True, exist_ok=True)
    print(f"Created output directory: {output_path}")
    
    # Copy pyodide folder if it exists
    if os.path.exists("pyodide"):
        pyodide_dest = output_path / "pyodide"
        if pyodide_dest.exists():
            shutil.rmtree(pyodide_dest)
        shutil.copytree("pyodide", pyodide_dest)
        print(f"Copied pyodide folder to {pyodide_dest}")
    
    # Copy py_html folder
    if os.path.exists("py_html"):
        py_html_dest = output_path / "py_html"
        if py_html_dest.exists():
            shutil.rmtree(py_html_dest)
        shutil.copytree("py_html", py_html_dest)
        print(f"Copied py_html folder to {py_html_dest}")
    
    # Copy scripts folder
    if os.path.exists(scripts_folder):
        scripts_dest = output_path / "scripts"
        if scripts_dest.exists():
            shutil.rmtree(scripts_dest)
        shutil.copytree(scripts_folder, scripts_dest)
        print(f"Copied {scripts_folder} folder to {scripts_dest}")
    
    return f"Environment setup complete in {output_path}"

def build_page(filename: str, scripts_folder: str = "scripts") -> str:
    """Generate HTML file with PyHTML environment setup."""
    import os
    import glob
    from pathlib import Path
    
    # Get all Python files from scripts folder
    python_files = []
    if os.path.exists(scripts_folder):
        for root, dirs, files in os.walk(scripts_folder):
            for file in files:
                if file.endswith(".py"):
                    rel_path = os.path.relpath(os.path.join(root, file), ".")
                    python_files.append(rel_path)
    else:
        # Fall back to current directory if scripts folder doesn't exist
        python_files = glob.glob("*.py")
    
    # Get all Python files from py_html module
    py_html_files = []
    if os.path.exists("py_html"):
        for root, dirs, files in os.walk("py_html"):
            for file in files:
                if file.endswith(".py"):
                    rel_path = os.path.relpath(os.path.join(root, file), ".")
                    py_html_files.append(rel_path)
    
    # Generate the HTML template
    html_content = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Python UX Application</title>
    <script src="pyodide/pyodide.js"></script>
    <style>
        body {{
            font-family: Arial, sans-serif;
            margin: 0;
            padding: 20px;
            background-color: #f5f5f5;
        }}
        #loading {{
            text-align: center;
            padding: 50px;
        }}
        #content {{
            max-width: 1200px;
            margin: 0 auto;
            display: none;
        }}
        .spinner {{
            border: 4px solid #f3f3f3;
            border-top: 4px solid #3498db;
            border-radius: 50%;
            width: 40px;
            height: 40px;
            animation: spin 2s linear infinite;
            margin: 0 auto;
        }}
        @keyframes spin {{
            0% {{ transform: rotate(0deg); }}
            100% {{ transform: rotate(360deg); }}
        }}
    </style>
</head>
<body>
    <div id="loading">
        <div class="spinner"></div>
        <p>Loading Python environment...</p>
    </div>
    
    <div id="content"></div>

    <script>
        async function initializeApp() {{
            try {{
                // Initialize Pyodide with local installation
                const pyodide = await loadPyodide({{
                    indexURL: "./pyodide/"
                }});
                
                // Install required packages
                await pyodide.loadPackage(['micropip']);
                
                // Load and mount py_html module files
                const pyHtmlFiles = {py_html_files};
                
                // Create py_html module structure in Pyodide
                pyodide.FS.mkdir('/py_html');
                pyodide.FS.mkdir('/py_html/macros');
                pyodide.FS.mkdir('/py_html/styles');
                
                // Create scripts module structure in Pyodide
                pyodide.FS.mkdir('/scripts');
                
                // Load each py_html file
                for (const file of pyHtmlFiles) {{
                    try {{
                        const response = await fetch(file);
                        const content = await response.text();
                        pyodide.FS.writeFile(`/${{file}}`, content);
                        console.log(`Loaded ${{file}}`);
                    }} catch (error) {{
                        console.warn(`Could not load ${{file}}:`, error);
                    }}
                }}
                
                // Load Python files from scripts folder
                const pythonFiles = {python_files};
                for (const file of pythonFiles) {{
                    try {{
                        const response = await fetch(file);
                        const content = await response.text();
                        pyodide.FS.writeFile(`/${{file}}`, content);
                        console.log(`Loaded ${{file}}`);
                    }} catch (error) {{
                        console.warn(`Could not load ${{file}}:`, error);
                    }}
                }}
                
                // Add py_html and scripts to Python path
                await pyodide.runPython(`
                    import sys
                    sys.path.insert(0, '/py_html')
                    sys.path.insert(0, '/scripts')
                    sys.path.insert(0, '/')
                    print("Python path updated with py_html and scripts")
                `);
                
                // Look for and execute main.py from scripts folder or current directory
                let mainScript = null;
                if (pythonFiles.includes('{scripts_folder}/main.py')) {{
                    mainScript = '{scripts_folder}/main.py';
                }} else if (pythonFiles.includes('main.py')) {{
                    mainScript = 'main.py';
                }}
                
                if (mainScript) {{
                    const response = await fetch(mainScript);
                    const mainCode = await response.text();
                    await pyodide.runPython(mainCode);
                    console.log(`Executed ${{mainScript}}`);
                }}
                
                // Hide loading and show content
                document.getElementById('loading').style.display = 'none';
                document.getElementById('content').style.display = 'block';
                
            }} catch (error) {{
                console.error('Error loading Pyodide:', error);
                document.getElementById('loading').innerHTML = `
                    <p style="color: red;">Error loading application: ${{error.message}}</p>
                `;
            }}
        }}
        
        // Start loading when page is ready
        window.addEventListener('DOMContentLoaded', initializeApp);
    </script>
</body>
</html>'''
    
    # Create output directory if needed
    output_path = Path(filename).parent
    if output_path != Path('.'):
        output_path.mkdir(parents=True, exist_ok=True)
    
    # Write the HTML file
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    return f"Generated {filename}"

class Page:
    """Represents a single page to be built."""
    
    def __init__(self, filename: str, main_script: str, title: str = "Python UX Application"):
        """
        Initialize a Page.
        
        Args:
            filename: Output HTML filename (e.g., "output/index.html")
            main_script: Python script to execute for this page (e.g., "main.py")
            title: Page title for the HTML <title> tag
        """
        self.filename = filename
        self.main_script = main_script
        self.title = title

def build_multiple_pages(pages: list, scripts_folder: str = "scripts") -> str:
    """
    Build multiple pages with different entry points.
    
    Args:
        pages: List of Page objects
        scripts_folder: Folder containing Python scripts
    
    Example:
        pages = [
            Page("output/index.html", "main.py", "Home"),
            Page("output/about.html", "about.py", "About"),
            Page("output/contact.html", "contact.py", "Contact")
        ]
        build_multiple_pages(pages)
    """
    import os
    import glob
    from pathlib import Path
    
    # Get all Python files from scripts folder
    python_files = []
    if os.path.exists(scripts_folder):
        for root, dirs, files in os.walk(scripts_folder):
            for file in files:
                if file.endswith(".py"):
                    rel_path = os.path.relpath(os.path.join(root, file), ".")
                    python_files.append(rel_path)
    
    # Get all Python files from py_html module
    py_html_files = []
    if os.path.exists("py_html"):
        for root, dirs, files in os.walk("py_html"):
            for file in files:
                if file.endswith(".py"):
                    rel_path = os.path.relpath(os.path.join(root, file), ".")
                    py_html_files.append(rel_path)
    
    results = []
    
    for page in pages:
        # Generate the HTML template for this page
        html_content = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{page.title}</title>
    <script src="pyodide/pyodide.js"></script>
    <style>
        body {{
            font-family: Arial, sans-serif;
            margin: 0;
            padding: 20px;
            background-color: #f5f5f5;
        }}
        #loading {{
            text-align: center;
            padding: 50px;
        }}
        #content {{
            max-width: 1200px;
            margin: 0 auto;
            display: none;
        }}
        .spinner {{
            border: 4px solid #f3f3f3;
            border-top: 4px solid #3498db;
            border-radius: 50%;
            width: 40px;
            height: 40px;
            animation: spin 2s linear infinite;
            margin: 0 auto;
        }}
        @keyframes spin {{
            0% {{ transform: rotate(0deg); }}
            100% {{ transform: rotate(360deg); }}
        }}
    </style>
</head>
<body>
    <div id="loading">
        <div class="spinner"></div>
        <p>Loading Python environment...</p>
    </div>
    
    <div id="content"></div>

    <script>
        async function initializeApp() {{
            try {{
                // Initialize Pyodide with local installation
                const pyodide = await loadPyodide({{
                    indexURL: "./pyodide/"
                }});
                
                // Install required packages
                await pyodide.loadPackage(['micropip']);
                
                // Load and mount py_html module files
                const pyHtmlFiles = {py_html_files};
                
                // Create py_html module structure in Pyodide
                pyodide.FS.mkdir('/py_html');
                pyodide.FS.mkdir('/py_html/macros');
                pyodide.FS.mkdir('/py_html/styles');
                
                // Create scripts module structure in Pyodide
                pyodide.FS.mkdir('/scripts');
                
                // Load each py_html file
                for (const file of pyHtmlFiles) {{
                    try {{
                        const response = await fetch(file);
                        const content = await response.text();
                        pyodide.FS.writeFile(`/${{file}}`, content);
                        console.log(`Loaded ${{file}}`);
                    }} catch (error) {{
                        console.warn(`Could not load ${{file}}:`, error);
                    }}
                }}
                
                // Load Python files from scripts folder
                const pythonFiles = {python_files};
                for (const file of pythonFiles) {{
                    try {{
                        const response = await fetch(file);
                        const content = await response.text();
                        pyodide.FS.writeFile(`/${{file}}`, content);
                        console.log(`Loaded ${{file}}`);
                    }} catch (error) {{
                        console.warn(`Could not load ${{file}}:`, error);
                    }}
                }}
                
                // Add py_html and scripts to Python path
                await pyodide.runPython(`
                    import sys
                    sys.path.insert(0, '/py_html')
                    sys.path.insert(0, '/scripts')
                    sys.path.insert(0, '/')
                    print("Python path updated with py_html and scripts")
                `);
                
                // Execute the specific main script for this page
                const mainScript = '{scripts_folder}/{page.main_script}';
                if (pythonFiles.includes(mainScript)) {{
                    const response = await fetch(mainScript);
                    const mainCode = await response.text();
                    await pyodide.runPython(mainCode);
                    console.log(`Executed ${{mainScript}}`);
                }} else {{
                    console.warn(`Main script not found: ${{mainScript}}`);
                }}
                
                // Hide loading and show content
                document.getElementById('loading').style.display = 'none';
                document.getElementById('content').style.display = 'block';
                
            }} catch (error) {{
                console.error('Error loading Pyodide:', error);
                document.getElementById('loading').innerHTML = `
                    <p style="color: red;">Error loading application: ${{error.message}}</p>
                `;
            }}
        }}
        
        // Start loading when page is ready
        window.addEventListener('DOMContentLoaded', initializeApp);
    </script>
</body>
</html>'''
        
        # Create output directory if needed
        output_path = Path(page.filename).parent
        if output_path != Path('.'):
            output_path.mkdir(parents=True, exist_ok=True)
        
        # Write the HTML file
        with open(page.filename, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        results.append(f"Generated {page.filename} (main script: {page.main_script}, title: {page.title})")
    
    return "\\n".join(results)
