#!/usr/bin/env python3
"""
Create distribution package for Nedlastarn
"""

import zipfile
import os
from pathlib import Path
from datetime import datetime

def create_distribution():
    """Create a distribution ZIP package"""
    
    # Get current directory
    current_dir = Path(__file__).parent
    
    # Define paths
    exe_path = current_dir / "dist" / "Nedlastarn.exe"
    readme_path = current_dir / "README.md"
    license_path = current_dir / "LICENSE"
    
    # Create distribution directory
    dist_dir = current_dir / "distribution"
    dist_dir.mkdir(exist_ok=True)
    
    # Create ZIP filename with timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M")
    zip_filename = f"Nedlastarn_v1.0_{timestamp}.zip"
    zip_path = dist_dir / zip_filename
    
    print(f"Creating distribution package: {zip_filename}")
    
    # Create ZIP file
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        # Add executable
        if exe_path.exists():
            zipf.write(exe_path, "Nedlastarn.exe")
            print(f"Added: Nedlastarn.exe ({exe_path.stat().st_size / 1024 / 1024:.1f} MB)")
        else:
            print("ERROR: Nedlastarn.exe not found!")
            return False
        
        # Add README
        if readme_path.exists():
            zipf.write(readme_path, "README.md")
            print("Added: README.md")
        
        # Add LICENSE
        if license_path.exists():
            zipf.write(license_path, "LICENSE")
            print("Added: LICENSE")
        
        # Add FFmpeg info file
        ffmpeg_info = """FFmpeg Installation Instructions
================================

Nedlastarn requires FFmpeg for video/audio conversion.

1. Download FFmpeg from: https://ffmpeg.org/download.html
2. Extract ffmpeg.exe to the same folder as Nedlastarn.exe
3. Run Nedlastarn.exe

Alternative: Install FFmpeg system-wide and add it to your PATH.

For more information, see: https://ffmpeg.org/download.html
"""
        zipf.writestr("FFmpeg_Instructions.txt", ffmpeg_info)
        print("Added: FFmpeg_Instructions.txt")
    
    print(f"\nDistribution package created: {zip_path}")
    print(f"Package size: {zip_path.stat().st_size / 1024 / 1024:.1f} MB")
    
    return True

if __name__ == "__main__":
    create_distribution()
