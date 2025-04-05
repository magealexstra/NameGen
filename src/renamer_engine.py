"""
Core renaming logic implementation
"""
import os
import shutil
import re
from pathlib import Path
from typing import List, Dict, Tuple, Optional, Any, Union



def improved_title_case(text: str) -> str:
    """
    Convert a string to title case with improved handling of word boundaries
    and special cases.
    
    Args:
        text: The text to convert to title case
    
    Returns:
        The text converted to proper title case
    """
    # Handle empty strings
    if not text:
        return text
    
    # Words that should not be capitalized in title case
    # (unless they are the first or last word)
    lowercase_words = {
        'a', 'an', 'the', 'and', 'but', 'or', 'for', 'nor', 'as', 'at', 
        'by', 'for', 'from', 'in', 'into', 'near', 'of', 'on', 'onto', 
        'to', 'with'
    }
    
    # Split by word boundaries considering spaces, hyphens, and underscores
    words = re.split(r'([\s_-]+)', text)
    result = []
    
    for i, word in enumerate(words):
        # Check if it's a word or a separator
        if i % 2 == 0:  # Even indices are words
            # Skip empty words
            if not word:
                result.append(word)
                continue
                
            # First letter uppercase, rest lowercase
            word_lower = word.lower()
            
            # First word, last word, or not in lowercase_words list
            if (i == 0 or i == len(words) - 1 or 
                    word_lower not in lowercase_words):
                # Handle apostrophes correctly
                # For example "O'Connor" should be "O'Connor" not "O'connor"
                if "'" in word:
                    parts = word.split("'")
                    result.append(parts[0][0].upper() + parts[0][1:].lower() + 
                                  "'" + parts[1][0].upper() + parts[1][1:].lower())
                else:
                    result.append(word[0].upper() + word[1:].lower())
            else:
                result.append(word_lower)
        else:  # Separators
            result.append(word)
    
    return ''.join(result)

def change_case(name: str, case_option: str) -> str:
    """
    Change the case of the filename.
    
    Args:
        name: Original filename (with or without extension)
        case_option: Type of case change ('lower', 'upper', 'title case', 'preserve')
    
    Returns:
        Modified filename
    """
    # Split the name into base and extension
    base_name, ext = os.path.splitext(name)
    
    # Apply the case transformation to the base name
    if case_option == "lower":
        new_base = base_name.lower()
    elif case_option == "upper":
        new_base = base_name.upper()
    elif case_option in ("title", "title case"):
        new_base = improved_title_case(base_name)
    else:  # "preserve" or any other value
        new_base = base_name
    
    # Return the modified name with the original extension
    return f"{new_base}{ext}"

def format_number(number: int, padding: int = 2, start: int = 1, step: int = 1) -> str:
    """
    Format a number with specified padding.
    
    Args:
        number: The index to use for calculating the number
        padding: Number of digits to pad to (e.g., 2 -> 01, 02, etc.)
        start: Starting number (e.g., 1, 100, etc.)
        step: Increment between numbers (default 1)
    
    Returns:
        Formatted number string
    """
    # Calculate the actual number based on start, index, and step
    # Our numbering is 1-based for user display, so add 1 to the index
    actual_number = start + (number * step)
    
    # Format the number with the specified padding
    return str(actual_number).zfill(padding)


