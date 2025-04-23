import re

from htmlnode import (
  LeafNode,
  ParentNode
)

from textnode import (
  TextNode,
  TextType,
)

from extract_block_nodes import (
  markdown_to_blocks,
  block_to_block_type,
)

from extract_inline_nodes import (
  split_inline_markdown,
)

def text_node_to_leaf_node(text_node):
  type = text_node.text_type.name
  match type:
    case "TEXT":
      return LeafNode(None, text_node.text)
    case "BOLD":
      return LeafNode("b", text_node.text)
    case "ITALIC":
      return LeafNode("i", text_node.text)
    case "CODE":
      return LeafNode("code", text_node.text)
    case "LINK":
      return LeafNode("a", text_node.text, {"href": text_node.url})
    case "IMAGE":
      return LeafNode("img", "", {"alt": text_node.text, "src": text_node.url})
    
def markdown_to_html_node(markdown):
  blocks = markdown_to_blocks(markdown)
  html_nodes = []
  for block in blocks:
    type = block_to_block_type(block)
    cleaned_text = strip_block_md(block, type)
    html_node = typed_block_to_nested_html(cleaned_text, type)
    html_nodes.append(html_node)
  return ParentNode("div", list(html_nodes))

def typed_block_to_nested_html(text, block_type):
  parent = ParentNode(block_type)
  if block_type == "code":
    parent.children = [text_node_to_leaf_node(TextNode(text, TextType.TEXT))]
    return ParentNode("pre", [parent])
  if block_type in ["ul", "ol"]:
    list_items = []
    for line in text.split("\n"):
      inline_nodes = split_inline_markdown(line)
      leaf_nodes = map(text_node_to_leaf_node, inline_nodes)
      list_items.append(ParentNode("li", list(leaf_nodes)))
    parent.children = list_items
    return parent
  else:
    split_children = split_inline_markdown(text.replace("\n", " "))
    parent.children = list(map(text_node_to_leaf_node, split_children))
    return parent
  
def strip_block_md(text, block_type):
  match block_type:
    case "p":
      return text
    case "code":
      return text.strip("`\n")
    case "blockquote":
      return text.replace(">", "")
    case "ul":
      return text.replace("- ", "")
    case "ol":
      return re.sub(r"^(\d+)\.\ ", "", text, count=100, flags=re.M)
    case "h1" | "h2" | "h3" | "h4" | "h5" | "h6":
      return text.lstrip("# ")
    case _:
      raise ValueError("block_type must be one of the BlockType Enum values")