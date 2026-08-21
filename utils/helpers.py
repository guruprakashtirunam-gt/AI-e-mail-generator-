"""
Purpose: Contains utility/helper functions that can be reused across different modules.
"""

import os
from typing import List
from streamlit.runtime.uploaded_file_manager import UploadedFile

def save_uploaded_files(uploaded_files: List[UploadedFile], save_dir: str) -> List[str]:
    """
    Saves uploaded Streamlit files to a local directory.
    
    Args:
        uploaded_files (List[UploadedFile]): List of files uploaded via Streamlit.
        save_dir (str): Directory where files should be saved.
        
    Returns:
        List[str]: List of file paths where the files were saved.
    """
    os.makedirs(save_dir, exist_ok=True)
    saved_paths = []
    
    for uploaded_file in uploaded_files:
        file_path = os.path.join(save_dir, uploaded_file.name)
        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        saved_paths.append(file_path)
        
    return saved_paths

def clear_directory(directory: str) -> None:
    """
    Deletes all files within a specified directory.
    
    Args:
        directory (str): Path to the directory to be cleared.
    """
    if os.path.exists(directory):
        for filename in os.listdir(directory):
            file_path = os.path.join(directory, filename)
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)
            except Exception as e:
                print(f"Failed to delete {file_path}. Reason: {e}")
