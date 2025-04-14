import unittest

from textnode import (
  TextNode,
  TextType,
)

from text_to_leaf import (
  text_node_to_leaf_node,
)

class TestTextToLeafConversion(unittest.TestCase):
  def test_text(self):
    node = TextNode("This is a text node", TextType.TEXT)
    leaf_node = text_node_to_leaf_node(node)
    self.assertEqual(leaf_node.tag, None)
    self.assertEqual(leaf_node.value, "This is a text node")
    self.assertEqual(
      leaf_node.to_html(),
      "This is a text node"
    )

  def test_bold(self):
    node = TextNode("This is a bold node", TextType.BOLD)
    leaf_node = text_node_to_leaf_node(node)
    self.assertEqual(leaf_node.tag, "b")
    self.assertEqual(leaf_node.value, "This is a bold node")
    self.assertEqual(
      leaf_node.to_html(),
      "<b>This is a bold node</b>"
    )

  def test_italic(self):
    node = TextNode("This is an italic node", TextType.ITALIC)
    leaf_node = text_node_to_leaf_node(node)
    self.assertEqual(leaf_node.tag, "i")
    self.assertEqual(leaf_node.value, "This is an italic node")
    self.assertEqual(
      leaf_node.to_html(),
      "<i>This is an italic node</i>"
    )

  def test_code(self):
    node = TextNode("This is a code node", TextType.CODE)
    leaf_node = text_node_to_leaf_node(node)
    self.assertEqual(leaf_node.tag, "code")
    self.assertEqual(leaf_node.value, "This is a code node")
    self.assertEqual(
      leaf_node.to_html(),
      "<code>This is a code node</code>"
    )

  def test_link(self):
    node = TextNode("This is a link node", TextType.LINK, "https://google.com")
    leaf_node = text_node_to_leaf_node(node)
    self.assertEqual(leaf_node.tag, "a")
    self.assertEqual(leaf_node.value, "This is a link node")
    self.assertEqual(
      leaf_node.to_html(),
      "<a href=\"https://google.com\">This is a link node</a>"
    )

  def test_image(self):
    node = TextNode("This is an image node", TextType.IMAGE, "https://hubspot.com")
    leaf_node = text_node_to_leaf_node(node)
    self.assertEqual(leaf_node.tag, "img")
    self.assertEqual(leaf_node.value, "")
    self.assertEqual(leaf_node.props_to_html(), " alt=\"This is an image node\" src=\"https://hubspot.com\"")
    self.assertEqual(
      leaf_node.to_html(),
      "<img alt=\"This is an image node\" src=\"https://hubspot.com\"></img>"
    )

if __name__ == "__main__":
  unittest.main()