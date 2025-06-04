import unittest

from htmlnode import HTMLNode

class TestHTMLNode(unittest.TestCase):
    def test_props_to_html_single_attribute(self):
        node = HTMLNode(tag="a", value="link", props={"href": "https://example.com"})
        self.assertEqual(node.props_to_html(), ' href="https://example.com"')

    def test_props_to_html_several_attributes(self):
        node = HTMLNode(tag="a", value="link", props={"href": "https://keklol.com", "target": "_blank"})
        self.assertEqual(node.props_to_html(), ' href="https://keklol.com" target="_blank"')

    def test_props_to_html_empty(self):
        node = HTMLNode()
        self.assertEqual(node.props_to_html(), "")
