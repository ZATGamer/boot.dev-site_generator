import unittest

from blockfunctions import (
    markdown_to_blocks,
    block_to_block_type,
    extract_title,
    BlockType,
)


class TestMarkdownToHTML(unittest.TestCase):
    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_markdown_to_blocks_newlines(self):
        md = """
This is **bolded** paragraph




This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_block_id(self):
        md = """
# Heading 1

## Heading 2

### Heading 3

#### Heading 4

##### Heading 5

###### Heading 6

```
This is a code Block for testing
And this is a 2nd line for more testing
Might as well add a 3rd line
```

> this is some quoted text
> this is a 2nd line
> this is a 3rd line

- unordered list item 1
- unordered list item 2
- unordered list item 3

1. Ordered List 1
2. Ordered List 2
3. Ordered List 3

This is a paragraph of text.
There is nothing special about it.
Its just text
"""
        blocks = markdown_to_blocks(md)
        blocktypes = []
        for block in blocks:
            blocktypes.append(block_to_block_type(block))
        self.assertEqual(blocktypes, [
            BlockType.HEADING,
            BlockType.HEADING,
            BlockType.HEADING,
            BlockType.HEADING,
            BlockType.HEADING,
            BlockType.HEADING,
            BlockType.CODE,
            BlockType.QUOTE,
            BlockType.UNORDERED_LIST,
            BlockType.ORDERED_LIST,
            BlockType.PARAGRAPH
        ])
        

    def test_block_id_brokens(self):
        md = """
# Heading 1

## Heading 2

### Heading 3

#### Heading 4

##### Heading 5

###### Heading 6

```
This is a code Block for testing
And this is a 2nd line for more testing
Might as well add a 3rd line
```

```
this is a broken code block
there is no closing brackets

> this is some quoted text
> this is a 2nd line
> this is a 3rd line

> this is going to be
a broken quote
> for testing

- unordered list item 1
- unordered list item 2
- unordered list item 3

1. Ordered List 1
2. Ordered List 2
3. Ordered List 3

1. Broken Order List 1
3. Broken Order List 2
2. Broken Order List 3

This is a paragraph of text.
There is nothing special about it.
Its just text
"""
        blocks = markdown_to_blocks(md)
        blocktypes = []
        for block in blocks:
            blocktypes.append(block_to_block_type(block))
        self.assertEqual(blocktypes, [
            BlockType.HEADING,
            BlockType.HEADING,
            BlockType.HEADING,
            BlockType.HEADING,
            BlockType.HEADING,
            BlockType.HEADING,
            BlockType.CODE,
            BlockType.PARAGRAPH,
            BlockType.QUOTE,
            BlockType.PARAGRAPH,
            BlockType.UNORDERED_LIST,
            BlockType.ORDERED_LIST,
            BlockType.PARAGRAPH,
            BlockType.PARAGRAPH
            ])

    def test_extract_title(self):
        md = """
## Heading 2

# Heading 1

### Heading 3
"""
        title = extract_title(md)
        self.assertEqual(
            title,
            "Heading 1"
        )

    def test_extract_title_fail(self):
        md = """
## Heading 2

# Heading 1 extra.    

### Heading 3
"""
        title = extract_title(md)
        self.assertEqual(
            title,
            "Heading 1 extra."
        )
        

if __name__ == "__main__":
    unittest.main()
