#!/usr/bin/env python3
# =========================================================================
# export_repo.py
# =========================================================================
# Author: Nic Cravino
# Created: May 25th, 2025
# =========================================================================
# This script exports a repository's structure and contents to a single, human-readable text file. Binary files are base64 encoded.
# =========================================================================
# License Apache 2 ...
#

import os
import base64
from pathlib import Path

def is_binary(file_path):
    """Check if a file is binary."""
    try:
        with open(file_path, 'rb') as f:
            # Read first 8000 bytes to check for binary content
            chunk = f.read(8000)
            # Check for null bytes or high byte values
            if b'\x00' in chunk:
                return True
            # Try to decode as text
            try:
                chunk.decode('utf-8')
            except UnicodeDecodeError:
                return True
    except Exception as e:
        print(f"Error checking if file is binary: {e}")
        return True
    return False

def get_file_contents(file_path, relative_path):
    """Get file contents with appropriate encoding."""
    if is_binary(file_path):
        try:
            with open(file_path, 'rb') as f:
                content = f.read()
                return f"\n[Binary file - {len(content)} bytes - base64 encoded]\n{base64.b64encode(content).decode('ascii')}\n"
        except Exception as e:
            return f"\n[Error reading binary file: {e}]\n"
    else:
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return f.read()
        except Exception as e:
            return f"\n[Error reading file: {e}]\n"

def export_repository(root_dir, output_file):
    """Export repository structure and contents to a single text file."""
    root_path = Path(root_dir).resolve()
    output_path = Path(output_file).resolve()
    
    print(f"Exporting repository from: {root_path}")
    print(f"Output file: {output_path}")
    
    with open(output_path, 'w', encoding='utf-8') as outfile:
        # Write header
        outfile.write("=" * 80 + "\n")
        outfile.write(f"REPOSITORY EXPORT: {root_path.name}\n")
        outfile.write(f"Generated on: {datetime.datetime.now().isoformat()}\n")
        outfile.write("=" * 80 + "\n\n")
        
        # Walk through the directory
        for current_dir, dirs, files in os.walk(root_path):
            # Skip hidden directories (like .git)
            dirs[:] = [d for d in dirs if not d.startswith('.')]
            
            relative_dir = Path(current_dir).relative_to(root_path)
            
            # Write directory header
            if str(relative_dir) != '.':
                outfile.write("\n" + "#" * 80 + "\n")
                outfile.write(f"DIRECTORY: {relative_dir}\n")
                outfile.write("#" * 80 + "\n\n")
            
            # Process files
            for file in sorted(files):
                if file.startswith('.'):
                    continue  # Skip hidden files
                    
                file_path = Path(current_dir) / file
                relative_file_path = relative_dir / file
                
                # Write file header
                outfile.write("\n" + "-" * 60 + "\n")
                outfile.write(f"FILE: {relative_file_path}\n")
                outfile.write("-" * 60 + "\n\n")
                
                # Write file contents
                try:
                    content = get_file_contents(file_path, relative_file_path)
                    outfile.write(content)
                    if not content.endswith('\n'):
                        outfile.write('\n')
                except Exception as e:
                    outfile.write(f"[Error processing file: {e}]\n")
                
                outfile.write("\n" + "=" * 60 + "\n\n")
    
    print(f"\nExport completed successfully to: {output_path}")
    print(f"Total size: {os.path.getsize(output_path) / (1024 * 1024):.2f} MB")

if __name__ == "__main__":
    import sys
    import datetime
    
    if len(sys.argv) > 1:
        root_directory = sys.argv[1]
    else:
        root_directory = os.getcwd()
    
    output_filename = f"{Path(root_directory).name}_export_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
    
    try:
        export_repository(root_directory, output_filename)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)
