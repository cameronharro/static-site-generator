import re

from textnode import (
  TextType,
  TextNode
)

def split_nodes_delimiter(delimiter, text_type):
  def inner_func(old_nodes):
    if not isinstance(text_type, TextType):
      raise ValueError("text_type must be an instance of the TextType enum")
    new_nodes = []
    for node in old_nodes:
      if node.text_type != TextType.TEXT:
        new_nodes.append(node)
        continue
      text = node.text
      parent_type = node.text_type
      split_text = text.split(delimiter)
      for i in range(0, len(split_text)):
        snippet = split_text[i]
        if len(snippet) > 0:
          new_nodes.append(TextNode(snippet, parent_type if i % 2 == 0 else text_type))
    return new_nodes
  return inner_func

split_nodes_bold = split_nodes_delimiter("**", TextType.BOLD)
split_nodes_italic = split_nodes_delimiter("_", TextType.ITALIC)
split_nodes_code = split_nodes_delimiter("`", TextType.CODE)

link_re = r"(?<!!)(\[[^\[\]]*\]\([^\(\)]*\))"
image_re = r"(!\[[^\[\]]*\]\([^\(\)]*\))"

def extract_url_tuple(text):
  splt = text.split("](")
  text = splt[0].strip("![]")
  url = splt[1].strip("()")
  return ((text, url))

def split_url_node(regex, target_type):
  if not isinstance(target_type, TextType):
    raise ValueError("text_type must be an instance of the TextType enum")
  
  def map_text_to_node(parent_type):
    def inner_func(snip):
      if len(snip) == 0:
        return None
      match = re.match(regex, snip)
      if match:
        tuple = extract_url_tuple(match.group())
        return TextNode(tuple[0], target_type, tuple[1])
      else:
        return TextNode(snip, parent_type)
    return inner_func
  
  def inner_func(old_nodes):
    new_nodes = []
    for node in old_nodes:
      if not isinstance(node.text_type, TextType):
        raise ValueError("text_type must be an instance of the TextType enum")
      if node.text_type != TextType.TEXT:
        new_nodes.append(node)
        continue
      text = node.text
      splt = re.split(regex, text)
      new_nodes.extend(filter(lambda x: x, map(map_text_to_node(node.text_type), splt)))
    return new_nodes
  return inner_func

split_nodes_image = split_url_node(image_re, TextType.IMAGE)
split_nodes_link = split_url_node(link_re, TextType.LINK)

def split_inline_markdown(text):
  initial_node = [TextNode(text, TextType.TEXT)]
  bold_extracted = split_nodes_bold(initial_node)
  italic_extracted = split_nodes_italic(bold_extracted)
  code_extracted = split_nodes_code(italic_extracted)
  link_extracted = split_nodes_link(code_extracted)
  image_extracted = split_nodes_image(link_extracted)
  return image_extracted