from textnode import (
  TextType,
  TextNode
)

def split_nodes_delimiter(old_nodes, delimiter, text_type):
  if not isinstance(text_type, TextType):
    raise ValueError("text_type must be an instance of the TextType enum")
  new_nodes = []
  for node in old_nodes:
    text = node.text
    parent_type = node.text_type
    split_text = text.split(delimiter)
    for i in range(0, len(split_text)):
      snippet = split_text[i]
      if len(snippet) > 0:
        new_nodes.append(TextNode(snippet, parent_type if i % 2 == 0 else text_type))
  return new_nodes
