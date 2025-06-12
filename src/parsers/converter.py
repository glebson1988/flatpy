import re

from src.nodes import BlockType, LeafNode, ParentNode, TextNode, TextType
from src.parsers.block_parser import block_to_block_type, markdown_to_blocks
from src.parsers.text_parser import text_to_textnodes


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
        return LeafNode(
            tag="img", value="", props={"src": text_node.url, "alt": text_node.text}
        )
    else:
        raise ValueError(f"Unsupported TextType: {text_node.text_type}")


def text_to_children(text):
    text_nodes = text_to_textnodes(text)
    children = []
    for text_node in text_nodes:
        html_node = text_node_to_html_node(text_node)
        children.append(html_node)
    return children


def block_to_html_node(block, block_type):
    if block_type == BlockType.PARAGRAPH:
        # replace newlines with spaces for paragraphs
        text = block.replace("\n", " ")
        children = text_to_children(text)
        return ParentNode("p", children)

    elif block_type == BlockType.HEADING:
        # extract heading level and text
        lines = block.splitlines()
        first_line = lines[0]
        level = len(first_line) - len(first_line.lstrip("#"))
        heading_text = first_line[level:].strip()
        children = text_to_children(heading_text)
        return ParentNode(f"h{level}", children)

    elif block_type == BlockType.CODE:
        # remove code block markers (```)
        lines = block.splitlines()
        if lines[0].startswith("```"):
            lines = lines[1:]
        if lines and lines[-1].startswith("```"):
            lines = lines[:-1]
        code_text = "\n".join(lines)
        # add newline at the end if it's not empty
        if code_text and not code_text.endswith("\n"):
            code_text += "\n"
        # for code blocks, we don't process inline markdown
        code_node = LeafNode(tag=None, value=code_text)
        inner_code = ParentNode("code", [code_node])
        return ParentNode("pre", [inner_code])

    elif block_type == BlockType.QUOTE:
        # remove > from each line
        lines = block.splitlines()
        quote_lines = []
        for line in lines:
            if line.startswith(">"):
                quote_lines.append(line[1:].strip())
            else:
                quote_lines.append(line.strip())
        quote_text = "\n".join(quote_lines)
        children = text_to_children(quote_text)
        return ParentNode("blockquote", children)

    elif block_type == BlockType.UNORDERED_LIST:
        # split into list items
        lines = block.splitlines()
        list_items = []
        for line in lines:
            if line.strip():
                # remove - and space
                item_text = re.sub(r"^\-\s+", "", line)
                item_children = text_to_children(item_text)
                list_items.append(ParentNode("li", item_children))
        return ParentNode("ul", list_items)

    elif block_type == BlockType.ORDERED_LIST:
        # split into list items
        lines = block.splitlines()
        list_items = []
        for line in lines:
            if line.strip():
                # remove number, dot and space
                item_text = re.sub(r"^\d+\.\s+", "", line)
                item_children = text_to_children(item_text)
                list_items.append(ParentNode("li", item_children))
        return ParentNode("ol", list_items)

    else:
        raise ValueError(f"Unknown block type: {block_type}")


def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    children = []

    for block in blocks:
        block_type = block_to_block_type(block)
        html_node = block_to_html_node(block, block_type)
        children.append(html_node)

    return ParentNode("div", children)
