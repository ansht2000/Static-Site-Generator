import unittest
from textnode import (
    TextNode,
    text_type_text,
    text_type_bold,
    text_type_italic,
    text_type_code,
    text_type_link,
    text_type_image,
)

class TestTextNode(unittest.TestCase):
    
    def test_eq(self):
        node = TextNode("This is a text node", text_type_bold)
        node2 = TextNode("This is a text node", text_type_bold)
        self.assertEqual(node, node2)
    
    def test_not_eq(self):
        node = TextNode("This is a text node", text_type_bold)
        node2 = TextNode("This is a different text node", text_type_bold)
        self.assertNotEqual(node, node2)

    def test_text_type_eq(self):
        node = TextNode("This is a text node", text_type_bold)
        node2 = TextNode("This is a text node", text_type_bold)
        self.assertEqual(node, node2)

    def test_text_type_not_eq(self):
        node = TextNode("This is a text node", text_type_italic)
        node2 = TextNode("This is a text node", text_type_bold)
        self.assertNotEqual(node, node2)
    
    def test_null_url_not_eq(self):
        node = TextNode("This is a text node", text_type_bold, "https://www.youtube.com")
        node2 = TextNode("This is a text node", text_type_bold)
        self.assertNotEqual(node, node2)

    def test_unpassed_url_is_none(self):
        node = TextNode("This is a text node", text_type_bold)
        self.assertEqual(node.url, None)

    def test_passed_url_is_not_none(self):
        node = TextNode("This is a text node", text_type_bold, "https://www.youtube.com")
        self.assertNotEqual(node.url, None)
        self.assertEqual(node.url, "https://www.youtube.com")

if __name__ == "__main__":
    unittest.main()