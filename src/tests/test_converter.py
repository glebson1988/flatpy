import unittest

from src.nodes import TextNode, TextType
from src.parsers import markdown_to_html_node, text_node_to_html_node


class TestTextNodeToHTMLNode(unittest.TestCase):

    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")
        self.assertEqual(html_node.props, {})

    def test_bold(self):
        node = TextNode("Bold text", TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "Bold text")
        self.assertEqual(html_node.props, {})

    def test_italic(self):
        node = TextNode("Italic text", TextType.ITALIC)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "i")
        self.assertEqual(html_node.value, "Italic text")
        self.assertEqual(html_node.props, {})

    def test_code(self):
        node = TextNode("Code text", TextType.CODE)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "code")
        self.assertEqual(html_node.value, "Code text")
        self.assertEqual(html_node.props, {})

    def test_link(self):
        node = TextNode("Click me", TextType.LINK, url="https://example.com")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "Click me")
        self.assertEqual(html_node.props, {"href": "https://example.com"})

    def test_image(self):
        node = TextNode("Alt text", TextType.IMAGE, url="https://example.com/image.jpg")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, "")
        self.assertEqual(
            html_node.props, {"src": "https://example.com/image.jpg", "alt": "Alt text"}
        )

    def test_invalid_text_type(self):
        class InvalidTextType:
            value = "Invalid"

        node = TextNode("Invalid text", InvalidTextType())
        with self.assertRaises(ValueError) as context:
            text_node_to_html_node(node)
        self.assertTrue(str(context.exception).startswith("Unsupported TextType:"))

    def test_link_no_url_raises_error(self):
        node = TextNode("Click me", TextType.LINK)
        with self.assertRaises(ValueError) as context:
            text_node_to_html_node(node)
        self.assertEqual(str(context.exception), "Link TextNode must have a URL")

    def test_image_no_url_raises_error(self):
        node = TextNode("Alt text", TextType.IMAGE)
        with self.assertRaises(ValueError) as context:
            text_node_to_html_node(node)
        self.assertEqual(str(context.exception), "Image TextNode must have a URL")

    def test_non_text_node_raises_error(self):
        invalid_node = "Not a TextNode"
        with self.assertRaises(ValueError) as context:
            text_node_to_html_node(invalid_node)
        self.assertEqual(str(context.exception), "Input must be a TextNode")


class TestMarkdownToHTMLNode(unittest.TestCase):

    def test_paragraphs(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_codeblock(self):
        md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )

    def test_headings(self):
        md = """
# Heading 1

## Heading 2

### Heading 3 with **bold**
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h1>Heading 1</h1><h2>Heading 2</h2><h3>Heading 3 with <b>bold</b></h3></div>",
        )

    def test_quote(self):
        md = """
> This is a
> quote block
> with **bold** text
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><blockquote>This is a\nquote block\nwith <b>bold</b> text</blockquote></div>",
        )

    def test_unordered_list(self):
        md = """
- First item with **bold**
- Second item with _italic_
- Third item with `code`
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ul><li>First item with <b>bold</b></li><li>Second item with <i>italic</i></li><li>Third item with <code>code</code></li></ul></div>",
        )

    def test_ordered_list(self):
        md = """
1. First item
2. Second item with **bold**
3. Third item
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ol><li>First item</li><li>Second item with <b>bold</b></li><li>Third item</li></ol></div>",
        )

    def test_mixed_blocks(self):
        md = """
# Main Title

This is a paragraph with **bold** text.

## Subheading

> This is a quote

- List item 1
- List item 2

```
code block here
```
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        expected = (
            "<div>"
            "<h1>Main Title</h1>"
            "<p>This is a paragraph with <b>bold</b> text.</p>"
            "<h2>Subheading</h2>"
            "<blockquote>This is a quote</blockquote>"
            "<ul><li>List item 1</li><li>List item 2</li></ul>"
            "<pre><code>code block here\n</code></pre>"
            "</div>"
        )
        self.assertEqual(html, expected)


if __name__ == "__main__":
    unittest.main()
