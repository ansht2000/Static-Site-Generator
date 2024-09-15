import unittest
from htmlnode import HTMLNode

class TestHTMLNode(unittest.TestCase):

    def test_eq(self):
        node = HTMLNode("<p>", "Hello", ["hello"], {"test": "testing"})
        node2 = HTMLNode("<p>", "Hello", ["hello"], {"test": "testing"})
        self.assertEqual(node, node2)

    def test_not_eq(self):
        node = HTMLNode("<p>", "Hello", ["hello"], {"test": "testing"})
        node2 = HTMLNode("<p>", "Hello!", ["hello"], {"test": "testing"})
        node3 = HTMLNode("<p>", "Hello!", ["hello", "goodbye"], {"test": "testing"})
        node4 = HTMLNode("<p>", "Hello!", ["hello"], {"test": "testing", "testing": "one two three"})
        node5 = HTMLNode("<h1>", "Hello", ["hello"], {"test": "testing"})
        self.assertNotEqual(node, node2)
        self.assertNotEqual(node, node3)
        self.assertNotEqual(node, node4)
        self.assertNotEqual(node, node5)

    def test_repr(self):
        node = HTMLNode("<p>", "Hello", ["hello"], {"test": "testing"})
        self.assertEqual("HTMLNode(<p>, Hello, ['hello'], {'test': 'testing'})", node.__repr__())

    def test_props_to_html(self):
        node = HTMLNode("<p>", "Hello", ["hello"], {"test": "testing"})
        self.assertEqual(" test=\"testing\"", node.props_to_html())
        node2 = HTMLNode("<p>", "Hello!", ["hello"], {"test": "testing", "testing": "one two three"})
        self.assertEqual(" test=\"testing\" testing=\"one two three\"", node2.props_to_html())

    def test_to_html(self):
        pass

if __name__ == "__main__":
    unittest.main()
