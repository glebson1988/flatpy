"""
Tests for parsing markdown block elements.
"""

import unittest

from src.nodes import BlockType
from src.parsers import block_to_block_type, markdown_to_blocks


class TestBlockParser(unittest.TestCase):
    """Tests for block parsing functions."""

    def test_markdown_to_blocks(self):
        md = """
        This is **bolded** paragraph

        This is another paragraph with _italic_ text and `code` here
        This is the same paragraph on a new line

        - This is a list
        - with items
        """
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_markdown_to_blocks_single(self):
        md = "# This is a heading"
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            ["# This is a heading"],
        )

    def test_markdown_to_blocks_multiple(self):
        md = """
        # Heading

        Paragraph with **bold** text.

        - List item 1
        - List item 2
        """
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "# Heading",
                "Paragraph with **bold** text.",
                "- List item 1\n- List item 2",
            ],
        )

    def test_markdown_to_blocks_empty(self):
        md = ""
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, [])

    def test_markdown_to_blocks_only_newlines(self):
        md = "\n\n\n"
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, [])

    def test_markdown_to_blocks_extra_newlines(self):
        md = "\n\n# Heading\n\n\nParagraph\n\n\n"
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "# Heading",
                "Paragraph",
            ],
        )

    def test_markdown_to_blocks_leading_trailing_whitespace(self):
        md = "   \n# Heading  \n  \nParagraph  \n  \n"
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "# Heading",
                "Paragraph",
            ],
        )

    def test_markdown_to_blocks_paragraph_with_newlines(self):
        md = """
        Paragraph line 1
        line 2
        line 3

        - List
        - Items
        """
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "Paragraph line 1\nline 2\nline 3",
                "- List\n- Items",
            ],
        )

    def test_block_type_heading(self):
        block = "# Heading"
        self.assertEqual(block_to_block_type(block), BlockType.HEADING)
        block = "## Subheading"
        self.assertEqual(block_to_block_type(block), BlockType.HEADING)
        block = "###### Deep Heading"
        self.assertEqual(block_to_block_type(block), BlockType.HEADING)
        block = "# Heading\nText"
        self.assertEqual(block_to_block_type(block), BlockType.HEADING)
        block = "####### Not a heading"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)
        block = "#No space heading"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)
        block = "# "
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_block_type_code(self):
        block = "```\nCode here\n```"
        self.assertEqual(block_to_block_type(block), BlockType.CODE)
        block = "```python\nprint('Hello')\n```"
        self.assertEqual(block_to_block_type(block), BlockType.CODE)
        block = "```\nIncomplete"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_block_type_quote(self):
        block = "> Quote text"
        self.assertEqual(block_to_block_type(block), BlockType.QUOTE)
        block = "> Line 1\n> Line 2"
        self.assertEqual(block_to_block_type(block), BlockType.QUOTE)
        block = "> Quote\nNot a quote"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_block_type_unordered_list(self):
        block = "- Item 1\n- Item 2"
        self.assertEqual(block_to_block_type(block), BlockType.UNORDERED_LIST)
        block = "- Single item"
        self.assertEqual(block_to_block_type(block), BlockType.UNORDERED_LIST)
        block = "- Item 1\nInvalid item"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_block_type_ordered_list(self):
        block = "1. Item 1\n2. Item 2"
        self.assertEqual(block_to_block_type(block), BlockType.ORDERED_LIST)
        block = "1. Single item"
        self.assertEqual(block_to_block_type(block), BlockType.ORDERED_LIST)
        block = "1. Item 1\n3. Item 2"  # wrong order
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)
        block = "2. Item 1"  # starts not from 1
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_block_type_paragraph(self):
        block = "This is a paragraph"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)
        block = "Line 1\nLine 2"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)
        block = ""  # empty block
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)


if __name__ == "__main__":
    unittest.main()
