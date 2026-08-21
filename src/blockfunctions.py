import re

from enum import Enum

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"


def markdown_to_blocks(markdown):
    if not markdown:
        raise Exception("No Markdown provided.")
    new_blocks = markdown.split("\n\n")
    updated_blocks = []
    for index, new_block in enumerate(new_blocks):
        new_block = new_block.strip('\n ')
        if new_block != '':
            updated_blocks.append(new_block)
        else:
            continue
    return(updated_blocks)


def block_to_block_type(block):
    block_lines = block.split("\n")

    if block.startswith(("# ", "## ", "### ", "#### ", "##### ", "###### ")):
        #Headings start with 1-6 # characters, followed by a space and then the heading text.
        return(BlockType.HEADING)

    if len(block_lines) > 1 and block.startswith("```\n") and block.endswith("\n```"):
        #Multiline Code blocks must start with 3 backticks and a newline, then end with 3 backticks.
        return(BlockType.CODE)

    if block.startswith("> "):
        #Every line in a quote block must start with a "greater-than" character: > followed by the quote text. A space after > is allowed but not required. 
        all_lines = True
        for line in block_lines:
            if not line.startswith("> "):
                all_lines = False
        if all_lines:
            return(BlockType.QUOTE)

    if block.startswith("- "):
        #Every line in an unordered list block must start with a - character, followed by a space.
        all_lines = True
        for line in block_lines:
            if line.startswith("- "):
                continue
            else:
                all_lines = False
                break
        if all_lines:
            return(BlockType.UNORDERED_LIST)

    start_number = r"\d\.\s"
    if block.startswith("1. "):
        #Every line in an ordered list block must start with a number followed by a . character and a space. The number must start at 1 and increment by 1 for each line.
        is_ordered = True
        current_line = 1
        for line in block_lines:
            if line.startswith(f"{current_line}. "):
                current_line += 1
                continue
            else:
                is_ordered = False
                break
            # Check the start of each line and make sure the number show == the number it should be.
        if is_ordered:
            return(BlockType.ORDERED_LIST)
        
    #If none of the above conditions are met, the block is a normal paragraph.
    return(BlockType.PARAGRAPH)
