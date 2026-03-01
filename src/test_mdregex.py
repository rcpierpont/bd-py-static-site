import unittest
from markdownregex import extract_title

class TestMarkdownRegex(unittest.TestCase):
    def test_extract_title_simple(self):
        md = """
# Hello this is a title
"""
        title = extract_title(md)
        self.assertEqual(title, "Hello this is a title")
        
    def test_extract_title_beginning(self):
        md = """
# Hello this is a title

this is NOT a title
"""
        title = extract_title(md)
        self.assertEqual(title, "Hello this is a title")

    def test_extract_title_middle(self):
        md = """
#this is not a title

### this is also NOT a title

# Hello this is a title
"""
        title = extract_title(md)
        self.assertEqual(title, "Hello this is a title")