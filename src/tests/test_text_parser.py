"""
Tests for parsing markdown inline elements.
"""

import unittest
from src.nodes import TextNode, TextType
from src.parsers import (
    split_nodes_delimiter,
    extract_markdown_images,
    extract_markdown_links,
    split_nodes_image,
    split_nodes_link,
    text_to_textnodes
)


class TestSplitNodesDelimiter(unittest.TestCase):
    """Tests for the split_nodes_delimiter function."""
    
    def test_split_code_single(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        expected = [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" word", TextType.TEXT),
        ]
        self.assertEqual(new_nodes, expected)

    def test_split_bold_single(self):
        node = TextNode("This is text with a **bold phrase** here", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        expected = [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("bold phrase", TextType.BOLD),
            TextNode(" here", TextType.TEXT),
        ]
        self.assertEqual(new_nodes, expected)

    def test_split_italic_single(self):
        node = TextNode("This is text with an _italic phrase_ here", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "_", TextType.ITALIC)
        expected = [
            TextNode("This is text with an ", TextType.TEXT),
            TextNode("italic phrase", TextType.ITALIC),
            TextNode(" here", TextType.TEXT),
        ]
        self.assertEqual(new_nodes, expected)

    def test_multiple_delimiters(self):
        node = TextNode("This has **bold** and **another bold** text", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        expected = [
            TextNode("This has ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" and ", TextType.TEXT),
            TextNode("another bold", TextType.BOLD),
            TextNode(" text", TextType.TEXT),
        ]
        self.assertEqual(new_nodes, expected)

    def test_non_text_node(self):
        node1 = TextNode("Bold text", TextType.BOLD)
        node2 = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node1, node2], "`", TextType.CODE)
        expected = [
            TextNode("Bold text", TextType.BOLD),
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" word", TextType.TEXT),
        ]
        self.assertEqual(new_nodes, expected)

    def test_missing_closing_delimiter(self):
        node = TextNode("This is text with a `code block word", TextType.TEXT)
        with self.assertRaises(ValueError) as context:
            split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(
            str(context.exception),
            "Invalid Markdown syntax: missing closing delimiter '`' in text: This is text with a `code block word",
        )

    def test_empty_text(self):
        node = TextNode("", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(new_nodes, [])

    def test_delimiter_at_start(self):
        node = TextNode("**bold** text", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        expected = [
            TextNode("bold", TextType.BOLD),
            TextNode(" text", TextType.TEXT),
        ]
        self.assertEqual(new_nodes, expected)

    def test_delimiter_at_end(self):
        node = TextNode("text **bold**", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        expected = [
            TextNode("text ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
        ]
        self.assertEqual(new_nodes, expected)

    def test_no_delimiter(self):
        node = TextNode("This is plain text", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        expected = [TextNode("This is plain text", TextType.TEXT)]
        self.assertEqual(new_nodes, expected)


class TestExtractMarkdownElements(unittest.TestCase):
    """Tests for extracting images and links from markdown."""
    
    def test_extract_markdown_images_single(self):
        text = "This is text with a ![image](https://i.imgur.com/zjjcJKZ.png) and some more text."
        result = extract_markdown_images(text)
        self.assertEqual(result, [("image", "https://i.imgur.com/zjjcJKZ.png")])

    def test_extract_markdown_images_multiple(self):
        text = (
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another "
            "![second image](https://i.imgur.com/dfsdkjfd.png)"
        )
        result = extract_markdown_images(text)
        expected = [
            ("image", "https://i.imgur.com/zjjcJKZ.png"),
            ("second image", "https://i.imgur.com/dfsdkjfd.png"),
        ]
        self.assertEqual(result, expected)

    def test_extract_markdown_images_empty(self):
        text = "This is text with no images"
        result = extract_markdown_images(text)
        self.assertEqual(result, [])

    def test_extract_markdown_images_mixed_with_links(self):
        text = "Text with ![image](https://i.imgur.com/zjjcJKZ.png) and [link](https://www.boot.dev)"
        result = extract_markdown_images(text)
        self.assertEqual(result, [("image", "https://i.imgur.com/zjjcJKZ.png")])

    def test_extract_markdown_images_empty_alt(self):
        text = "Text with ![](https://i.imgur.com/zjjcJKZ.png)"
        result = extract_markdown_images(text)
        self.assertEqual(result, [("", "https://i.imgur.com/zjjcJKZ.png")])

    def test_extract_markdown_links_single(self):
        text = "This is text with a [link](https://www.boot.dev) and some more text."
        result = extract_markdown_links(text)
        self.assertEqual(result, [("link", "https://www.boot.dev")])

    def test_extract_markdown_links_multiple(self):
        text = (
            "This is text with a [link](https://www.boot.dev) and "
            "[another link](https://www.google.com) here."
        )
        result = extract_markdown_links(text)
        expected = [
            ("link", "https://www.boot.dev"),
            ("another link", "https://www.google.com"),
        ]
        self.assertEqual(result, expected)

    def test_extract_markdown_links_empty(self):
        text = "This is text with no links"
        result = extract_markdown_links(text)
        self.assertEqual(result, [])

    def test_extract_markdown_links_mixed_with_images(self):
        text = "Text with [link](https://www.boot.dev) and ![image](https://i.imgur.com/zjjcJKZ.png)"
        result = extract_markdown_links(text)
        self.assertEqual(result, [("link", "https://www.boot.dev")])

    def test_extract_markdown_links_empty_anchor(self):
        text = "Text with [](https://www.boot.dev)"
        result = extract_markdown_links(text)
        self.assertEqual(result, [("", "https://www.boot.dev")])


class TestSplitNodesImage(unittest.TestCase):
    """Tests for the split_nodes_image function."""
    
    def test_split_images(self):
        node = TextNode(
            "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        expected = [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("rick roll", TextType.IMAGE, "https://i.imgur.com/aKaOqIh.gif"),
            TextNode(" and ", TextType.TEXT),
            TextNode("obi wan", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
        ]
        self.assertListEqual(new_nodes, expected)

    def test_split_images_single(self):
        node = TextNode(
            "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and some more text",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        expected = [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("rick roll", TextType.IMAGE, "https://i.imgur.com/aKaOqIh.gif"),
            TextNode(" and some more text", TextType.TEXT),
        ]
        self.assertListEqual(new_nodes, expected)

    def test_split_images_no_images(self):
        node = TextNode("This is text with no images", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        expected = [TextNode("This is text with no images", TextType.TEXT)]
        self.assertListEqual(new_nodes, expected)

    def test_split_images_empty_text(self):
        node = TextNode("", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        self.assertEqual(new_nodes, [])

    def test_split_images_non_text_node(self):
        node = TextNode("Bold text", TextType.BOLD)
        new_nodes = split_nodes_image([node])
        expected = [TextNode("Bold text", TextType.BOLD)]
        self.assertListEqual(new_nodes, expected)

    def test_split_images_mixed_content(self):
        node = TextNode(
            "Text ![image](https://i.imgur.com/zjjcJKZ.png) more text",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        expected = [
            TextNode("Text ", TextType.TEXT),
            TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
            TextNode(" more text", TextType.TEXT),
        ]
        self.assertListEqual(new_nodes, expected)


class TestSplitNodesLink(unittest.TestCase):
    """Tests for the split_nodes_link function."""
    
    def test_split_links(self):
        node = TextNode(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        expected = [
            TextNode("This is text with a link ", TextType.TEXT),
            TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
            TextNode(" and ", TextType.TEXT),
            TextNode("to youtube", TextType.LINK, "https://www.youtube.com/@bootdotdev"),
        ]
        self.assertListEqual(new_nodes, expected)

    def test_split_links_single(self):
        node = TextNode(
            "This is text with a link [to boot dev](https://www.boot.dev) and some more text",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        expected = [
            TextNode("This is text with a link ", TextType.TEXT),
            TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
            TextNode(" and some more text", TextType.TEXT),
        ]
        self.assertListEqual(new_nodes, expected)

    def test_split_links_no_links(self):
        node = TextNode("This is text with no links", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        expected = [TextNode("This is text with no links", TextType.TEXT)]
        self.assertListEqual(new_nodes, expected)

    def test_split_links_empty_text(self):
        node = TextNode("", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        self.assertEqual(new_nodes, [])

    def test_split_links_non_text_node(self):
        node = TextNode("Bold text", TextType.BOLD)
        new_nodes = split_nodes_link([node])
        expected = [TextNode("Bold text", TextType.BOLD)]
        self.assertListEqual(new_nodes, expected)

    def test_split_links_mixed_content(self):
        node = TextNode(
            "Text [link](https://www.boot.dev) and ![image](https://i.imgur.com/zjjcJKZ.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        expected = [
            TextNode("Text ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://www.boot.dev"),
            TextNode(" and ![image](https://i.imgur.com/zjjcJKZ.png)", TextType.TEXT),
        ]
        self.assertListEqual(new_nodes, expected)


class TestTextToTextnodes(unittest.TestCase):
    """Tests for the text_to_textnodes function."""
    
    def test_text_to_textnodes_full(self):
        text = (
            "This is **text** with an _italic_ word and a `code block` and an "
            "![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        )
        nodes = text_to_textnodes(text)
        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("text", TextType.BOLD),
            TextNode(" with an ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" word and a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" and an ", TextType.TEXT),
            TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
            TextNode(" and a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://boot.dev"),
        ]
        self.assertListEqual(nodes, expected)

    def test_text_to_textnodes_only_text(self):
        text = "This is plain text"
        nodes = text_to_textnodes(text)
        expected = [TextNode("This is plain text", TextType.TEXT)]
        self.assertListEqual(nodes, expected)

    def test_text_to_textnodes_only_formatting(self):
        text = "**bold** _italic_ `code`"
        nodes = text_to_textnodes(text)
        expected = [
            TextNode("bold", TextType.BOLD),
            TextNode(" ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" ", TextType.TEXT),
            TextNode("code", TextType.CODE),
        ]
        self.assertListEqual(nodes, expected)

    def test_text_to_textnodes_only_image(self):
        text = "![image](https://i.imgur.com/zjjcJKZ.png)"
        nodes = text_to_textnodes(text)
        expected = [TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png")]
        self.assertListEqual(nodes, expected)

    def test_text_to_textnodes_only_link(self):
        text = "[link](https://www.boot.dev)"
        nodes = text_to_textnodes(text)
        expected = [TextNode("link", TextType.LINK, "https://www.boot.dev")]
        self.assertListEqual(nodes, expected)

    def test_text_to_textnodes_empty(self):
        text = ""
        nodes = text_to_textnodes(text)
        self.assertListEqual([], nodes)

    def test_text_to_textnodes_mixed_no_formatting(self):
        text = "Text with ![image](https://i.imgur.com/zjjcJKZ.png) and [link](https://www.boot.dev)"
        nodes = text_to_textnodes(text)
        expected = [
            TextNode("Text with ", TextType.TEXT),
            TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
            TextNode(" and ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://www.boot.dev"),
        ]
        self.assertListEqual(nodes, expected)

    def test_text_to_textnodes_formatting_in_text(self):
        text = "Text with **bold** and ![image](https://i.imgur.com/zjjcJKZ.png)"
        nodes = text_to_textnodes(text)
        expected = [
            TextNode("Text with ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" and ", TextType.TEXT),
            TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
        ]
        self.assertListEqual(nodes, expected)


if __name__ == "__main__":
    unittest.main() 
