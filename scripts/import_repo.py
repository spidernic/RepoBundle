#!/usr/bin/env python3
# =========================================================================
# import_repo.py
# =========================================================================
# Author: Nic Cravino
# Created: May 25th, 2025
# =========================================================================
# This script restores a repository from a human-readable export file, reconstructing both text and binary files.
# =========================================================================
# License Apache 2 ...
#

import os
import re
import base64
import argparse
from pathlib import Path

def parse_export_file(export_file):
    """Parse the exported file and yield (file_path, content, is_binary) tuples."""
    with open(export_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Skip the header
    content = content.split('DIRECTORY: .\n', 1)[-1]
    
    # Split into file sections
    file_sections = re.split(r'\n-{60}\nFILE: (.*?)\n-{60}\n', content)[1:]
    
    for i in range(0, len(file_sections), 2):
        if i + 1 >= len(file_sections):
            break
            
        file_path = file_sections[i]
        file_content = file_sections[i+1]
        
        # Check if this is a binary file
        is_binary = False
        binary_match = re.match(r'\[Binary file - (\d+) bytes - base64 encoded\]\n([\s\S]*?)(?=\n\n=)', file_content, re.DOTALL)
        
        if binary_match:
            is_binary = True
            file_content = binary_match.group(2).strip()
        else:
            # For text files, get content up to the next file marker
            file_content = file_content.split('\n' + '='*60)[0]
        
        yield file_path, file_content, is_binary

def restore_repository(export_file, output_dir):
    """Restore the repository from the exported file."""
    output_path = Path(output_dir).resolve()
    os.makedirs(output_path, exist_ok=True)
    
    print(f"Restoring repository to: {output_path}")
    
    for file_path, content, is_binary in parse_export_file(export_file):
        full_path = output_path / file_path
        
        # Create parent directories if they don't exist
        os.makedirs(full_path.parent, exist_ok=True)
        
        # Write file content
        try:
            if is_binary:
                # Decode base64 content
                binary_data = base64.b64decode(content)
                with open(full_path, 'wb') as f:
                    f.write(binary_data)
                print(f"Restored binary file: {file_path} ({len(binary_data)} bytes)")
            else:
                with open(full_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                print(f"Restored text file: {file_path} ({len(content)} characters)")
        except Exception as e:
            print(f"Error restoring {file_path}: {e}")
    
    print(f"\nRepository restoration complete to: {output_path}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Restore repository from exported file.')
    parser.add_argument('export_file', help='Path to the exported repository file')
    parser.add_argument('-o', '--output', default='restored_repo', 
                       help='Output directory (default: ./restored_repo)')
    
    args = parser.parse_args()
    
    if not os.path.exists(args.export_file):
        print(f"Error: File not found: {args.export_file}")
        exit(1)
    
    try:
        restore_repository(args.export_file, args.output)
    except Exception as e:
        print(f"Error: {e}")
        exit(1)
