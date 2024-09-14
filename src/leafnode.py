from htmlnode import HTMLNode

class LeafNode(HTMLNode):
    
    def __init__(self, tag=None, value=None, children=None, props=None):
        super().__init__(tag, value, children, props)
    