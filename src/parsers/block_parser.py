"""
Module for parsing markdown block elements (headings, lists, quotes, code).
"""

import re
from src.nodes import BlockType


def markdown_to_blocks(markdown):
    """
    Splits markdown text into separate blocks.
    
    Blocks are separated by two or more line breaks.
    Empty lines and extra spaces are removed.
    
    Args:
        markdown: string with markdown text
        
    Returns:
        list: list of strings, each representing a separate block
    """
    raw_blocks = re.split(r'\n\s*\n', markdown.strip())

    blocks = []
    for block in raw_blocks:
        lines = block.splitlines()
        stripped_lines = [line.strip() for line in lines if line.strip()]
        if stripped_lines:
            blocks.append("\n".join(stripped_lines))

    return blocks


def block_to_block_type(block):
    """
    Determines block type based on its content.
    
    Args:
        block: string with block content
        
    Returns:
        BlockType: block type (HEADING, CODE, QUOTE, UNORDERED_LIST, ORDERED_LIST, PARAGRAPH)
    """
    if not block:
        return BlockType.PARAGRAPH

    lines = block.splitlines()

    # heading: starts with 1–6 # and space
    if re.match(r'^#{1,6}\s+.+$', lines[0]):
        return BlockType.HEADING

    # code: starts and ends with ```
    if len(lines) >= 1 and lines[0].startswith('```') and lines[-1].startswith('```'):
        return BlockType.CODE

    # quote: all rows start with >
    if all(line.startswith('>') for line in lines if line.strip()):
        return BlockType.QUOTE

    # unordered list: all rows start with - and space
    if all(re.match(r'^\-\s+.+$', line) for line in lines if line.strip()):
        return BlockType.UNORDERED_LIST

    # ordered list: all rows start with number, dot and space (1., 2., ...)
    if lines and all(
        re.match(r'^\d+\.\s+.+$', line) for line in lines if line.strip()
    ):
        # check that numbers start with 1
        numbers = [
            int(re.match(r'^(\d+)\.', line).group(1))
            for line in lines if line.strip()
        ]
        if numbers == list(range(1, len(numbers) + 1)):
            return BlockType.ORDERED_LIST

    # default: paragraph
    return BlockType.PARAGRAPH 
