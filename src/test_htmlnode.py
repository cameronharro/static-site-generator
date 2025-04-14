import unittest

from htmlnode import (
  HTMLNode,
)

class TestHTMLNode(unittest.TestCase):
  def test(self):
    link_node = HTMLNode("a", "A link to Google.com", None, {"href": "https://www.google.com", "target": "_blank",})
    self.assertEqual(link_node.tag, "a")
    self.assertIn("href=\"https://www.google.com\"", link_node.props_to_html())
    self.assertIn("target=\"_blank\"", link_node.props_to_html())
    self.assertEqual(link_node.props_to_html(), " href=\"https://www.google.com\" target=\"_blank\"")
    self.assertRaises(NotImplementedError, link_node.to_html)

if __name__ == "__main__":
  unittest.main()