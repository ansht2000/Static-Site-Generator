import unittest
from parentnode import ParentNode
from leafnode import LeafNode

class TestParentNode(unittest.TestCase):

    def test_init_no_children(self):
        self.assertRaises(
            ValueError,
            ParentNode,
            tag="a", props={"href": "balls"}
        )
        with self.assertRaises(ValueError) as context:
            ParentNode(tag="a", props={"href": "balls"})
        self.assertEqual(str(context.exception), "Children must be provided for a parent node")

    def test_init_with_value(self):
        self.assertRaises(
            TypeError,
            ParentNode,
            tag="a", props={"href": "balls"}, value="balls"
        )
    
    def test_to_html(self):
        node = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )
        html_string = node.to_html()
        self.assertEqual("<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>", html_string)
        node2 = ParentNode(
            "p",
            [
                ParentNode(
                    "p",
                    [
                        LeafNode("b", "Bold text"),
                        LeafNode(None, "Normal text"),
                        LeafNode("i", "italic text"),
                        LeafNode(None, "Normal text"),
                    ]
                ),
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )
        html_string2 = node2.to_html()
        self.assertEqual(
            "<p><p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>",
            html_string2
        )
        node3 = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
            {"href": "balls"}
        )
        html_string3 = node3.to_html()
        self.assertEqual("<p href=\"balls\"><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>", html_string3)
        node4 = ParentNode(
            "p",
            [
                ParentNode(
                    "p",
                    [
                        LeafNode("b", "Bold text"),
                        LeafNode(None, "Normal text"),
                        LeafNode("i", "italic text"),
                        LeafNode(None, "Normal text"),
                    ]
                ),
                ParentNode(
                    "p",
                    [
                        LeafNode("b", "Bold text"),
                        LeafNode(None, "Normal text"),
                        LeafNode("i", "italic text"),
                        LeafNode(None, "Normal text"),
                    ]
                )
            ],
        )
        html_string4 = node4.to_html()
        self.assertEqual(
                "<p><p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p><p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p></p>",
                html_string4
            )

if __name__ == "__main__":
    unittest.main()