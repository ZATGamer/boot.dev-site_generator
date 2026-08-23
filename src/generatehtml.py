import re
import os

from blockfunctions import BlockType, block_to_block_type, markdown_to_blocks, extract_title
from htmlnode import ParentNode
from splitfunctions import text_to_textnodes
from textnode import TextNode, TextType, text_node_to_html_node

def markdown_to_html_node(markdown):
    # Split the markdown into blocks
    blocks = markdown_to_blocks(markdown)

    block_nodes = []
    # Loop over blocks
    for block in blocks:
        # Determin type of block
        block_type = block_to_block_type(block)
        # Based on block type create proper node

        if block_type == BlockType.PARAGRAPH:
            children_nodes = text_to_children(block)
            block_nodes.append(ParentNode("p", children_nodes))

        elif block_type == BlockType.HEADING:
            # Determin which heading
            level = 0
            
            for char in block:
                if char == "#":
                    level += 1
                else:
                    break

            tag = f"h{level}"
            # Strip out the Heading marker
            block = block[level + 1:]
            # create children by calling the text_to_children Function
            children_nodes = text_to_children(block)
            block_nodes.append(ParentNode(tag, children_nodes))

        elif block_type == BlockType.CODE:
            block_nodes.append(ParentNode("pre", [text_node_to_html_node(TextNode(strip_code_block(block), TextType.CODE))]))

        elif block_type == BlockType.QUOTE:
            block = block.strip("> ")
            block = block.replace(">", "")
            children_nodes = text_to_children(block)
            block_nodes.append(ParentNode("blockquote", children_nodes))


        elif block_type == BlockType.UNORDERED_LIST:
            # remove the first "- "
            block = block.strip("- ")
            # break up the items now.
            items = block.split("\n- ")
            children_html = []
            for item in items:
                children = text_to_children(item)
                children_html.append(ParentNode("li", children))
            block_nodes.append(ParentNode("ul", children_html))


        elif block_type == BlockType.ORDERED_LIST:
            start_number = r"\d\.\s"

            items = block.split("\n")
            children_html = []
            # remove the numbers from the line           
            for item in items:
                item = re.sub(start_number, "", item)
                children = text_to_children(item)
                children_html.append(ParentNode("li", children))
            block_nodes.append(ParentNode("ol", children_html))

        else:
            raise Exception("Invaild Block Type")
        
        # Assign proper child Node
    

    return ParentNode("div", children=block_nodes)

def strip_code_block(text):
    return(text[4:-3])

def replace_return_with_space(text):
    return text.replace("\n", " ")

def text_to_children(text):
    text = replace_return_with_space(text)
    text_nodes = text_to_textnodes(text)
    children_nodes = []
    for text_node in text_nodes:
        children_nodes.append(text_node_to_html_node(text_node))
    return children_nodes

def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    md = ""
    with open(from_path) as markdown:
        md = markdown.read()

    template = ""
    with open(template_path)as temp:
        template = temp.read()

    content = markdown_to_html_node(md).to_html()

    title = extract_title(md)

    template = template.replace("{{ Title }}", title)
    template = template.replace("{{ Content }}", content)

    with open(dest_path, 'w') as output:
        output.write(template)

def generate_website(content, template, dest):
    if not os.path.exists(dest):
        os.mkdir(dest)

    items = os.listdir(content)

    for item in items:
        item_path = os.path.join(content, item)
        dest_path = os.path.join(dest, item.replace('.md', '.html'))
        if os.path.isfile(item_path):
            if item.endswith(".md"):
                generate_page(item_path, template, dest_path)
        else:
            generate_website(item_path, template, dest_path)
        