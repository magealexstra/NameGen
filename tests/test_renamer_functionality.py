#!/usr/bin/env python3
"""
Test script for verifying the renamer engine functionality
"""
import os
import sys
import tempfile
from pathlib import Path

# Add the parent directory to the path so we can import from src
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.renamer_engine import (
    improved_title_case,
    change_case,
    add_sequential_number,
    generate_preview_name
)

def test_title_case():
    """Test title case functionality"""
    print("\n=== Testing Title Case ===")
    test_cases = [
        "stary jack",
        "the quick brown fox jumps over the lazy dog",
        "a to an of with by in or and",
        "o'connor's test",
        "test_with_underscores",
        "test-with-hyphens",
        "UPPERCASE TEXT",
        "MiXeD cAsE tExT"
    ]
    
    print("Input -> Output:")
    for test in test_cases:
        result = improved_title_case(test)
        print(f"'{test}' -> '{result}'")

def test_case_functions():
    """Test case change functions"""
    print("\n=== Testing Case Functions ===")
    test_filename = "stary_jack.jpg"
    
    print("Input filename:", test_filename)
    print(f"lowercase: '{change_case(test_filename, 'lower')}'")
    print(f"UPPERCASE: '{change_case(test_filename, 'upper')}'")
    print(f"Title Case: '{change_case(test_filename, 'title case')}'")
    print(f"Preserve: '{change_case(test_filename, 'preserve')}'")

def test_sequential_numbering():
    """Test sequential numbering functionality"""
    print("\n=== Testing Sequential Numbering ===")
    filename = "test.jpg"
    
    options = {"padding": 2, "start": 1, "step": 1, "position": "suffix", "separator": "_"}
    print("Default options:", options)
    for i in range(5):
        result = add_sequential_number(filename, i, options)
        print(f"File {i+1}: '{result}'")
    
    print("\nCustom options (prefix, padding=3, start=10, step=5):")
    options = {"padding": 3, "start": 10, "step": 5, "position": "prefix", "separator": "-"}
    for i in range(5):
        result = add_sequential_number(filename, i, options)
        print(f"File {i+1}: '{result}'")

def test_name_replacement():
    """Test name replacement functionality"""
    print("\n=== Testing Name Replacement ===")
    
    original_paths = [
        "/path/to/some_image.jpg",
        "/path/to/another_file.png",
        "/path/to/document.pdf"
    ]
    
    # Test full name replacement
    scheme_params = {
        "replace_name": True,
        "new_name": "Stary Jack",
        "case_option": "title case"
    }
    
    print("Original -> New (replace_name=True, new_name='Stary Jack', title case):")
    for i, path in enumerate(original_paths):
        filename = os.path.basename(path)
        result = generate_preview_name(path, i, scheme_params)
        print(f"'{filename}' -> '{result}'")

def test_find_replace():
    """Test find and replace functionality"""
    print("\n=== Testing Find and Replace ===")
    
    original_paths = [
        "/path/to/image_01.jpg",
        "/path/to/image_02.png",
        "/path/to/document_03.pdf"
    ]
    
    # Test find and replace
    scheme_params = {
        "replace_name": False,
        "find": "image",
        "replace": "photo",
        "case_option": "preserve"
    }
    
    print("Original -> New (find='image', replace='photo'):")
    for i, path in enumerate(original_paths):
        filename = os.path.basename(path)
        result = generate_preview_name(path, i, scheme_params)
        print(f"'{filename}' -> '{result}'")

def test_combined_options():
    """Test combined options"""
    print("\n=== Testing Combined Options ===")
    
    original_paths = [
        "/path/to/test_image_1.jpg",
        "/path/to/test_image_2.jpg",
        "/path/to/test_image_3.jpg"
    ]
    
    # Test with multiple options enabled
    scheme_params = {
        "replace_name": True,
        "new_name": "vacation photo",
        "find": "photo",
        "replace": "picture",
        "case_option": "title case",
        "use_numbering": True,
        "number_options": {
            "padding": 2,
            "start": 10,
            "step": 1,
            "position": "suffix",
            "separator": "_"
        }
    }
    
    print("Testing multiple options combined:")
    print("- Replace name with 'vacation photo'")
    print("- Find 'photo' and replace with 'picture'")
    print("- Apply Title Case")
    print("- Add sequential numbering (suffix, start=10)")
    print("\nOriginal -> New:")
    
    for i, path in enumerate(original_paths):
        filename = os.path.basename(path)
        result = generate_preview_name(path, i, scheme_params)
        print(f"'{filename}' -> '{result}'")

def main():
    """Run all tests"""
    print("=== Renamer Engine Functionality Tests ===")
    
    test_title_case()
    test_case_functions()
    test_sequential_numbering()
    test_name_replacement()
    test_find_replace()
    test_combined_options()
    
    print("\nAll tests completed.")

if __name__ == "__main__":
    main()
