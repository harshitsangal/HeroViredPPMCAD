#!/usr/bin/env python3

import os
import sys
import shutil
from datetime import datetime

def make_backup(source_dir, dest_dir):
    # Ensure source exists and is a directory
    if not os.path.exists(source_dir):
        print(f"Error: Source directory '{source_dir}' does not exist.")
        return
    if not os.path.isdir(source_dir):
        print(f"Error: Source '{source_dir}' is not a directory.")
        return

    # Ensure destination exists; if not, try to create it
    if not os.path.exists(dest_dir):
        try:
            os.makedirs(dest_dir, exist_ok=True)
            print(f"Created destination directory '{dest_dir}'.")
        except Exception as e:
            print(f"Error: Could not create destination directory '{dest_dir}': {e}")
            return
    elif not os.path.isdir(dest_dir):
        print(f"Error: Destination '{dest_dir}' is not a directory.")
        return

    # Iterate over items in source directory
    for item in os.listdir(source_dir):
        src_path = os.path.join(source_dir, item)
        # Skip subdirectories — only copy files
        if not os.path.isfile(src_path):
            continue

        base_name, ext = os.path.splitext(item)
        dest_path = os.path.join(dest_dir, item)

        # If file with same name exists in destination, append timestamp
        if os.path.exists(dest_path):
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            new_name = f"{base_name}_{timestamp}{ext}"
            dest_path = os.path.join(dest_dir, new_name)

        try:
            # Use copy2 to preserve metadata (timestamp, permissions) if possible
            shutil.copy2(src_path, dest_path)
            print(f"Copied '{src_path}' ➜ '{dest_path}'")
        except Exception as e:
            print(f"Error copying '{src_path}' to '{dest_path}': {e}")

def main():
    if len(sys.argv) != 3:
        print("Usage: python backup.py /path/to/source /path/to/destination")
        sys.exit(1)

    source_dir = sys.argv[1]
    dest_dir = sys.argv[2]

    make_backup(source_dir, dest_dir)

if __name__ == "__main__":
    main()
