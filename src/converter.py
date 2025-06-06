import re
from htmlnode import LeafNode
from textnode import TextNode, TextType

def text_node_to_html_node(text_node):
    if not isinstance(text_node, TextNode):
        raise ValueError("Input must be a TextNode")
    
    if text_node.text_type == TextType.TEXT:
        return LeafNode(tag=None, value=text_node.text)
    elif text_node.text_type == TextType.BOLD:
        return LeafNode(tag="b", value=text_node.text)
    elif text_node.text_type == TextType.ITALIC:
        return LeafNode(tag="i", value=text_node.text)
    elif text_node.text_type == TextType.CODE:
        return LeafNode(tag="code", value=text_node.text)
    elif text_node.text_type == TextType.LINK:
        if text_node.url is None:
            raise ValueError("Link TextNode must have a URL")
        return LeafNode(tag="a", value=text_node.text, props={"href": text_node.url})
    elif text_node.text_type == TextType.IMAGE:
        if text_node.url is None:
            raise ValueError("Image TextNode must have a URL")
        return LeafNode(tag="img", value="", props={"src": text_node.url, "alt": text_node.text})
    else:
        raise ValueError(f"Unsupported TextType: {text_node.text_type}")

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []

    for node in old_nodes:
        if not isinstance(node, TextNode):
            new_nodes.append(node)
            continue
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        # split the text by the delimiter
        parts = node.text.split(delimiter)

        # if the number of parts is even, it means a closing delimiter is missing
        if len(parts) % 2 == 0:
            raise ValueError(f"Invalid Markdown syntax: missing closing delimiter '{delimiter}' in text: {node.text}")

        # process the parts, alternating between TEXT and the specified text_type
        for i, part in enumerate(parts):
            if not part:
                continue
            if i % 2 == 0:
                # even-indexed parts are outside delimiters (TEXT)
                new_nodes.append(TextNode(part, TextType.TEXT))
            else:
                # odd-indexed parts are inside delimiters (specified text_type)
                new_nodes.append(TextNode(part, text_type))

    return new_nodes

def extract_markdown_images(text):
    pattern = r"!\[([^\[\]]*)\]\(([^\(\)]*)\)"
    matches = re.findall(pattern, text)
    return [(alt_text, url) for alt_text, url in matches]

def extract_markdown_links(text):
    pattern = r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)"
    matches = re.findall(pattern, text)
    return [(anchor_text, url) for anchor_text, url in matches]
