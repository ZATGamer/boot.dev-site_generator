import re

from textnode import TextNode, TextType


def split_nodes_delimiter(old_nodes: list[TextNode], delimiter: str, text_type: TextType) -> list[TextNode]:
    new_nodes = []

    for old_node in old_nodes:
        if old_node.text_type is not TextType.TEXT:
            new_nodes.append(old_node)
            continue

        split_node = []
        sections = old_node.text.split(delimiter)

        if len(sections) % 2 == 0:
            raise Exception(f"No closing delimiter found")

        for i in range(len(sections)):
            if sections[i] == "":
                continue
            if i % 2 == 0:
                new_nodes.append(TextNode(sections[i], TextType.TEXT))
            else:
                new_nodes.append(TextNode(sections[i], text_type))
        new_nodes.extend(split_node)
    return new_nodes


def extract_markdown_images(text) -> list[tuple[str, str]]:
    return(re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text))
    

def extract_markdown_links(text) -> list[tuple[str, str]]:
    return(re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)",text))


def split_nodes_image(old_nodes: list[TextNode]) -> list[TextNode]:
    new_nodes = []

    for old_node in old_nodes:
        # Lets look for any images in the text
        images = extract_markdown_images(old_node.text)
        if len(images) == 0:
            new_nodes.append(old_node)
            continue
        # We have images, break apart the string at the image points
        current_text = old_node.text
        for image in images:
            split_point = f"![{image[0]}]({image[1]})"
            sections = current_text.split(split_point)
            if len(sections) == 2:
                new_nodes.append(TextNode(sections[0], TextType.TEXT))
                new_nodes.append(TextNode(image[0], TextType.IMAGE, image[1]))
                current_text = sections[-1]
            else:
                raise Exception("Invalid Format")
        if current_text != "":
            new_nodes.append(TextNode(current_text, TextType.TEXT))
    return new_nodes


def split_nodes_link(old_nodes: list[TextNode]) -> list[TextNode]:
    new_nodes = []
    
    for old_node in old_nodes:
        # Lets look for any images in the text
        links = extract_markdown_links(old_node.text)
        if len(links) == 0:
            new_nodes.append(old_node)
            continue
        # We have images, break apart the string at the image points
        current_text = old_node.text
        for link in links:
            split_point = f"[{link[0]}]({link[1]})"
            sections = current_text.split(split_point)
            if len(sections) == 2:
                new_nodes.append(TextNode(sections[0], TextType.TEXT))
                new_nodes.append(TextNode(link[0], TextType.LINK, link[1]))
                current_text = sections[-1]
            else:
                raise Exception("Invalid format")
        if current_text != "":
            new_nodes.append(TextNode(current_text, TextType.TEXT))
    return new_nodes


def text_to_textnodes(text):
    if not text:
        raise Exception("No text provided")
    nodes = [TextNode(text, TextType.TEXT)]

    delimiters = {
        "`": TextType.CODE,
        "**": TextType.BOLD,
        "_":TextType.ITALIC
        }

    for delimiter in delimiters:
        nodes = split_nodes_delimiter(nodes, delimiter, delimiters[delimiter])

    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    
    return nodes
