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

    def test_split_nodes_invalid_delimiter(self):
        node = TextNode("This is invalid &text&", "boop")
        self.assertRaises(
            Exception,
            split_nodes_delimiter,
            node,
            "&",
            "boop"
        )
        with self.assertRaises(Exception) as context:
            split_nodes_delimiter(node, "&", "boop")
        self.assertEqual(str(context.exception), "Invalid markdown syntax")

    def test_split_nodes_delimiter(self):
        node1 = TextNode("This is text with a `code block` word", "text")
        new_nodes1 = split_nodes_delimiter([node1], "`", "code")
        self.assertEqual([
            TextNode("This is text with a ", "text"),
            TextNode("code block", "code"),
            TextNode(" word", "text"),
        ], new_nodes1)
        node2 = TextNode("This is text with an *italic* word", "text")
        new_nodes2 = split_nodes_delimiter([node2], "*", "italic")
        self.assertEqual([
            TextNode("This is text with an ", "text"),
            TextNode("italic", "italic"),
            TextNode(" word", "text"),
        ], new_nodes2)
        node3 = TextNode("This is text with an *italic*", "text")
        new_nodes3 = split_nodes_delimiter([node3], "*", "italic")
        self.assertEqual([
            TextNode("This is text with an ", "text"),
            TextNode("italic", "italic"),
        ], new_nodes3)
        node4 = TextNode("*italic* This is text with an", "text")
        new_nodes4 = split_nodes_delimiter([node4], "*", "italic")
        self.assertEqual([
            TextNode("italic", "italic"),
            TextNode(" This is text with an", "text"),
        ], new_nodes4)
        node5 = TextNode("This is *italic* text with an *italic* word *italic*", "text")
        new_nodes5 = split_nodes_delimiter([node5], "*", "italic")
        self.assertEqual([
            TextNode("This is ", "text"),
            TextNode("italic", "italic"),
            TextNode(" text with an ", "text"),
            TextNode("italic", "italic"),
            TextNode(" word ", "text"),
            TextNode("italic", "italic"),
        ], new_nodes5)
        node6 = TextNode("This is **bold** text with an **bold** word **bold**", "text")
        new_nodes6 = split_nodes_delimiter([node6], "**", "bold")
        self.assertEqual([
            TextNode("This is ", "text"),
            TextNode("bold", "bold"),
            TextNode(" text with an ", "text"),
            TextNode("bold", "bold"),
            TextNode(" word ", "text"),
            TextNode("bold", "bold"),
        ], new_nodes6)
        node_list = [TextNode("bold", "bold"), node6, TextNode("this is more text", "text")]
        new_nodes7 = split_nodes_delimiter(node_list, "**", "bold")
        self.assertEqual([
            TextNode("bold", "bold", None),
            TextNode("This is ", "text", None),
            TextNode("bold", "bold", None),
            TextNode(" text with an ", "text", None),
            TextNode("bold", "bold", None),
            TextNode(" word ", "text", None),
            TextNode("bold", "bold", None),
            TextNode("this is more text", "text", None)
        ], new_nodes7)

    def test_extract_markdown_images_and_links(self):
        text1 = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        extracted_text1 = extract_markdown_images(text1)
        self.assertEqual([("rick roll", "https://i.imgur.com/aKaOqIh.gif"), ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg")], extracted_text1)
        text2 = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        extracted_text2 = extract_markdown_links(text2)
        self.assertEqual([("to boot dev", "https://www.boot.dev"), ("to youtube", "https://www.youtube.com/@bootdotdev")], extracted_text2)

    def test_split_nodes_image(self):
        node = TextNode(
            "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg) and ![troll face](https://i.imgur.com/fJRm4Vk.jpeg)",
            "text",
        )
        new_nodes = split_nodes_image([node])
        self.assertEqual([
            TextNode("This is text with a ", "text", None),
            TextNode("rick roll", "image", "https://i.imgur.com/aKaOqIh.gif"),
            TextNode(" and ", "text", None),
            TextNode("obi wan", "image", "https://i.imgur.com/fJRm4Vk.jpeg"),
            TextNode(" and ", "text", None),
            TextNode("troll face", "image", "https://i.imgur.com/fJRm4Vk.jpeg")
        ], new_nodes)

    def test_split_nodes_link(self):
        node = TextNode(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)",
            "text",
        )
        new_nodes = split_nodes_link([node])
        self.assertEqual([
            TextNode("This is text with a link ", "text"),
            TextNode("to boot dev", "link", "https://www.boot.dev"),
            TextNode(" and ", "text"),
            TextNode(
                "to youtube", "link", "https://www.youtube.com/@bootdotdev"
            ),
        ], new_nodes)



if __name__ == "__main__":
    unittest.main()