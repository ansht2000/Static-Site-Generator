import unittest
from leafnode import LeafNode

class TestLeafNode(unittest.TestCase):

    def test_init_no_value(self):
        # test that the exception is raised
        self.assertRaises(
            ValueError,
            LeafNode,
            tag="a", props={"href": "balls"}
        )
        # test that the exception provides the correct message
        with self.assertRaises(ValueError) as context:
            LeafNode(tag="a", props={"href": "balls"})
        self.assertEqual(str(context.exception), "Value must be provided for a leaf node")

    def test_to_html(self):
        node = LeafNode(tag="p", value="Hello")
        html_string = node.to_html()
        self.assertEqual("<p>Hello</p>", html_string)
        node2 = LeafNode(tag="a", value="Click me!", props={"href": "https://www.google.com"})
        html_string2 = node2.to_html()
        self.assertEqual("<a href=\"https://www.google.com\">Click me!</a>", html_string2)
        node3 = LeafNode(value="hello")
        html_string3 = node3.to_html()
        self.assertEqual("hello", html_string3)
        node4 = LeafNode("p", "This is a paragraph of text.")
        html_string4 = node4.to_html()
        self.assertEqual("<p>This is a paragraph of text.</p>", html_string4)
    

if __name__ == "__main__":
    unittest.main()