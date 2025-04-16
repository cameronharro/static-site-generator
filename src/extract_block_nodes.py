from enum import Enum
import re

BlockType = Enum(
  'BlockType',
  [
    "PARAGRAPH",
    "HEADING",
    "CODE",
    "QUOTE",
    "UNORDERED_LIST",
    "ORDERED_LIST"
  ]
)

h_re = r"#{1,6}\ .*(?!\n)"
code_re = r"^```(.|[\n])*```$"
quote_line_re = r"^>.*"
ul_line_re = r"^-\ .*"
ol_line_re = r"^(\d+)\.\ .*"

def markdown_to_blocks(markdown):
  blocks = markdown.split("\n\n")
  return list(map(lambda x: x.strip("\n "), blocks))

def block_to_block_type(block):
  heading = re.match(h_re, block)
  if heading:
    return BlockType.HEADING
  code = re.match(code_re, block)
  if code:
    return BlockType.CODE
  new_lines = re.findall(r"\n", block)
  quote = re.findall(quote_line_re, block, re.M)
  if len(quote) == len(new_lines) + 1:
    return BlockType.QUOTE
  ul = re.findall(ul_line_re, block, re.M)
  if len(ul) == len(new_lines) + 1:
    return BlockType.UNORDERED_LIST  
  ol = re.findall(ol_line_re, block, re.M)
  if len(ol) == len(new_lines) + 1:
    numbers = list(map(lambda x: int(x), ol))
    target = list(range(1, len(ol) + 1))
    if numbers == target:
      return BlockType.ORDERED_LIST  
  return BlockType.PARAGRAPH