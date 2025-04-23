import unittest

from textnode import (
  TextNode,
  TextType,
)

from markdown_to_html import (
  text_node_to_leaf_node,
  markdown_to_html_node,
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

class TestMarkdownToHTML(unittest.TestCase):
  def test_paragraphs(self):
      md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""

      node = markdown_to_html_node(md)
      desired_result = "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>"
      html = node.to_html()
      self.assertEqual(
          html,
          desired_result,
      )

  def test_codeblock(self):
    md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""

    node = markdown_to_html_node(md)
    desired_result = "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff</code></pre></div>"
    html = node.to_html()
    self.assertEqual(
        html,
        desired_result,
    )

  def test_headings(self):
    md = """
# Heading 1

## Heading 2
"""

    node = markdown_to_html_node(md)
    desired_result = "<div><h1>Heading 1</h1><h2>Heading 2</h2></div>"
    html = node.to_html()
    self.assertEqual(
        html,
        desired_result,
    )

  def test_blockquote(self):
    md = """
>This is
>a blockquote
>that's three lines long
"""

    node = markdown_to_html_node(md)
    desired_result = "<div><blockquote>This is a blockquote that's three lines long</blockquote></div>"
    html = node.to_html()
    self.assertEqual(
        html,
        desired_result,
    )
    
  def test_ul(self):
    md = """
- This is
- a list
- that's **three lines long**
"""

    node = markdown_to_html_node(md)
    desired_result = "<div><ul><li>This is</li><li>a list</li><li>that's <b>three lines long</b></li></ul></div>"
    html = node.to_html()
    self.assertEqual(
        html,
        desired_result,
    )
    
  def test_ol(self):
    md = """
1. This is
2. a list
3. that's **three lines long**
"""

    node = markdown_to_html_node(md)
    desired_result = "<div><ol><li>This is</li><li>a list</li><li>that's <b>three lines long</b></li></ol></div>"
    html = node.to_html()
    self.assertEqual(
        html,
        desired_result,
    )
    

if __name__ == "__main__":
  unittest.main()