import unittest

from htmlnode import (
  HTMLNode,
  ParentNode,
  LeafNode,
)

class TestHTMLNode(unittest.TestCase):
  def test(self):
    link_node = HTMLNode("a", "A link to Google.com", None, {"href": "https://www.google.com", "target": "_blank",})
    self.assertEqual(link_node.tag, "a")
    self.assertIn("href=\"https://www.google.com\"", link_node.props_to_html())
    self.assertIn("target=\"_blank\"", link_node.props_to_html())
    self.assertEqual(link_node.props_to_html(), " href=\"https://www.google.com\" target=\"_blank\"")
    self.assertRaises(NotImplementedError, link_node.to_html)

class TestLeafNode(unittest.TestCase):
  def test(self):
    hello_node = LeafNode("p", "Hello, world!")
    self.assertEqual(hello_node.to_html(), "<p>Hello, world!</p>")
    link_node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
    self.assertEqual(link_node.to_html(), "<a href=\"https://www.google.com\">Click me!</a>")
    self.assertRaises(ValueError, LeafNode(None, None).to_html,)
    self.assertEqual(LeafNode(None, "Some text").to_html(), "Some text")

class TestParentNode(unittest.TestCase):
  def test_to_html_with_children(self):
    child_node = LeafNode("span", "child")
    parent_node = ParentNode("div", [child_node])
    self.assertEqual(
      parent_node.to_html(),
      "<div><span>child</span></div>"
    )

  def test_to_html_with_multiple_children(self):
    child_node = LeafNode("span", "span text")
    child_node2 = LeafNode("b", "bold text")
    parent_node = ParentNode("div", [child_node, child_node2])
    self.assertEqual(
      parent_node.to_html(),
      "<div><span>span text</span><b>bold text</b></div>"
    )

  def test_to_html_with_grandchildren(self):
    grandchild_node = LeafNode("b", "grandchild")
    child_node = ParentNode("span", [grandchild_node])
    parent_node = ParentNode("div", [child_node])
    self.assertEqual(
      parent_node.to_html(),
      "<div><span><b>grandchild</b></span></div>",
    )

  def test_to_html_with_greatgrandchildren(self):
    greatgrandchild_node = LeafNode("b", "greatgrandchild")
    grandchild_node = ParentNode("span", [greatgrandchild_node])
    child_node = ParentNode("div", [grandchild_node])
    parent_node = ParentNode("article", [child_node])
    self.assertEqual(
      parent_node.to_html(),
      "<article><div><span><b>greatgrandchild</b></span></div></article>",
    )
  
  def test_missing_tag(self):
    child_node = LeafNode("span", "child")
    parent_node = ParentNode(None, [child_node])
    self.assertRaisesRegex(
      ValueError,
      "Parent Nodes must have a tag parameter to render valid HTML",
      parent_node.to_html
    )

  def test_missing_children(self):
    parent_node = ParentNode("div", None)
    self.assertRaisesRegex(
      ValueError,
      "Parent Nodes must have a children parameter; otherwise they should be Leaf Nodes",
      parent_node.to_html
    )


if __name__ == "__main__":
  unittest.main()