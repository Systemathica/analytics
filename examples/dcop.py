import os
import shutil

def copy_filtered_files(src, dst, extensions):
    """
    Copies files from src to dst, preserving the folder structure,
    but only copying files with extensions in the extensions list.
    """
    if not os.path.exists(dst):
        os.makedirs(dst)

    for root, dirs, files in os.walk(src):
        # Determine the destination directory
        dest_dir = os.path.join(dst, os.path.relpath(root, src))

        # Create the destination directory if it doesn't exist
        if not os.path.exists(dest_dir):
            os.makedirs(dest_dir)

        # Copy each file with the allowed extension
        for file in files:
            if any(file.endswith(ext) for ext in extensions):
                src_file = os.path.join(root, file)
                dst_file = os.path.join(dest_dir, file)
                shutil.copy2(src_file, dst_file)

# Example usage
source_directory = r'C:\Users\raman\OneDrive\Desktop\Doc\Test'
destination_directory = r'C:\Users\raman\OneDrive\Desktop\Doc\TestCopy'
allowed_extensions = ['.pptx', '.xlsx', '.docx']  # Add or remove extensions as needed

copy_filtered_files(source_directory, destination_directory, allowed_extensions)
