from htmlnode import HTMLNode

class LeafNode(HTMLNode):
  def __init__(self, tag, value, props=None):
    super().__init__(tag, value, None, props)
    if not value:
      raise ValueError("Leaf nodes must have a value")

  def to_html(self):
    if not self.tag:
      return self.value
    props = self.props_to_html()
    open_tag = f"<{self.tag}{props}>"
    close_tag = f"</{self.tag}>"
    return f"{open_tag}{self.value}{close_tag}"