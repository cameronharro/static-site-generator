import unittest

from textnode import (
  TextNode,
  TextType,
)

from split_nodes import (
  split_nodes_delimiter,
  split_nodes_image,
  split_nodes_link,
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

class TestSplitImage(unittest.TestCase):
  def test_no_image(self):
    node = TextNode(
      "This is text with no images at all",
      TextType.TEXT,
    )
    new_nodes = split_nodes_image([node])
    self.assertListEqual(
      [
        TextNode("This is text with no images at all", TextType.TEXT),
      ],
      new_nodes,
    )

  def test_solo_image(self):
    node = TextNode(
      "![image](https://i.imgur.com/zjjcJKZ.png)",
      TextType.TEXT,
    )
    new_nodes = split_nodes_image([node])
    self.assertListEqual(
      [
        TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
      ],
      new_nodes,
    )

  def test_two_images(self):
    node = TextNode(
      "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
      TextType.TEXT,
    )
    new_nodes = split_nodes_image([node])
    self.assertListEqual(
      [
        TextNode("This is text with an ", TextType.TEXT),
        TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
        TextNode(" and another ", TextType.TEXT),
        TextNode("second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"),
      ],
      new_nodes,
    )

  def test_image_and_link(self):
    node = TextNode(
      "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and a [hyperlink](https://i.imgur.com/3elNhQu.png)",
      TextType.TEXT,
    )
    new_nodes = split_nodes_image([node])
    self.assertListEqual(
      [
        TextNode("This is text with an ", TextType.TEXT),
        TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
        TextNode(" and a [hyperlink](https://i.imgur.com/3elNhQu.png)", TextType.TEXT),
      ],
      new_nodes,
    )

  def test_multiple_nodes(self):
    node = TextNode(
      "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and a [hyperlink](https://i.imgur.com/3elNhQu.png)",
      TextType.TEXT,
    )
    node1 = TextNode(
      "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and a [hyperlink](https://i.imgur.com/3elNhQu.png)",
      TextType.TEXT,
    )
    new_nodes = split_nodes_image([node, node1])
    self.assertListEqual(
      [
        TextNode("This is text with an ", TextType.TEXT),
        TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
        TextNode(" and a [hyperlink](https://i.imgur.com/3elNhQu.png)", TextType.TEXT),
        TextNode("This is text with an ", TextType.TEXT),
        TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
        TextNode(" and a [hyperlink](https://i.imgur.com/3elNhQu.png)", TextType.TEXT),
      ],
      new_nodes,
    )

class TestSplitLink(unittest.TestCase):
  def test_no_link(self):
    node = TextNode(
      "This is text with no links at all",
      TextType.TEXT,
    )
    new_nodes = split_nodes_link([node])
    self.assertListEqual(
      [
        TextNode("This is text with no links at all", TextType.TEXT),
      ],
      new_nodes,
    )

  def test_solo_link(self):
    node = TextNode(
      "[to boot dev](https://www.boot.dev)",
      TextType.TEXT,
    )
    new_nodes = split_nodes_link([node])
    self.assertListEqual(
      [
        TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
      ],
      new_nodes,
    )

  def test_two_links(self):
    node = TextNode(
      "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)",
      TextType.TEXT,
    )
    new_nodes = split_nodes_link([node])
    self.assertEqual(
      [
        TextNode("This is text with a link ", TextType.TEXT),
        TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
        TextNode(" and ", TextType.TEXT),
        TextNode(
          "to youtube", TextType.LINK, "https://www.youtube.com/@bootdotdev"
        ),
      ],
      new_nodes
    )

  def test_image_and_link(self):
    node = TextNode(
      "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and a [hyperlink](https://i.imgur.com/3elNhQu.png)",
      TextType.TEXT,
    )
    new_nodes = split_nodes_link([node])
    self.assertListEqual(
      [
        TextNode("This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and a ", TextType.TEXT),
        TextNode("hyperlink", TextType.LINK, "https://i.imgur.com/3elNhQu.png"),
      ],
      new_nodes,
    )

  def test_multiple_nodes(self):
    node = TextNode(
      "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and a [hyperlink](https://i.imgur.com/3elNhQu.png)",
      TextType.TEXT,
    )
    node1 = TextNode(
      "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and a [hyperlink](https://i.imgur.com/3elNhQu.png)",
      TextType.TEXT,
    )
    new_nodes = split_nodes_link([node, node1])
    self.assertListEqual(
      [
        TextNode("This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and a ", TextType.TEXT),
        TextNode("hyperlink", TextType.LINK, "https://i.imgur.com/3elNhQu.png"),
        TextNode("This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and a ", TextType.TEXT),
        TextNode("hyperlink", TextType.LINK, "https://i.imgur.com/3elNhQu.png"),
      ],
      new_nodes,
    )

if __name__ == "__main__":
  unittest.main()