import unittest

from htmlnode import (
  HTMLNode,
)

class TestHTMLNode(unittest.TestCase):
  def test_eq(self):
    linknode = HTMLNode("a", "A link to Google.com", None, {"href": "https://www.google.com", "target": "_blank",})
    self.assertEqual(linknode.tag, "a")
    self.assertIn("href=\"https://www.google.com\"", linknode.props_to_html())
    self.assertIn("target=\"_blank\"", linknode.props_to_html())
    self.assertEqual(linknode.props_to_html(), " href=\"https://www.google.com\" target=\"_blank\" ")
    self.assertRaises(NotImplementedError, linknode.to_html)

if __name__ == "__main__":
  unittest.main()