"""
Module for parsing markdown inline elements (bold text, italic, code, links, images).
"""

import re
from src.nodes import TextNode, TextType


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    """
    Splits TextNode by specified delimiter, creating new nodes with specified type.
    
    Args:
        old_nodes: list of nodes to process
        delimiter: delimiter to search for (e.g., "**" for bold text)
        text_type: text type for content between delimiters
        
    Returns:
        list: new list of nodes with split content
        
    Raises:
        ValueError: if closing delimiter is missing
    """
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
    """
    Extracts images from markdown text.
    
    Args:
        text: string with markdown text
        
    Returns:
        list: list of tuples (alt_text, url) for each found image
    """
    pattern = r"!\[([^\[\]]*)\]\(([^\(\)]*)\)"
    matches = re.findall(pattern, text)
    return [(alt_text, url) for alt_text, url in matches]


def extract_markdown_links(text):
    """
    Extracts links from markdown text.
    
    Args:
        text: string with markdown text
        
    Returns:
        list: list of tuples (anchor_text, url) for each found link
    """
    pattern = r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)"
    matches = re.findall(pattern, text)
    return [(anchor_text, url) for anchor_text, url in matches]


def split_nodes_image(old_nodes):
    """
    Splits TextNode containing images into separate nodes.
    
    Args:
        old_nodes: list of nodes to process
        
    Returns:
        list: new list of nodes with extracted images
    """
    new_nodes = []
    for node in old_nodes:
        if not isinstance(node, TextNode) or node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        if not node.text:
            continue

        # extract images from the text
        images = extract_markdown_images(node.text)
        if not images:
            new_nodes.append(node)
            continue

        current_text = node.text
        for alt_text, url in images:
            # split on the first occurence of the image markdown
            image_markdown = f"![{alt_text}]({url})"
            parts = current_text.split(image_markdown, 1)

            # add text before the image (if not empty)
            if parts[0]:
                new_nodes.append(TextNode(parts[0], TextType.TEXT))

            # add the image node
            new_nodes.append(TextNode(alt_text, TextType.IMAGE, url))

            # continue processing the remaining text
            current_text = parts[1]

        # add any remaining text after the last image
        if current_text:
            new_nodes.append(TextNode(current_text, TextType.TEXT))

    return new_nodes


def split_nodes_link(old_nodes):
    """
    Splits TextNode containing links into separate nodes.
    
    Args:
        old_nodes: list of nodes to process
        
    Returns:
        list: new list of nodes with extracted links
    """
    new_nodes = []
    for node in old_nodes:
        if not isinstance(node, TextNode) or node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        if not node.text:
            continue

        # extract links from the text
        links = extract_markdown_links(node.text)
        if not links:
            new_nodes.append(node)
            continue

        current_text = node.text
        for anchor_text, url in links:
            # split on the first occurrence of the link markdown
            link_markdown = f"[{anchor_text}]({url})"
            parts = current_text.split(link_markdown, 1)

            # add text before the link (if not empty)
            if parts[0]:
                new_nodes.append(TextNode(parts[0], TextType.TEXT))

            # add the link node
            new_nodes.append(TextNode(anchor_text, TextType.LINK, url))

            # continue processing the remaining text
            current_text = parts[1]

        # add any remaining text after the last link (if not empty)
        if current_text:
            new_nodes.append(TextNode(current_text, TextType.TEXT))

    return new_nodes


def text_to_textnodes(text):
    """
    Parses markdown text and returns a list of TextNode.
    
    Processes all types of inline elements: images, links, code, bold and italic text.
    
    Args:
        text: string with markdown text
        
    Returns:
        list: list of TextNode representing parsed text
    """
    # start with a single TextNode of type TEXT
    nodes = [TextNode(text, TextType.TEXT)] if text else []

    # split by images first
    nodes = split_nodes_image(nodes)

    # then split by links
    nodes = split_nodes_link(nodes)

    # then split by inline formatting: code, bold, italic
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)

    return nodes 
