class HTMLNode:
  def __init__(self, tag=None, value=None, children=None, props=None):
    self.tag = tag
    self.value = value
    self.children = children
    self.props = props
  
  def to_html(self):
    raise NotImplementedError()
  
  def props_to_html(self):
    html_string = ''
    if self.props:
      for key in self.props:
        html_string = html_string + f" {key}=\"{self.props[key]}\""
    return html_string
  
  def __repr__(self):
    return f"HTMLNode | tag: {self.tag}, value: {self.value}, children: {self.children}, props: {self.props},"
  
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