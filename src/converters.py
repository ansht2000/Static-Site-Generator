from leafnode import LeafNode
from parentnode import ParentNode
import re
import os
import shutil
from pathlib import Path
from textnode import (
    TextNode,
    text_type_text,
    text_type_bold,
    text_type_italic,
    text_type_code,
    text_type_link,
    text_type_image,
)

block_type_paragraph = "paragraph"
block_type_heading = "heading"
block_type_code = "code"
block_type_quote = "quote"
block_type_unordered_list = "unordered_list"
block_type_ordered_list = "ordered_list"

def copy_content(src_dir_path, dest_dir_path):
    if not os.path.exists(dest_dir_path):
        os.mkdir(dest_dir_path)
    for filename in os.listdir(src_dir_path):
        from_path = os.path.join(src_dir_path, filename)
        to_path = os.path.join(dest_dir_path, filename)
        print(f" * {from_path} -> {to_path}")
        if os.path.isfile(from_path):
            shutil.copy(from_path, to_path)
        else:
            copy_content(from_path, to_path)

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    for filename in os.listdir(dir_path_content):
        from_path = os.path.join(dir_path_content, filename)
        dest_path = os.path.join(dest_dir_path, filename)
        if os.path.isfile(from_path):
            dest_path = Path(dest_path).with_suffix(".html")
            generate_page(from_path, template_path, dest_path)
        else:
            generate_pages_recursive(from_path, template_path, dest_path)


def generate_page(from_path, template_path, dest_path):
    print(f" * {from_path} {template_path} -> {dest_path}")
    from_file = open(from_path, "r")
    markdown_content = from_file.read()
    from_file.close()

    template_file = open(template_path, "r")
    template = template_file.read()
    template_file.close()

    node = markdown_to_html_node(markdown_content)
    html = node.to_html()

    title = extract_title_markdown(markdown_content)
    template = template.replace("{{ Title }}", title)
    template = template.replace("{{ Content }}", html)

    dest_dir_path = os.path.dirname(dest_path)
    if dest_dir_path != "":
        os.makedirs(dest_dir_path, exist_ok=True)
    to_file = open(dest_path, "w")
    to_file.write(template)

def extract_title_markdown(markdown):
    header_one = re.findall(r"# (.*)", markdown)
    if len(header_one) == 0:
        raise Exception("Markdown file must have at least one top level header")
    return header_one[0]

def extract_markdown_images(text):
    return re.findall(r"!\[(.*?)\]\((.*?)\)", text)

def extract_markdown_links(text):
    # (?<!!) is a negative lookbehind epxression to exclude
    # captured exclamation marks in the returned list
    return re.findall(r"(?<!!)\[(.*?)\]\((.*?)\)", text)

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
    code_match = re.fullmatch(r"(?s)^```.*```$", block)
    quote_match = re.fullmatch(r"^(?:>.*\n)*(?:>.*)", block)
    unordered_list_match = re.fullmatch(r"^(?:[*-] .*\n)*(?:[*-] .*)$", block)
    ordered_list_match = check_indices_ordered_list(re.findall(r"(\d+)\. .*\n*", block))
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
    
def text_to_children(text):
    child_nodes = []
    text_nodes = text_to_textnodes(text)
    for node in text_nodes:
        child_nodes.append(text_node_to_html_node(node))
    return child_nodes

def ulist_to_html_node(block):
    list_items = re.findall(r"(?:[*-] (.*)\n*)", block)
    list_nodes = []
    for item in list_items:
        child_nodes = text_to_children(item)
        list_nodes.append(ParentNode(tag="li", children=child_nodes))
    return ParentNode(tag="ul", children=list_nodes)

def olist_to_html_node(block):
    list_items = re.findall(r"(?:\d+\. (.*)\n*)", block)
    list_nodes = []
    for item in list_items:
        child_nodes = text_to_children(item)
        list_nodes.append(ParentNode(tag="li", children=child_nodes))
    return ParentNode(tag="ol", children=list_nodes)

def quote_to_html_node(block):
    quote_items = re.findall(r"(?:>(.*)\n*)", block)
    quote_items = list(map(lambda x: x.strip(), quote_items))
    quote_nodes = []
    for item in quote_items:
        child_nodes = text_to_children(item)
        quote_nodes.append(ParentNode(tag="p", children=child_nodes))
    return ParentNode(tag="blockquote", children=quote_nodes)

def code_to_html_node(block):
    code_items = re.findall(r"(?s)```(.*)```", block)
    child_nodes = text_to_children(code_items[0])
    code_nodes = ParentNode(tag="code", children=child_nodes)
    return ParentNode("pre", [code_nodes])

def heading_to_html_node(block):
    heading_items = re.findall(r"#{1,6} .*", block)
    level = 0
    text = heading_items[0]
    for char in text:
        if char == "#":
            level += 1
        else:
            break
    text = heading_items[0][level + 1:]
    child_nodes = text_to_children(text)
    return ParentNode(tag=f"h{level}", children=child_nodes)

def paragraph_to_html_node(block):
    lines = block.split("\n")
    paragraph = " ".join(lines)
    child_nodes = text_to_children(paragraph)
    return ParentNode("p", children=child_nodes)
    
def markdown_to_html_node(markdown):
    block_list = markdown_to_blocks(markdown)
    block_nodes = []
    for block in block_list:
        block_type = block_to_block_type(block)
        if block_type == block_type_unordered_list:
            html_node = ulist_to_html_node(block)
            block_nodes.append(html_node)
        elif block_type == block_type_ordered_list:
            html_node = olist_to_html_node(block)
            block_nodes.append(html_node)
        elif block_type == block_type_quote:
            html_node = quote_to_html_node(block)
            block_nodes.append(html_node)
        elif block_type == block_type_code:
            html_node = code_to_html_node(block)
            block_nodes.append(html_node)
        elif block_type == block_type_heading:
            html_node = heading_to_html_node(block)
            block_nodes.append(html_node)
        elif block_type == block_type_paragraph:
            html_node = paragraph_to_html_node(block)
            block_nodes.append(html_node)
        else:
            raise ValueError("Invalid mardown block type")
    return ParentNode(tag="div", children=block_nodes)
            
