from htmlnode import HTMLNode

class ParentNode(HTMLNode):

    def __init__(self, tag=None, children=None, props=None):
        # children is technically allowed to be none in the constructor to
        # keep consistency with the parent HTMLNode class but it is required
        # for a parent node
        if (children is None or len(children) == 0):
            raise ValueError("Children must be provided for a parent node")
        super().__init__(tag=tag, children=children, props=props)

    def to_html(self):
        if (self.tag is None or self.tag == ""):
            raise ValueError("Tag must be provided for a parent node")
        html_string = ""   
        for child in self.children:
            html_string += child.to_html()
        props_string = ""
        if self.props is not None:
            props_string = super().props_to_html()
        return f"<{self.tag}{props_string}>{html_string}</{self.tag}>"