def generate_preview_name(original_path: str, index: int, scheme_params: Dict[str, Any]) -> str:
    """
    Generate a preview of the renamed file based on the renaming scheme.
    
    Args:
        original_path: Path to the original file
        index: The index of the file in the list (0-based)
        scheme_params: Dictionary with renaming scheme parameters:
            - replace_name: Whether to replace the entire name with new_name
            - new_name: New name to use if replacing the entire name
            - prefix: String to add at the beginning (if not replacing the name)
            - suffix: String to add at the end (if not replacing the name)
            - find: Substring to find
            - replace: Replacement string
            - case_option: Type of case change ('lower', 'upper', 'title', 'preserve')
            - use_numbering: Whether to add sequential numbers
            - number_options: Options for sequential numbering
    
    Returns:
        Preview of the renamed file (filename only, no path)
    """
    # Get the original filename without path
    filename = os.path.basename(original_path)

    # If replacing the entire name, use the new name
    if scheme_params.get("replace_name", False):
        # Keep the original extension
        _, ext = os.path.splitext(filename)
        filename = scheme_params.get("new_name", "") + ext
    else:
        # Otherwise, apply prefix and suffix manually
        prefix = scheme_params.get("prefix", "")
        suffix = scheme_params.get("suffix", "")
        base_name, ext = os.path.splitext(filename)
        filename = f"{prefix}{base_name}{suffix}{ext}"

    # Apply find and replace if specified
    find_str = scheme_params.get("find", "")
    replace_str = scheme_params.get("replace", "")
    if find_str:
        base_name, ext = os.path.splitext(filename)
        base_name = base_name.replace(find_str, replace_str)
        filename = f"{base_name}{ext}"

    # Apply case change if specified
    case_option = scheme_params.get("case_option", "preserve")
    if case_option != "preserve":
        filename = change_case(filename, case_option)

    # Apply sequential numbering if enabled
    if scheme_params.get("use_numbering", False):
        number_options = scheme_params.get("number_options", {})
        filename = add_sequential_number(filename, index, number_options)

    return filename


def add_sequential_number(name: str, index: int, options: Dict[str, Any]) -> str:
    """
    Add a sequential number to a filename.
    
    Args:
        name: Original filename (with or without extension)
        index: The index of the file in the list (0-based)
        options: Dictionary with options:
            - padding: Number of digits to pad to (e.g., 2 -> 01, 02, etc.)
            - start: Starting number (e.g., 1, 100, etc.)
            - step: Increment between numbers (default 1)
            - position: Where to add the number ('prefix', 'suffix')
            - separator: String to use between number and name
     
    Returns:
        Modified filename with sequential number
    """
    # Extract options with defaults
    padding = options.get("padding", 2)
    start = options.get("start", 1)
    step = options.get("step", 1)
    position = options.get("position", "suffix")
    separator = options.get("separator", "_")
    
    # Format the number
    formatted_number = format_number(index, padding, start, step)
    
    # Split the name into base and extension
    base_name, ext = os.path.splitext(name)
    
    # Add the number to the appropriate position
    if position == "prefix":
        new_base = f"{formatted_number}{separator}{base_name}"
    else:  # suffix or any other value
        new_base = f"{base_name}{separator}{formatted_number}"
    
    # Return the modified name with the original extension
    return f"{new_base}{ext}"

    
    # Apply case change
    if scheme_params.get("case_option", "preserve") != "preserve":
        filename = change_case(
            filename, 
            scheme_params.get("case_option", "preserve")
        )
    
    # Apply sequential numbering
    if scheme_params.get("use_numbering", False):
        number_options = scheme_params.get("number_options", {})
        filename = add_sequential_number(
            filename, 
            index, 
            number_options
        )
    
    return filename

def get_example_previews(file_list: List[str], scheme_params: Dict[str, Any], count: int = 5) -> List[Tuple[str, str]]:
    """
    Generate example previews for a list of files.
    
    Args:
        file_list: List of file paths
        scheme_params: Dictionary with renaming scheme parameters
        count: Number of examples to generate (default 5)
    
    Returns:
        List of tuples (original_filename, preview_filename)
    """
    previews = []
    
    # Limit to the specified count
    file_count = min(len(file_list), count)
    
    for i in range(file_count):
        original_path = file_list[i]
        original_filename = os.path.basename(original_path)
        
        preview_filename = generate_preview_name(original_path, i, scheme_params)
        
        previews.append((original_filename, preview_filename))
    
    return previews


