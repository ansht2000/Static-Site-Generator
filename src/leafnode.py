from htmlnode import HTMLNode

class LeafNode(HTMLNode):

    def __init__(self, tag=None, value=None, props=None):
        # value is technically allowed to be none in the constructor to keep
        # consistency with the parent HTMLNode class but it is required
        # for a leaf node
        if value is None:
            raise ValueError("Value must be provided for a leaf node")
        super().__init__(tag=tag, value=value, props=props)
    
    def to_html(self):
        if self.tag is None:
            return f"{self.value}"
        props_string = ""
        if self.props is not None:
            props_string = super().props_to_html()
        return f"<{self.tag}{props_string}>{self.value}</{self.tag}>"

        