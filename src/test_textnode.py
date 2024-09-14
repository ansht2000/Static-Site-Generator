import unittest
from textnode import TextNode

class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", "bold")
        node2 = TextNode("This is a text node", "bold")
        self.assertEqual(node, node2)
    
    def test_not_eq(self):
        node = TextNode("This is a text node", "bold")
        node2 = TextNode("This is a different text node", "bold")
        self.assertNotEqual(node, node2)

    def test_text_type_eq(self):
        node = TextNode("This is a text node", "bold")
        node2 = TextNode("This is a text node", "bold")
        self.assertEqual(node, node2)

    def test_text_type_not_eq(self):
        node = TextNode("This is a text node", "italic")
        node2 = TextNode("This is a text node", "bold")
        self.assertNotEqual(node, node2)
    
    def test_null_url_not_eq(self):
        node = TextNode("This is a text node", "bold", "https://www.youtube.com")
        node2 = TextNode("This is a text node", "bold")
        self.assertNotEqual(node, node2)

    def test_unpassed_url_is_none(self):
        node = TextNode("This is a text node", "bold")
        self.assertEqual(node.url, None)

    def test_passed_url_is_not_none(self):
        node = TextNode("This is a text node", "bold", "https://www.youtube.com")
        self.assertNotEqual(node.url, None)
        self.assertEqual(node.url, "https://www.youtube.com")

if __name__ == "__main__":
    unittest.main()