def apply_rename(files_to_process: List[Tuple[str, int]], scheme_params: Dict[str, Any], move_to_folder: Optional[str] = None) -> Dict[str, Union[str, List[Tuple[str, str, str]]]]:
    """
    Apply the renaming scheme to a list of files.
    
    Args:
        files_to_process: List of tuples (original_path, index)
        scheme_params: Dictionary with renaming scheme parameters
        move_to_folder: Target folder to move files to (if specified)
    
    Returns:
        Dictionary with the result of the operation:
            - status: 'success' or 'error'
            - results: List of tuples (original_path, new_path, 'success' or error message)
            - message: Summary message
    """
    # Result tracking
    results = []
    success_count = 0
    error_count = 0
    
    # Ensure destination folder exists if specified
    if move_to_folder and not os.path.exists(move_to_folder):
        try:
            os.makedirs(move_to_folder)
        except Exception as e:
            return {
                "status": "error",
                "results": [],
                "message": f"Failed to create destination folder: {str(e)}"
            }
    
    # Process each file
    for original_path, index in files_to_process:
        try:
            # Generate the new filename
            new_name = generate_preview_name(original_path, index, scheme_params)
            
            # Determine the target path
            if move_to_folder:
                target_path = os.path.join(move_to_folder, new_name)
                # Use shutil.move for moving across filesystems
                shutil.move(original_path, target_path)
            else:
                # Rename in place
                target_dir = os.path.dirname(original_path)
                target_path = os.path.join(target_dir, new_name)
                os.rename(original_path, target_path)
            
            # Track success
            results.append((original_path, target_path, "success"))
            success_count += 1
            
        except FileNotFoundError:
            results.append((original_path, "", "File not found"))
            error_count += 1
        except PermissionError:
            results.append((original_path, "", "Permission denied"))
            error_count += 1
        except FileExistsError:
            results.append((original_path, "", "Destination file already exists"))
            error_count += 1
        except Exception as e:
            results.append((original_path, "", f"Error: {str(e)}"))
            error_count += 1
    
    # Determine the overall status
    status = "success" if error_count == 0 else "partial" if success_count > 0 else "error"
    
    # Generate summary message
    message = f"Renamed {success_count} files successfully"
    if error_count > 0:
        message += f", {error_count} failed"
    
    return {
        "status": status,
        "results": results,
        "message": message
    }
def check_conflicts_and_validity(file_list: List[str], scheme_params: Dict[str, Any], destination_folder: Optional[str] = None) -> Dict[str, List[Tuple[str, str]]]:
    """
    Check for conflicts and validity issues with the renaming scheme.
    
    Args:
        file_list: List of file paths to be renamed
        scheme_params: Dictionary with renaming scheme parameters
        destination_folder: Target folder for the renamed files (if moving)
    
    Returns:
        Dictionary with identified issues:
            - duplicates: List of (original_path, new_name) tuples for duplicate new names
            - invalid_chars: List of (original_path, new_name) tuples with invalid characters
            - existing_files: List of (original_path, new_name) tuples that would overwrite existing files
    """
    # Initialize the report
    report = {
        "duplicates": [],
        "invalid_chars": [],
        "existing_files": []
    }
    
    # Invalid characters in filenames (platform-dependent)
    invalid_pattern = r'[\\/:*?"<>|]' if os.name == 'nt' else r'/'
    
    # Track new names to detect duplicates
    new_names = {}
    
    # Process each file
    for i, original_path in enumerate(file_list):
        # Generate the new filename
        new_name = generate_preview_name(original_path, i, scheme_params)
        
        # Check for invalid characters
        if re.search(invalid_pattern, new_name):
            report["invalid_chars"].append((original_path, new_name))
        
        # Determine the target path
        if destination_folder:
            target_path = os.path.join(destination_folder, new_name)
        else:
            target_path = os.path.join(os.path.dirname(original_path), new_name)
        
        # Check for duplicates
        if new_name in new_names:
            report["duplicates"].append((original_path, new_name))
        else:
            new_names[new_name] = original_path
        
        # Check for existing files (if original and new path are different)
        if os.path.normpath(original_path) != os.path.normpath(target_path) and os.path.exists(target_path):
            report["existing_files"].append((original_path, new_name))
    
    return report

