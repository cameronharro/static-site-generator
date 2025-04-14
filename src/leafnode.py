from htmlnode import HTMLNode

class LeafNode(HTMLNode):
  def __init__(self, tag, value, props=None):
    super().__init__(tag, value, None, props)

  def to_html(self):
    if not self.value and (not self.tag == "img"):
      raise ValueError("Leaf nodes must have a value")
    if not self.tag:
      return self.value
    props = self.props_to_html()
    open_tag = f"<{self.tag}{props}>"
    close_tag = f"</{self.tag}>"
    return f"{open_tag}{self.value}{close_tag}"