import unittest
from converters import *
from textnode import TextNode
from leafnode import LeafNode

class TestConverter(unittest.TestCase):
    
    def test_text_to_text(self):
        node = TextNode("hello", "text")
        leaf_node = text_node_to_html_node(node)
        self.assertEqual("hello", leaf_node.to_html())

    def test_text_to_bold_text(self):
        node = TextNode("hello", "bold")
        leaf_node = text_node_to_html_node(node)
        self.assertEqual("<b>hello</b>", leaf_node.to_html())
    
    def test_text_to_italic_text(self):
        node = TextNode("hello", "italic")
        leaf_node = text_node_to_html_node(node)
        self.assertEqual("<i>hello</i>", leaf_node.to_html())
    
    def test_text_to_code_text(self):
        node = TextNode("hello", "code")
        leaf_node = text_node_to_html_node(node)
        self.assertEqual("<code>hello</code>", leaf_node.to_html())

    def test_text_to_link_text(self):
        node = TextNode("hello", "link", "http://balls.com")
        leaf_node = text_node_to_html_node(node)
        self.assertEqual("<a href=\"http://balls.com\">hello</a>", leaf_node.to_html())

    def test_text_to_link_text(self):
        node = TextNode("alt-text", "image", "http://balls.com")
        leaf_node = text_node_to_html_node(node)
        self.assertEqual("<img src=\"http://balls.com\" alt=\"alt-text\"/>", leaf_node.to_html())

    def test_no_text_provided(self):
        node = TextNode("balls", "balls")
        self.assertRaises(
            Exception,
            text_node_to_html_node,
            node
        )
        # test that the exception provides the correct message
        with self.assertRaises(Exception) as context:
            text_node_to_html_node(node)
        self.assertEqual(str(context.exception), "Invalid or unimplemented text node type")



if __name__ == "__main__":
    unittest.main()