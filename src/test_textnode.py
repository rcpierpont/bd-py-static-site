import unittest
from textnode import TextNode,TextType,text_node_to_html
from htmlnode import LeafNode
from splitnodes import split_nodes_delimiter,split_nodes_image,split_nodes_link,text_to_text_nodes
from markdownregex import extract_markdown_links,extract_markdown_images

class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)
    
    def test_text_not_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is another text node", TextType.BOLD)
        self.assertNotEqual(node, node2)

    def test_type_not_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.ITALIC)
        self.assertNotEqual(node, node2)

    def test_url_not_eq(self):
        node = TextNode("This is a text node", TextType.BOLD, url="https://www.boot.dev")
        node2 = TextNode("This is a text node", TextType.ITALIC)
        self.assertNotEqual(node, node2)
    
    def test_node_to_html_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_to_html_italic(self):
        node = TextNode("This is in italics", TextType.ITALIC)
        html_node = text_node_to_html(node)
        self.assertEqual(html_node.tag, 'i')
        self.assertEqual(html_node.value, "This is in italics")

    def test_to_html_code(self):
        node = TextNode("This is code", TextType.CODE)
        html_node = text_node_to_html(node)
        self.assertEqual(html_node.tag, 'code')
        self.assertEqual(html_node.value, "This is code")
    
    def test_to_html_link(self):
        node = TextNode("This is a link", TextType.LINK, url='www.google.com')
        html_node = text_node_to_html(node)
        self.assertEqual(html_node.tag, 'a')
        self.assertEqual(html_node.props['href'], 'www.google.com')
        self.assertEqual(html_node.value, "This is a link")
    
    def test_to_html_image(self):
        node = TextNode("This is an image", TextType.IMAGE, url='www.google.com')
        html_node = text_node_to_html(node)
        self.assertEqual(html_node.tag, 'img')
        self.assertEqual(html_node.props['src'], 'www.google.com')
        self.assertEqual(html_node.props['alt'], "This is an image")
        self.assertEqual(html_node.value, '')
    
    def test_split_nodes_inline_italic(self):
        node = TextNode('This text has some _italic text_ in the middle.', TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], '_', TextType.ITALIC)
        self.assertEqual(new_nodes[0].text, 'This text has some ')
        self.assertEqual(new_nodes[1].text, 'italic text')
        self.assertEqual(new_nodes[2].text, ' in the middle.')
        self.assertEqual(new_nodes[0].text_type, TextType.TEXT)
        self.assertEqual(new_nodes[1].text_type, TextType.ITALIC)
        self.assertEqual(new_nodes[2].text_type, TextType.TEXT)

    def test_split_nodes_inline_bold(self):
        node = TextNode('This text has some **bold text** in the middle.', TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], '**', TextType.BOLD)
        self.assertEqual(new_nodes[0].text, 'This text has some ')
        self.assertEqual(new_nodes[1].text, 'bold text')
        self.assertEqual(new_nodes[2].text, ' in the middle.')
        self.assertEqual(new_nodes[0].text_type, TextType.TEXT)
        self.assertEqual(new_nodes[1].text_type, TextType.BOLD)
        self.assertEqual(new_nodes[2].text_type, TextType.TEXT)
    
    def test_split_nodes_single_code(self):
        node = TextNode('This text has some `code text` in the middle.', TextType.CODE)
        new_nodes = split_nodes_delimiter([node], '`', TextType.CODE)
        self.assertEqual(len(new_nodes), 1)
        self.assertEqual(new_nodes[0].text, node.text)

    def test_split_nodes_single_bold(self):
        node = TextNode('This text has some **bold text** in the middle.', TextType.CODE)
        new_nodes = split_nodes_delimiter([node], '**', TextType.CODE)
        self.assertEqual(len(new_nodes), 1)
        self.assertEqual(new_nodes[0].text, node.text)
    
    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)
    
    def test_extract_markdown_links(self):
        matches = extract_markdown_links(
            "This is text with a link [to bootdev](https://www.boot.dev)"
        )
        self.assertListEqual([('to bootdev', 'https://www.boot.dev')], matches)

    def test_extract_multiple_links(self):
        matches = extract_markdown_links(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com)"
        )
        self.assertListEqual([('to boot dev', 'https://www.boot.dev'), ('to youtube', 'https://www.youtube.com')], matches)

    def test_extract_multiple_images(self):
        matches = extract_markdown_images(
            "This is text with two images, ![image A](https://i.imgur.com/aKaOqIh.gif) and ![image B](https://i.imgur.com/fJRm4Vk.jpeg)"
        )
        self.assertListEqual([('image A', 'https://i.imgur.com/aKaOqIh.gif'), ('image B', 'https://i.imgur.com/fJRm4Vk.jpeg')], matches)
    
    def test_extract_image_and_link(self):
        text =  "This is text with a link [to bootdev](https://www.boot.dev) and an ![image](https://i.imgur.com/zjjcJKZ.png)"
        image_matches = extract_markdown_images(text)
        link_matches = extract_markdown_links(text)
        self.assertListEqual([('image', 'https://i.imgur.com/zjjcJKZ.png')], image_matches)
        self.assertListEqual([('to bootdev', 'https://www.boot.dev')], link_matches)
    
    def test_split_image_no_text(self):
        node = TextNode("image", TextType.IMAGE, url="https://i.imgur.com/zjjcJKZ.png")
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png")],new_nodes)
    
    def test_split_link_no_text(self):
        node = TextNode("link", TextType.LINK, url="https://i.imgur.com/zjjcJKZ.png")
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [TextNode("link", TextType.LINK, "https://i.imgur.com/zjjcJKZ.png")],new_nodes)

    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode("second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )
    
    def test_split_links(self):
        node = TextNode(
            "This is text with [a link](https://i.imgur.com/zjjcJKZ.png) and [another link](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with ", TextType.TEXT),
                TextNode("a link", TextType.LINK, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and ", TextType.TEXT),
                TextNode("another link", TextType.LINK, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )
    
    def test_text_to_text_nodes(self):
        new_nodes = text_to_text_nodes("This is **bold text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)")
        self.assertListEqual(new_nodes, [
            TextNode("This is ", TextType.TEXT), 
            TextNode("bold text", TextType.BOLD), 
            TextNode(" with an ", TextType.TEXT), 
            TextNode("italic", TextType.ITALIC), 
            TextNode(" word and a ", TextType.TEXT), 
            TextNode("code block", TextType.CODE), 
            TextNode(" and an ", TextType.TEXT),
            TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
            TextNode(" and a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://boot.dev")]
            )
if __name__ == "__main__":
    unittest.main()