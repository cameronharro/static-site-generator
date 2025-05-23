from sys import (
  argv
)

from os import (
  listdir,
  mkdir, 
)

from pathlib import (
  Path
)

from shutil import (
  copy,
  rmtree,
)

from markdown_to_html import(
  extract_title,
  markdown_to_html_node
)

def matching_dest_path(dest_root, path):
  return Path.joinpath(dest_root, *path.parts[1:])

def copy_dir_tree(src_dirs, dest_root):
  for dir in src_dirs:
    matching_dir = matching_dest_path(dest_root, dir)
    if not Path.exists(matching_dir):
      mkdir(matching_dir)

def clean_copy_directory_contents(src_root, dest_root):
  src_p = Path(src_root)
  src_files, src_dirs = get_paths_recursive(src_p)
  copy_dir_tree(src_dirs, dest_root)
  for path in src_files:
    copy(path, matching_dest_path(dest_root, path))

def get_paths_recursive(curr_path):
  contained_paths = list(map(lambda x: Path.joinpath(curr_path, x), listdir(curr_path)))
  files = []
  dirs = [curr_path]
  next_calls = []
  for path in contained_paths:
    if Path.is_dir(path):
      next_calls.append(path)
    else:
      files.append(path)
  if len(files) != len(contained_paths):
    for dir in next_calls:
      nested_files, nested_dirs = get_paths_recursive(dir)
      files.extend(nested_files)
      dirs.extend(nested_dirs)
  return files, dirs

def generate_page(from_path, template_path, dest_path, basepath):
  print(f"Generating page from {from_path} to {dest_path} using {template_path}")
  src_file = open(from_path)
  md = src_file.read()
  src_file.close()

  template_file = open(template_path)
  html = template_file.read()
  template_file.close()

  title = extract_title(md)
  content = markdown_to_html_node(md).to_html()
  html = html.replace("{{ Title }}", title)
  html = html.replace("{{ Content }}", content)
  html = html.replace("href=\"/", f"href=\"{basepath}")
  html = html.replace("src=\"/", f"src=\"{basepath}")
  
  dest_file = open(dest_path, "x")
  dest_file.write(html)
  dest_file.close()

def generate_pages_recursive(src_root_path, template_path, dest_root_path, basepath):
  src_p = Path(src_root_path)
  src_files, src_dirs = get_paths_recursive(src_p)
  copy_dir_tree(src_dirs, dest_root_path)
  for file in src_files:
    dest_path = matching_dest_path(dest_root_path, file)
    dirs = list(reversed(dest_path.parents))
    converted_extension = Path.joinpath(dirs[-1], dest_path.stem + ".html")
    generate_page(file, template_path, converted_extension, basepath)

def main():
  basepath = argv[1] or "/"
  dest_p = Path("./docs")
  if Path.exists(dest_p):
    rmtree(dest_p)
  clean_copy_directory_contents("./static", dest_p)
  generate_pages_recursive("./content", "./template.html", dest_p, basepath)

if __name__ == "__main__":
  main()