import unittest
from markdownblocks import markdown_to_html_node

class TestMarkdownToHTML(unittest.TestCase):
    def test_paragraphs(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )
    
    def test_codeblock(self):
        md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )
    
    def test_heading_plain(self):
        md = """
#### THIS IS A HEADING WITH NORMAL TEXT
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h4>THIS IS A HEADING WITH NORMAL TEXT</h4></div>"
        )

    def test_heading_inline(self):
        md = """
#### THIS IS A HEADING WITH **BOLD TEXT**
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h4>THIS IS A HEADING WITH <b>BOLD TEXT</b></h4></div>"
        )
    
    def test_unordered_list(self):
        md = """
- this is
- an unordered
- list
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ul><li>this is</li><li>an unordered</li><li>list</li></ul></div>"
        )
    
    def test_unordered_list_italics(self):
        md = """
- this is
- an _italicized_ unordered
- list
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ul><li>this is</li><li>an <i>italicized</i> unordered</li><li>list</li></ul></div>"
        )

    def test_ordered_list(self):
        md = """
1. this is
2. an ordered
3. list
4. with some _italics_
5. because it has numbers
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ol><li>this is</li><li>an ordered</li><li>list</li><li>with some <i>italics</i></li><li>because it has numbers</li></ol></div>"
        )
    def test_quote(self):
        md = """
> This is **bolded text**
> that is within
> a quote block
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><blockquote>This is <b>bolded text</b> that is within a quote block</blockquote></div>",
        )