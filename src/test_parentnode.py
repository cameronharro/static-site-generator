import unittest
from parentnode import (
  ParentNode,
)
from leafnode import (
  LeafNode
)


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