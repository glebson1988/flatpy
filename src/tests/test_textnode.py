import unittest

from src.nodes import TextNode, TextType


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_not_eq_text(self):
        node = TextNode("Text A", TextType.BOLD)
        node2 = TextNode("Text B", TextType.BOLD)
        self.assertNotEqual(node, node2)

    def test_not_eq_text_type(self):
        node = TextNode("Text", TextType.TEXT)
        node2 = TextNode("Text", TextType.BOLD)
        self.assertNotEqual(node, node2)

    def test_not_eq_url(self):
        node = TextNode("Text", TextType.LINK, "http://example.com")
        node2 = TextNode("Text", TextType.LINK, "http://other.com")
        self.assertNotEqual(node, node2)

    def test_eq_with_none_url(self):
        node = TextNode("Text", TextType.LINK, url=None)
        node2 = TextNode("Text", TextType.LINK)
        self.assertEqual(node, node2)


if __name__ == "__main__":
    unittest.main()
