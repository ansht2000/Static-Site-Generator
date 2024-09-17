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

# implementation using regexes
# def split_nodes_delimiter(old_nodes, delimiter, text_type):
#     valid_delimiters = ["**", "*", "`"]
#     if delimiter not in valid_delimiters:
#         raise Exception("Invalid markdown syntax")
#     new_nodes = []
#     for node in old_nodes:
#         node_text = node.text
#         if node.text_type != "text":
#             new_nodes.append(TextNode(node_text, node.text_type))
#             continue
#         delimited_text = re.findall(rf"\{delimiter}([^\{delimiter}]+)\{delimiter}", node_text)
#         split_text = node_text.split(delimiter)
#         nodes_to_add = map(lambda text: TextNode(text, text_type) if (text in delimited_text) else TextNode(text, "text"), split_text)
#         new_nodes.extend(nodes_to_add)
#     return new_nodes

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


        
