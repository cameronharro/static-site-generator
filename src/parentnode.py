from htmlnode import (
  HTMLNode
)

class ParentNode(HTMLNode):
  def __init__(self, tag, children, props=None):
    super().__init__(tag, None, children, props)

  def to_html(self):
    if not self.tag:
      raise ValueError("Parent Nodes must have a tag parameter to render valid HTML")
    if not self.children:
      raise ValueError("Parent Nodes must have a children parameter; otherwise they should be Leaf Nodes")
    props = self.props_to_html()
    open_tag = f"<{self.tag}{props}>"
    close_tag = f"</{self.tag}>"
    children_html = "".join(map(lambda x: x.to_html(), self.children))
    return f"{open_tag}{children_html}{close_tag}"
    
