import unittest
from leafnode import (
  LeafNode,
)

class TestLeafNode(unittest.TestCase):
  def test(self):
    hello_node = LeafNode("p", "Hello, world!")
    self.assertEqual(hello_node.to_html(), "<p>Hello, world!</p>")
    link_node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
    self.assertEqual(link_node.to_html(), "<a href=\"https://www.google.com\">Click me!</a>")
    self.assertRaises(ValueError, LeafNode, None, None)
    self.assertEqual(LeafNode(None, "Some text").to_html(), "Some text")

if __name__ == "__main__":
  unittest.main()