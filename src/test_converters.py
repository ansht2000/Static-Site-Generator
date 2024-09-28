import unittest
from converters import *
from textnode import (
    TextNode,
    text_type_text,
    text_type_bold,
    text_type_italic,
    text_type_code,
    text_type_link,
    text_type_image,
)
from converters import (
    block_type_paragraph,
    block_type_heading,
    block_type_code,
    block_type_quote,
    block_type_unordered_list,
    block_type_ordered_list,
)
from htmlnode import HTMLNode

class TestConverter(unittest.TestCase):
    
    def test_text_to_text(self):
        node = TextNode("hello", text_type_text)
        leaf_node = text_node_to_html_node(node)
        self.assertEqual("hello", leaf_node.to_html())

    def test_text_to_bold_text(self):
        node = TextNode("hello", text_type_bold)
        leaf_node = text_node_to_html_node(node)
        self.assertEqual("<b>hello</b>", leaf_node.to_html())
    
    def test_text_to_italic_text(self):
        node = TextNode("hello", text_type_italic)
        leaf_node = text_node_to_html_node(node)
        self.assertEqual("<i>hello</i>", leaf_node.to_html())
    
    def test_text_to_code_text(self):
        node = TextNode("hello", text_type_code)
        leaf_node = text_node_to_html_node(node)
        self.assertEqual("<code>hello</code>", leaf_node.to_html())

    def test_text_to_link_text(self):
        node = TextNode("hello", text_type_link, "http://balls.com")
        leaf_node = text_node_to_html_node(node)
        self.assertEqual("<a href=\"http://balls.com\">hello</a>", leaf_node.to_html())

    def test_text_to_link_text(self):
        node = TextNode("alt-text", text_type_image, "http://balls.com")
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
        node1 = TextNode("This is text with a `code block` word", text_type_text)
        new_nodes1 = split_nodes_delimiter([node1], "`", text_type_code)
        self.assertEqual([
            TextNode("This is text with a ", text_type_text),
            TextNode("code block", text_type_code),
            TextNode(" word", text_type_text),
        ], new_nodes1)
        node2 = TextNode("This is text with an *italic* word", text_type_text)
        new_nodes2 = split_nodes_delimiter([node2], "*", text_type_italic)
        self.assertEqual([
            TextNode("This is text with an ", text_type_text),
            TextNode("italic", text_type_italic),
            TextNode(" word", text_type_text),
        ], new_nodes2)
        node3 = TextNode("This is text with an *italic*", text_type_text)
        new_nodes3 = split_nodes_delimiter([node3], "*", text_type_italic)
        self.assertEqual([
            TextNode("This is text with an ", text_type_text),
            TextNode("italic", text_type_italic),
        ], new_nodes3)
        node4 = TextNode("*italic* This is text with an", text_type_text)
        new_nodes4 = split_nodes_delimiter([node4], "*", text_type_italic)
        self.assertEqual([
            TextNode("italic", text_type_italic),
            TextNode(" This is text with an", text_type_text),
        ], new_nodes4)
        node5 = TextNode("This is *italic* text with an *italic* word *italic*", text_type_text)
        new_nodes5 = split_nodes_delimiter([node5], "*", text_type_italic)
        self.assertEqual([
            TextNode("This is ", text_type_text),
            TextNode("italic", text_type_italic),
            TextNode(" text with an ", text_type_text),
            TextNode("italic", text_type_italic),
            TextNode(" word ", text_type_text),
            TextNode("italic", text_type_italic),
        ], new_nodes5)
        node6 = TextNode("This is **bold** text with an **bold** word **bold**", text_type_text)
        new_nodes6 = split_nodes_delimiter([node6], "**", text_type_bold)
        self.assertEqual([
            TextNode("This is ", text_type_text),
            TextNode("bold", text_type_bold),
            TextNode(" text with an ", text_type_text),
            TextNode("bold", text_type_bold),
            TextNode(" word ", text_type_text),
            TextNode("bold", text_type_bold),
        ], new_nodes6)
        node_list = [TextNode("bold", text_type_bold), node6, TextNode("this is more text", text_type_text)]
        new_nodes7 = split_nodes_delimiter(node_list, "**", text_type_bold)
        self.assertEqual([
            TextNode("bold", text_type_bold, None),
            TextNode("This is ", text_type_text, None),
            TextNode("bold", text_type_bold, None),
            TextNode(" text with an ", text_type_text, None),
            TextNode("bold", text_type_bold, None),
            TextNode(" word ", text_type_text, None),
            TextNode("bold", text_type_bold, None),
            TextNode("this is more text", text_type_text, None)
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
            text_type_text,
        )
        new_nodes = split_nodes_image_link([node], text_type_image)
        self.assertEqual([
            TextNode("This is text with a ", text_type_text, None),
            TextNode("rick roll", text_type_image, "https://i.imgur.com/aKaOqIh.gif"),
            TextNode(" and ", text_type_text, None),
            TextNode("obi wan", text_type_image, "https://i.imgur.com/fJRm4Vk.jpeg"),
            TextNode(" and ", text_type_text, None),
            TextNode("troll face", text_type_image, "https://i.imgur.com/fJRm4Vk.jpeg")
        ], new_nodes)

    def test_split_nodes_link(self):
        node = TextNode(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)",
            text_type_text,
        )
        new_nodes = split_nodes_image_link([node], text_type_link)
        self.assertEqual([
            TextNode("This is text with a link ", text_type_text),
            TextNode("to boot dev", text_type_link, "https://www.boot.dev"),
            TextNode(" and ", text_type_text),
            TextNode(
                "to youtube", text_type_link, "https://www.youtube.com/@bootdotdev"
            ),
        ], new_nodes)

    def test_text_to_textnodes(self):
        text = "This is **text** with an *italic* word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        nodes = text_to_textnodes(text)
        self.assertEqual([
            TextNode("This is ", text_type_text),
            TextNode("text", text_type_bold),
            TextNode(" with an ", text_type_text),
            TextNode("italic", text_type_italic),
            TextNode(" word and a ", text_type_text),
            TextNode("code block", text_type_code),
            TextNode(" and an ", text_type_text),
            TextNode("obi wan image", text_type_image, "https://i.imgur.com/fJRm4Vk.jpeg"),
            TextNode(" and a ", text_type_text),
            TextNode("link", text_type_link, "https://boot.dev"),
        ], nodes)

    def test_markdown_to_blocks(self):
        markdown = """# This is a heading

                        This is a paragraph of text. It has some **bold** and *italic* words inside of it.

                        * This is the first list item in a list block
                        * This is a list item
                        * This is another list item"""
        block_list = markdown_to_blocks(markdown)
        self.assertEqual([
            "# This is a heading",
            "This is a paragraph of text. It has some **bold** and *italic* words inside of it.",
            "* This is the first list item in a list block\n* This is a list item\n* This is another list item"
            ], block_list)
        markdown2 = """# This is a heading
                       # with two lines in it

                        This is a paragraph of text. It has some **bold** and *italic* words inside of it.
                        This paragraph has two lines.
                        Three lines even!



                        * This is the first list item in a list block
                        * This is a list item
                        * This is another list item
                        * This is another list item"""
        block_list2 = markdown_to_blocks(markdown2)
        self.assertEqual([
            "# This is a heading\n# with two lines in it",
            "This is a paragraph of text. It has some **bold** and *italic* words inside of it.\nThis paragraph has two lines.\nThree lines even!",
            "* This is the first list item in a list block\n* This is a list item\n* This is another list item\n* This is another list item"
        ], block_list2)
        markdown3 = """# This is a heading

                        This is a paragraph of text. It has some **bold** and *italic* words inside of it.
                        This paragraph has two lines.
                        Three lines even!



                        * This is the first list item in a list block
                        * This is a list item
                        * This is another list item
                        * This is another list item
                        
                        ```
                        func main(){
                            print("hello")
                        }
                        ```"""
        block_list3 = markdown_to_blocks(markdown3)

    def test_block_to_block_type_heading(self):
        block = "Heading"
        block_type = block_to_block_type(block)
        self.assertEqual(block_type_paragraph, block_type)
        block = "# Heading"
        block_type = block_to_block_type(block)
        self.assertEqual(block_type_heading, block_type)
        block = "## Heading"
        block_type = block_to_block_type(block)
        self.assertEqual(block_type_heading, block_type)
        block = "### Heading"
        block_type = block_to_block_type(block)
        self.assertEqual(block_type_heading, block_type)
        block = "#### Heading"
        block_type = block_to_block_type(block)
        self.assertEqual(block_type_heading, block_type)
        block = "##### Heading"
        block_type = block_to_block_type(block)
        self.assertEqual(block_type_heading, block_type)
        block = "###### Heading"
        block_type = block_to_block_type(block)
        self.assertEqual(block_type_heading, block_type)
        block = "####### Heading"
        block_type = block_to_block_type(block)
        self.assertEqual(block_type_paragraph, block_type)
        block = "#######Heading"
        block_type = block_to_block_type(block)
        self.assertEqual(block_type_paragraph, block_type)
    
    def test_block_to_block_type_code(self):
        block = "```code```"
        block_type = block_to_block_type(block)
        self.assertEqual(block_type_code, block_type)
        block = "`code`"
        block_type = block_to_block_type(block)
        self.assertEqual(block_type_paragraph, block_type)
        block = "``code``"
        block_type = block_to_block_type(block)
        self.assertEqual(block_type_paragraph, block_type)
        block = "code"
        block_type = block_to_block_type(block)
        self.assertEqual(block_type_paragraph, block_type)
        block = "```code\nmore code```"
        block_type = block_to_block_type(block)
        self.assertEqual(block_type_code, block_type)

    def test_block_to_block_type_code(self):
        block = ">quote"
        block_type = block_to_block_type(block)
        self.assertEqual(block_type_quote, block_type)
        block = "> quote"
        block_type = block_to_block_type(block)
        self.assertEqual(block_type_quote, block_type)
        block = ">"
        block_type = block_to_block_type(block)
        self.assertEqual(block_type_quote, block_type)
        block = "> #quote"
        block_type = block_to_block_type(block)
        self.assertEqual(block_type_quote, block_type)
        block = "quote"
        block_type = block_to_block_type(block)
        self.assertEqual(block_type_paragraph, block_type)
        block = "> quote\n> more quote\n> even more quote\n>man this is a long quote"
        block_type = block_to_block_type(block)
        self.assertEqual(block_type_quote, block_type)

    def test_block_to_block_type_unordered_list(self):
        block = "* This is the first list item in a list block\n* This is a list item\n* This is another list item"
        block_type = block_to_block_type(block)
        self.assertEqual(block_type_unordered_list, block_type)
        block = "* This is the first list item in a list block\n* This is a list item\n* This is another list item\n* This is another list item"
        block_type = block_to_block_type(block)
        self.assertEqual(block_type_unordered_list, block_type)
        block = "random text"
        block_type = block_to_block_type(block)
        self.assertEqual(block_type_paragraph, block_type)

    def test_block_to_block_type_ordered_list(self):
        block = "1. first item\n2. second item\n3. third item"
        block_type = block_to_block_type(block)
        self.assertEqual(block_type_ordered_list, block_type)
        block = "1. first item\n2. second item\n4. fourth item"
        block_type = block_to_block_type(block)
        self.assertEqual(block_type_paragraph, block_type)
        block = "2. first item\n3. second item\n4. fourth item"
        block_type = block_to_block_type(block)
        self.assertEqual(block_type_paragraph, block_type)
        block = "1. first item\n2. second item\n3. third item\n4. fourth item\n5. fifth item\n6. sixth item\n7. seventh item\n8. eighth item\n9. ninth item\n10. tenth item\n11. eleventh item"
        block_type = block_to_block_type(block)
        self.assertEqual(block_type_ordered_list, block_type)

    def test_markdown_to_html_node(self):
        markdown = """# This is a heading

                      ## This is a subheading

                        This is a paragraph of text. It has some **bold** and *italic* words inside of it.

                        * This is the first list item in a list block
                        * This is a list item
                        * This is another list item

                        1. This is an ordered list with an *italic* word
                        2. this is another item in the list which has an ![image](https://boot.dev)
                        3. this is the last item in the list

                        > ### Trying to make a quote with a heading
                        > This is a quote with a **bold** word
                        >This is another part of the quote wich a link [boot.dev](https://boot.dev)
                        > This is the last part of the quote

                        ```
                        func main() {
                            print("hello")
                        }
                        ```"""
        html_node = markdown_to_html_node(markdown)

    

if __name__ == "__main__":
    unittest.main()