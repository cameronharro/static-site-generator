import unittest

from textnode import (
  TextNode,
  TextType,
)

from split_nodes import (
  split_nodes_delimiter
)

class TestSplitDelimiter(unittest.TestCase):
  bold_node = TextNode("This is text with a *bold* word", TextType.TEXT)
  italic_node = TextNode("This is text with an _italic_ word", TextType.TEXT)
  code_node = TextNode("This is text with a `code block`", TextType.TEXT)
  multi_marked_node = TextNode("This `text block` has _multiple_ different *markup* styles", TextType.TEXT)

  def test_bold_node(self):
    new_nodes = split_nodes_delimiter([self.bold_node], "*", TextType.BOLD)
    self.assertEqual(
      new_nodes,
      [
        TextNode("This is text with a ", TextType.TEXT),
        TextNode("bold", TextType.BOLD),
        TextNode(" word", TextType.TEXT),
      ]
    )

  def test_italic_node(self):
    new_nodes = split_nodes_delimiter([self.italic_node], "_", TextType.ITALIC)
    self.assertEqual(
      new_nodes,
      [
        TextNode("This is text with an ", TextType.TEXT),
        TextNode("italic", TextType.ITALIC),
        TextNode(" word", TextType.TEXT),
      ]
    )

  def test_code_node(self):
    new_nodes = split_nodes_delimiter([self.code_node], "`", TextType.CODE)
    self.assertEqual(
      new_nodes,
      [
        TextNode("This is text with a ", TextType.TEXT),
        TextNode("code block", TextType.CODE),
      ]
    )

  def test_multiple_nodes(self):
    new_nodes = split_nodes_delimiter([self.bold_node, self.italic_node], "*", TextType.BOLD)
    self.assertEqual(
      new_nodes, 
      [
        TextNode("This is text with a ", TextType.TEXT),
        TextNode("bold", TextType.BOLD),
        TextNode(" word", TextType.TEXT),
        self.italic_node
      ]
    )

  def test_multi_node(self):
    new_nodes = split_nodes_delimiter(
      split_nodes_delimiter(
        split_nodes_delimiter(
          [self.multi_marked_node],
          "`",
          TextType.CODE,
        ),
        "_",
        TextType.ITALIC,
        ),
      "*",
      TextType.BOLD,
    )
    self.assertEqual(
      new_nodes,
      [
        TextNode("This ", TextType.TEXT),
        TextNode("text block", TextType.CODE),
        TextNode(" has ", TextType.TEXT),
        TextNode("multiple", TextType.ITALIC),
        TextNode(" different ", TextType.TEXT),
        TextNode("markup", TextType.BOLD),
        TextNode(" styles", TextType.TEXT),
      ],
    )

if __name__ == "__main__":
  unittest.main()