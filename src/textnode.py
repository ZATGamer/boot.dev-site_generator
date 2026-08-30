from enum import Enum
from htmlnode import LeafNode

class TextType(Enum):
    TEXT = "text"
    BOLD = "bold"
    ITALIC = "italic"
    CODE = "code"
    LINK = "link"
    IMAGE = "image"

class TextNode():

    def __init__(self, text, text_type, url=None):
        self.text: str = text
        self.text_type: TextType = TextType(text_type)
        self.url: str = url

    def __eq__(self, other: TextNode):
        text = False
        text_type = False
        url = False
        if self.text == other.text:
            text = True
        if self.text_type == other.text_type:
            text_type = True
        if self.url == other.url:
            url = True

        if text and text_type and url:
            return True
        else:
            return False

    def __repr__(self):
        return (f"TextNode({self.text}, {self.text_type.value}, {self.url})")


def text_node_to_html_node(text_node: TextNode) -> LeafNode:

    if text_node.text_type == TextType.TEXT:
        return LeafNode(None, text_node.text)
    elif text_node.text_type == TextType.BOLD:
        return LeafNode("b", text_node.text)
    elif text_node.text_type == TextType.ITALIC:
        return LeafNode("i", text_node.text)
    elif text_node.text_type == TextType.CODE:
        return LeafNode("code", text_node.text)
    elif text_node.text_type == TextType.LINK:
        if text_node.url is None:
            raise ValueError("invalid URL")
        return LeafNode("a", text_node.text, {"href": text_node.url})
    elif text_node.text_type == TextType.IMAGE:
        if text_node.url is None:
            raise ValueError("invalid URL")
        return LeafNode("img", "", {"src": text_node.url, "alt": text_node.text})
    raise ValueError(f"invalid text type: {text_node.text_type}")