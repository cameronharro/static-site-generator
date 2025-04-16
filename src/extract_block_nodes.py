def markdown_to_blocks(markdown):
  blocks = markdown.split("\n\n")
  return list(map(lambda x: x.strip("\n "), blocks))