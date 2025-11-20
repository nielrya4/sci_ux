#!/usr/bin/env python3
"""
Download ipywidgets and dependencies for local Pyodide installation
"""

import os
import sys
import subprocess
import urllib.request
import json

def download_file(url, filename):
    """Download a file from URL"""
    print(f"Downloading {filename}...")
    try:
        urllib.request.urlretrieve(url, filename)
        print(f"✅ Downloaded {filename}")
        return True
    except Exception as e:
        print(f"❌ Error downloading {filename}: {e}")
        return False

def main():
    # ipywidgets and its dependencies that work with Pyodide
    packages = [
        "ipywidgets-8.1.5-py3-none-any.whl",
        "widgetsnbextension-4.0.11-py3-none-any.whl", 
        "jupyterlab_widgets-3.0.13-py3-none-any.whl",
        "comm-0.2.2-py3-none-any.whl",
        "traitlets-5.14.3-py3-none-any.whl",
    ]
    
    # Base PyPI URL
    base_url = "https://files.pythonhosted.org/packages"
    
    # Package URLs (simplified - these are common compatible versions)
    urls = {
        "ipywidgets-8.1.5-py3-none-any.whl": f"{base_url}/6a/b8/bac96af3969bb86b444be6e3615b2b77b8e5a8e1feee0a3edbfd64cb9e4d0c/ipywidgets-8.1.5-py3-none-any.whl",
        "widgetsnbextension-4.0.11-py3-none-any.whl": f"{base_url}/b6/54/6d61f24ed26899a62cb7e0cb645e88d96b5b16a8b36be8e7e5b1caed8e01c/widgetsnbextension-4.0.11-py3-none-any.whl",
        "jupyterlab_widgets-3.0.13-py3-none-any.whl": f"{base_url}/a6/9c/07a99b36f5b42de68e22be90f5c0def2b6513dc63e2d25cde0c4e6a4a6f5/jupyterlab_widgets-3.0.13-py3-none-any.whl",
        "comm-0.2.2-py3-none-any.whl": f"{base_url}/e6/75/49e5bfe642f71f8d5c2ac06cf1b5b7085851d4b8d19b4bd8f05b0c1e3a9b/comm-0.2.2-py3-none-any.whl",
        "traitlets-5.14.3-py3-none-any.whl": f"{base_url}/39/c3/205e88f02959712cb1e0eeb3a5b7dbea2f64d3b68bea8ee4a1bc6d70db13/traitlets-5.14.3-py3-none-any.whl",
    }
    
    print("🔧 Downloading ipywidgets and dependencies...")
    
    success_count = 0
    for package in packages:
        if package in urls:
            if download_file(urls[package], package):
                success_count += 1
        else:
            print(f"⚠️ No URL found for {package}")
    
    print(f"\n📊 Downloaded {success_count}/{len(packages)} packages")
    
    if success_count == len(packages):
        print("✅ All packages downloaded successfully!")
        print("\n📝 Next steps:")
        print("1. These .whl files are now available in your local Pyodide directory")
        print("2. Update your HTML to use loadPackage() instead of micropip.install()")
        print("3. Or manually install with micropip.install('file:package-name.whl')")
    else:
        print("⚠️ Some packages failed to download. Check your internet connection.")

if __name__ == "__main__":
    main()