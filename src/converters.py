from textnode import TextNode
from leafnode import LeafNode
import re

def text_node_to_html_node(text_node: TextNode):
    text_type = text_node.text_type
    text = text_node.text
    url = text_node.url
    match text_type:
        case "text":
            return LeafNode(value=text)
        case "bold":
            return LeafNode(tag="b", value=text)
        case "italic":
            return LeafNode(tag="i", value=text)
        case "code":
            return LeafNode(tag="code", value=text)
        case "link":
            return LeafNode(tag="a", value=text, props={"href": url})
        case "image":
            return LeafNode(tag="img", value="", props={"src": url, "alt": text})
        case _:
            raise Exception("Invalid or unimplemented text node type")

# implementation using map and filter
def split_nodes_delimiter(old_nodes, delimiter, text_type):
    valid_delimiters = ["**", "*", "`"]
    if delimiter not in valid_delimiters:
        raise Exception("Invalid markdown syntax")
    new_nodes = []
    for node in old_nodes:
        node_text = node.text
        if node.text_type != "text":
            new_nodes.append(TextNode(node_text, node.text_type))
            continue
        split_nodes = node_text.split(delimiter)
        text_nodes = map(
                lambda x: TextNode(x, "text")
                if (split_nodes.index(x) % 2 == 0)
                else TextNode(x, text_type), split_nodes
        )
        new_nodes.extend(list(filter(lambda x: x.text != "", text_nodes)))
    return new_nodes

def extract_markdown_images(text):
    return re.findall(r"!\[(.*?)\]\((.*?)\)", text)

def extract_markdown_links(text):
    # (?<!!) is a negative lookahead epxression to exclude
    # captured exclamation marks in the returned list
    return re.findall(r"(?<!!)\[(.*?)\]\((.*?)\)", text)

def split_nodes_image(old_nodes):
    new_nodes = []
    for node in old_nodes:
        node_text = node.text
        image_list = extract_markdown_images(node_text)
        for img_tuple in image_list:
            img_text = f"![{img_tuple[0]}]({img_tuple[1]})"
            split_text = node_text.split(img_text)
            new_nodes.append(TextNode(split_text[0], "text"))
            new_nodes.append(TextNode(img_tuple[0], "image", img_tuple[1]))
            node_text = split_text[1]
    return new_nodes


def split_nodes_link(old_nodes):
    new_nodes = []
    for node in old_nodes:
        node_text = node.text
        link_list = extract_markdown_links(node_text)
        for link_tuple in link_list:
            link_text = f"[{link_tuple[0]}]({link_tuple[1]})"
            split_text = node_text.split(link_text)
            new_nodes.append(TextNode(split_text[0], "text"))
            new_nodes.append(TextNode(link_tuple[0], "link", link_tuple[1]))
            node_text = split_text[1]
    return new_nodes
        
