"""
Basic tests for the image renamer functionality
"""
import os
import sys
import unittest
from pathlib import Path

# Add the src directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from renamer_engine import (
    add_prefix_suffix,
    replace_substring,
    change_case,
    format_number,
    add_sequential_number,
    generate_preview_name
)


class TestRenamerFunctions(unittest.TestCase):
    """Test basic functionality of the renamer engine functions"""

    def test_add_prefix_suffix(self):
        """Test adding prefix and suffix"""
        # Test adding prefix
        self.assertEqual(add_prefix_suffix("image.jpg", "prefix_", ""), "prefix_image.jpg")
        # Test adding suffix
        self.assertEqual(add_prefix_suffix("image.jpg", "", "_suffix"), "image_suffix.jpg")
        # Test adding both
        self.assertEqual(add_prefix_suffix("image.jpg", "prefix_", "_suffix"), "prefix_image_suffix.jpg")
        # Test with empty strings
        self.assertEqual(add_prefix_suffix("image.jpg", "", ""), "image.jpg")

    def test_replace_substring(self):
        """Test replacing substrings"""
        # Basic replacement
        self.assertEqual(replace_substring("image001.jpg", "001", "002"), "image002.jpg")
        # Case sensitivity
        self.assertEqual(replace_substring("IMAGE.jpg", "IMAGE", "image"), "image.jpg")
        # Multiple occurrences
        self.assertEqual(replace_substring("img_img.jpg", "img", "image"), "image_image.jpg")
        # No match
        self.assertEqual(replace_substring("image.jpg", "foo", "bar"), "image.jpg")
        # Empty find string
        self.assertEqual(replace_substring("image.jpg", "", "bar"), "image.jpg")

    def test_change_case(self):
        """Test case changing"""
        # To lowercase
        self.assertEqual(change_case("IMAGE.jpg", "lower"), "image.jpg")
        # To uppercase
        self.assertEqual(change_case("image.jpg", "upper"), "IMAGE.jpg")
        # To title case
        self.assertEqual(change_case("image_file.jpg", "title"), "Image_File.jpg")
        # Preserve case
        self.assertEqual(change_case("iMaGe.jpg", "preserve"), "iMaGe.jpg")
        # Invalid option defaults to preserve
        self.assertEqual(change_case("image.jpg", "invalid"), "image.jpg")

    def test_format_number(self):
        """Test number formatting"""
        # Basic padding (with our 1-based approach)
        self.assertEqual(format_number(0, 3), "001")  # Index 0 gives number 1 with padding 3
        # Custom start
        self.assertEqual(format_number(0, 2, 5), "05")  # Start at 5, index 0
        # With step
        self.assertEqual(format_number(2, 2, 1, 10), "21")  # 1 + (2 * 10) = 21
        # No padding
        self.assertEqual(format_number(6, 1), "7")  # 1 + 6 = 7

    def test_add_sequential_number(self):
        """Test adding sequential numbers"""
        options = {"padding": 2, "start": 1, "step": 1, "position": "suffix", "separator": "_"}
        # Default suffix position
        self.assertEqual(add_sequential_number("image.jpg", 0, options), "image_01.jpg")
        
        # Prefix position
        options["position"] = "prefix"
        self.assertEqual(add_sequential_number("image.jpg", 1, options), "02_image.jpg")
        
        # Custom separator
        options["separator"] = "-"
        self.assertEqual(add_sequential_number("image.jpg", 2, options), "03-image.jpg")

    def test_generate_preview_name(self):
        """Test the preview name generation"""
        # Setup test parameters
        original_path = "/path/to/test_image.jpg"
        index = 0
        
        # Test with prefix and suffix
        params = {
            "prefix": "prefix_",
            "suffix": "_suffix",
            "case_option": "preserve"
        }
        self.assertEqual(
            generate_preview_name(original_path, index, params),
            "prefix_test_image_suffix.jpg"
        )
        
        # Test with find/replace
        params = {
            "find": "test",
            "replace": "new"
        }
        self.assertEqual(
            generate_preview_name(original_path, index, params),
            "new_image.jpg"
        )
        
        # Test with case change
        params = {
            "case_option": "upper"
        }
        self.assertEqual(
            generate_preview_name(original_path, index, params),
            "TEST_IMAGE.jpg"
        )
        
        # Test with numbering
        params = {
            "use_numbering": True,
            "number_options": {
                "padding": 3,
                "start": 1,
                "step": 1,
                "position": "suffix",
                "separator": "_"
            }
        }
        self.assertEqual(
            generate_preview_name(original_path, index, params),
            "test_image_001.jpg"
        )
        
        # Test with all options
        params = {
            "prefix": "pre_",
            "suffix": "_post",
            "find": "test",
            "replace": "new",
            "case_option": "title",
            "use_numbering": True,
            "number_options": {
                "padding": 2,
                "start": 10,
                "step": 5,
                "position": "prefix",
                "separator": "-"
            }
        }
        self.assertEqual(
            generate_preview_name(original_path, index, params),
            "10-Pre_New_Image_Post.jpg"
        )


if __name__ == "__main__":
    unittest.main()
