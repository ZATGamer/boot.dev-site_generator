class HTMLNode():
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag: str = tag
        self.value: str = value
        self.children: list[HTMLNode] = children
        self.props: dict[str:str] = props

    def to_html(self):
        raise NotImplementedError("to_html method not implemented")

    def props_to_html(self):
        if self.props:
            return_string = ""
            for prop in self.props:
                return_string += f" {prop}=\"{self.props[prop]}\""
        else:
            return_string = ""

        return return_string
    
    def __repr__(self):
        return(f"HTMLNode({self.tag}, {self.value}, children: {self.children}, {self.props})")


class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, None, props)

    def to_html(self):
        if self.value is None:
            raise ValueError("invalid HTML: no value")
        if self.tag is None:
            return self.value
        
        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"
                    

    def __repr__(self):
        return (f"HTMLNode({self.tag}, {self.value}, {self.props})")


class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, None, children, props)

    def to_html(self):
        if self.tag is None:
            raise ValueError("invalid TAG: no value")
        if self.children is None:
            raise ValueError('invalid CHILDREN: no children')

        children_html = ""
        for child in self.children:
            children_html += child.to_html()

        return f"<{self.tag}{self.props_to_html()}>{children_html}</{self.tag}>"