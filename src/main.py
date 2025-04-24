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

def matching_dest_path(dest_root, path):
  return Path.joinpath(dest_root, *path.parts[1:])

def clean_copy_directory_contents(src_path, dest_path):
  src_p = Path(src_path)
  dest_p = Path(dest_path)
  if Path.exists(dest_p):
    rmtree(dest_p)
  src_files, src_dirs = get_paths_recursive(src_p)
  mkdir(dest_p)
  for dir in src_dirs:
    mkdir(matching_dest_path(dest_p, dir))
  for path in src_files:
    copy(path, matching_dest_path(dest_p, path))

def get_paths_recursive(curr_path):
  contained_paths = list(map(lambda x: Path.joinpath(curr_path, x), listdir(curr_path)))
  files = []
  dirs = []
  for path in contained_paths:
    if Path.is_dir(path):
      dirs.append(path)
    else:
      files.append(path)
  if len(dirs) != 0:
    for dir in dirs:
      nested_files, nested_dirs = get_paths_recursive(dir)
      files.extend(nested_files)
      dirs.extend(nested_dirs)
  return files, dirs

def main():
  clean_copy_directory_contents("./static", "./public")

if __name__ == "__main__":
  main()