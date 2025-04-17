from leafnode import (
  LeafNode
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