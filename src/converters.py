from textnode import (
    TextNode,
    text_type_text,
    text_type_bold,
    text_type_italic,
    text_type_code,
    text_type_link,
    text_type_image,
)
from leafnode import LeafNode
import re

block_type_paragraph = "paragraph"
block_type_heading = "heading"
block_type_code = "code"
block_type_quote = "quote"
block_type_unordered_list = "unordered_list"
block_type_ordered_list = "ordered_list"

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

        if node.text_type != text_type_text:
            new_nodes.append(TextNode(node_text, node.text_type))
            continue
        split_nodes = node_text.split(delimiter)
        text_nodes = map(
                lambda x: TextNode(x, text_type_text)
                if (split_nodes.index(x) % 2 == 0)
                else TextNode(x, text_type), split_nodes
        )
        new_nodes.extend(list(filter(lambda x: x.text != "", text_nodes)))
    return new_nodes

def extract_markdown_images(text):
    return re.findall(r"!\[(.*?)\]\((.*?)\)", text)

def extract_markdown_links(text):
    # (?<!!) is a negative lookbehind epxression to exclude
    # captured exclamation marks in the returned list
    return re.findall(r"(?<!!)\[(.*?)\]\((.*?)\)", text)

def split_nodes_image_link(old_nodes, type):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != text_type_text:
            new_nodes.append(node)
            continue
        node_text = node.text
        extracted_list = []
        match type:
            case "image":
                extracted_list = extract_markdown_images(node_text)
            case "link":
                extracted_list = extract_markdown_links(node_text)
        if len(extracted_list) == 0:
            new_nodes.append(node)
            continue
        for extracted_tuple in extracted_list:
            match type:
                case "image":
                    extracted_text = f"![{extracted_tuple[0]}]({extracted_tuple[1]})"
                case "link":
                    extracted_text = f"[{extracted_tuple[0]}]({extracted_tuple[1]})"
            split_text = node_text.split(extracted_text)
            if len(split_text) != 2:
                raise Exception("Invalid markdown, link section not closed")
            if split_text[0] != "":
                new_nodes.append(TextNode(split_text[0], text_type_text))
            new_nodes.append(TextNode(extracted_tuple[0], type, extracted_tuple[1]))
            node_text = split_text[1]
        if node_text != "":
            new_nodes.append(TextNode(node_text, text_type_text))
    return new_nodes

def text_to_textnodes(text):
    node = [TextNode(text, text_type_text)]
    new_nodes = split_nodes_delimiter(node, "**", text_type_bold)
    new_nodes = split_nodes_delimiter(new_nodes, "*", text_type_italic)
    new_nodes = split_nodes_delimiter(new_nodes, "`", text_type_code)
    new_nodes = split_nodes_image_link(new_nodes, text_type_image)
    new_nodes = split_nodes_image_link(new_nodes, text_type_link)
    return new_nodes

def markdown_to_blocks(markdown):
    block_list = list(map(lambda x: "\n".join(list(map(lambda y: y.strip(), x.split("\n")))), markdown.split("\n\n")))
    return list(filter(lambda x: x != "", block_list))

def check_indices_ordered_list(matches):
    if len(matches) == 0:
        return False
    count = 1
    for match in matches:
        if int(match) == count:
            count += 1
            continue
        else:
            return False
    return True

def block_to_block_type(block):
    heading_match = re.fullmatch(r"^#{1,6} .*", block)
    code_match = re.fullmatch(r"^```.*```$", block)
    quote_match = re.fullmatch(r"^(?:>.*\n)*(?:>.*)", block)
    unordered_list_match = re.fullmatch(r"^(?:[*-] .*\n)*(?:[*-] .*)$", block)
    ordered_list_match = check_indices_ordered_list(re.findall(r"(\d+). .*\n*", block))
    if heading_match:
        return block_type_heading
    elif code_match:
        return block_type_code
    elif quote_match:
        return block_type_quote
    elif unordered_list_match:
        return block_type_unordered_list
    elif ordered_list_match:
        return block_type_ordered_list
    else:
        return block_type_paragraph
    
def markdown_to_html_node(markdown):
    pass
    