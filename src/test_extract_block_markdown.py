import unittest

from extract_block_nodes import (
   markdown_to_blocks,
   block_to_block_type,
   BlockType,
)

class TestExtractBlocks(unittest.TestCase):
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

  def test_ugly_markdown(self):
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

  def test_wrong_markdown(self):
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
        "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line\n- This is a list\n- with items",
      ],
    )

class TestBlockToHeading(unittest.TestCase):
  def test_heading_1(self):
    block = "# Heading 1"
    self.assertEqual(block_to_block_type(block), BlockType.HEADING)
  def test_heading_2(self):
    block = "## Heading 2"
    self.assertEqual(block_to_block_type(block), BlockType.HEADING)
  def test_heading_3(self):
    block = "### Heading 3"
    self.assertEqual(block_to_block_type(block), BlockType.HEADING)
  def test_heading_4(self):
    block = "#### Heading 4"
    self.assertEqual(block_to_block_type(block), BlockType.HEADING)
  def test_heading_5(self):
    block = "##### Heading 5"
    self.assertEqual(block_to_block_type(block), BlockType.HEADING)
  def test_heading_6(self):
    block = "###### Heading 6"
    self.assertEqual(block_to_block_type(block), BlockType.HEADING)
  def test_consecutive_headings(self):
    block = """
  # Heading 1
  # Heading 2
  """
    self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)
  def test_unstripped_newline(self):
    block = """
  # Heading 1

  """
    self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)
  def test_no_space(self):
    block = "#Heading"
    self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)