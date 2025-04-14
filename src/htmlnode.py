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