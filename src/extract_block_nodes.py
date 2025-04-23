from enum import Enum
import re

class BlockType(Enum):
  PARAGRAPH = "p"
  HEADING = "h"
  CODE = "code"
  QUOTE = "blockquote"
  UNORDERED_LIST = "ul"
  ORDERED_LIST = "ol"

h_re = r"#{1,6}\ .*(?!\n)"
code_re = r"^```(.|[\n])*```$"
quote_line_re = r"^>.*"
ul_line_re = r"^-\ .*"
ol_line_re = r"^(\d+)\.\ .*"

def markdown_to_blocks(markdown):
  blocks = markdown.split("\n\n")
  return list(filter(lambda x: len(x) > 0, map(lambda x: x.strip("\n "), blocks)))

def block_to_block_type(block):
  heading = re.match(h_re, block)
  if heading:
    return BlockType.HEADING.value + f"{get_heading_level(block)}"
  code = re.match(code_re, block)
  if code:
    return BlockType.CODE.value
  new_lines = re.findall(r"\n", block)
  quote = re.findall(quote_line_re, block, re.M)
  if len(quote) == len(new_lines) + 1:
    return BlockType.QUOTE.value
  ul = re.findall(ul_line_re, block, re.M)
  if len(ul) == len(new_lines) + 1:
    return BlockType.UNORDERED_LIST  .value
  ol = re.findall(ol_line_re, block, re.M)
  if len(ol) == len(new_lines) + 1:
    numbers = list(map(lambda x: int(x), ol))
    target = list(range(1, len(ol) + 1))
    if numbers == target:
      return BlockType.ORDERED_LIST.value
  return BlockType.PARAGRAPH.value

def get_heading_level(text):
  if text[0] != "#":
    return 0
  return 1 + get_heading_level(text[1:])