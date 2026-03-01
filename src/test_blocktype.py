import unittest
from markdownblocks import markdown_to_blocks
from blocktype import BlockType,block_to_block_type

class TestBlockType(unittest.TestCase):
    def test_block_to_block_type_code(self):
        md = """
```
sdfsf
	this could be {code}
```
"""
        block = ''.join(markdown_to_blocks(md))
        self.assertEqual(block_to_block_type(block), BlockType.CODE)

    def test_block_to_block_type_heading(self):
        md = """
##### this is heading text
"""
        block = ''.join(markdown_to_blocks(md))
        self.assertEqual(block_to_block_type(block), BlockType.HEADING)

    def test_block_to_block_type_quote(self):
        md = """
> this
> is
> definitely
> a
> quote!
"""
        block = ''.join(markdown_to_blocks(md))
        self.assertEqual(block_to_block_type(block), BlockType.QUOTE)
    
    def test_block_to_block_type_ul(self):
        md = """
- this be
- an unordered
- list
"""
        block = ''.join(markdown_to_blocks(md))
        self.assertEqual(block_to_block_type(block), BlockType.UNORDERED_LIST)

    def test_block_to_block_type_ol(self):
        md = """
1. this is
2. an ordered
3. list
4. because it has numbers
"""
        block = ''.join(markdown_to_blocks(md))
        self.assertEqual(block_to_block_type(block), BlockType.ORDERED_LIST)

    def test_block_to_block_type_paragraph(self):
        md = """this is just a paragraph"""
        block = ''.join(markdown_to_blocks(md))
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)