"""
Module for converting between different node types.
"""

from src.nodes import LeafNode, TextNode, TextType


def text_node_to_html_node(text_node):
    """
    Converts TextNode to HTMLNode.
    
    Args:
        text_node: TextNode instance to convert
        
    Returns:
        LeafNode: corresponding HTMLNode
        
    Raises:
        ValueError: if input is not a TextNode or has unsupported type
    """
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
