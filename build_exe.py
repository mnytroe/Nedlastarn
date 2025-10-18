#!/usr/bin/env python3
"""
Build script for Nedlastarn executable
"""

import PyInstaller.__main__
import os
import sys
from pathlib import Path

def build_executable():
    """Build Nedlastarn as a standalone executable"""
    
    # Get the current directory
    current_dir = Path(__file__).parent
    
    # Define paths
    main_script = current_dir / "Nedlastarn.py"
    icon_path = current_dir / "icon.ico"  # Optional icon file
    
    # PyInstaller arguments
    args = [
        str(main_script),
        "--name=Nedlastarn",
        "--onefile",  # Create a single executable file
        "--windowed",  # No console window (GUI app)
        "--clean",  # Clean cache before building
        "--noconfirm",  # Overwrite output directory without asking
        
        # Add data files
        "--add-data=README.md;.",  # Include README
        "--add-data=LICENSE;.",  # Include LICENSE
        
        # Optimize for size
        "--strip",  # Strip debug symbols
        "--optimize=2",  # Python optimization level
        
        # Exclude unnecessary modules to reduce size
        "--exclude-module=tkinter.test",
        "--exclude-module=test",
        "--exclude-module=unittest",
        "--exclude-module=pydoc",
        "--exclude-module=doctest",
        
        # Custom options
        "--distpath=dist",  # Output directory
        "--workpath=build",  # Temporary files directory
        "--specpath=.",  # Spec file location
    ]
    
    # Add icon if it exists
    if icon_path.exists():
        args.extend(["--icon", str(icon_path)])
    
    print("Building Nedlastarn executable...")
    print(f"Working directory: {current_dir}")
    print(f"Main script: {main_script}")
    
    try:
        PyInstaller.__main__.run(args)
        print("Build completed successfully!")
        print("Executable created in: dist/Nedlastarn.exe")
        
    except Exception as e:
        print(f"Build failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    build_executable()
