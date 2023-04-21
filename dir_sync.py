import os
import shutil
import argparse
from typing import List
from tqdm import tqdm

class DirectorySync:
  def __init__(self):
    self.root = os.path.abspath(os.getcwd())

  def copy_dirs_with_subdirs(self, src, dst)->None:
    """
        Copies all directories and files in src to dst, but only if dst does not
        have the same directory name. If a directory with the same name exists,
        only its files are copied.
    """
  
    abs_src = os.path.join(self.root, src)
    abs_dst = os.path.join(self.root,dst)

    for item in os.listdir(abs_src):
      src_path = os.path.join(abs_src, item) #e.g. /media/usr/HP
      dst_path = os.path.join(abs_dst, item) #e.g. /partimag/HP
      
      if os.path.isdir(src_path):
        #if /partimag/HP exists:
        if os.path.exists(dst_path):
          self.copy_dirs(src_path,dst_path)
        else:
          print('{0: <13}'.format("[Msg]") + f"Directory '{dst_path}' not exists.'")

    print('{0: <13}'.format("[End]") + f"finished syncing.")

  def copy_dirs(self, src, dst)->None:
    """
    Copies all files and directories in src to dst for brand dirs,
    but only if dst does not have the same directory name.
    """
    for item in os.listdir(src):
        src_path = os.path.join(src, item) #e.g. /media/usr/HP/193...
        dst_path = os.path.join(dst, item) #e.g. /partimag/HP/193...
        
        if os.path.isdir(src_path):
            if not os.path.exists(dst_path):
                print('{0: <13}'.format("[sync]") + f"Syncing '{src_path}' with '{dst_path}'")
                try:
                  self.copy_directory_tree(src_path,dst_path)
                except Exception as e:
                  print('{0:<13}'.format("[Err]") + f"{e}")
            else:
              # print("[Msg] {:>10}".format(f" Directory '{dst_path}' already exists."))
              continue
        else:
          # not a dir, is a file 
          basename = os.path.basename(src_path)
          if not os.path.exists(os.path.join(dst,basename)):
            print('{0: <13}'.format("[Copy Files]") + f"copying '{src_path}' -> '{dst_path}'")
            shutil.copy2(src_path,dst_path)
          else:
            continue
  
  def copy_directory_tree(self, src_dir, dest_dir):
    try:
        total = sum(len(files) for _, _, files in os.walk(src_dir))
        tqdm.write(f"Copying {total} files and directories from {src_dir} to {dest_dir}")
        with tqdm(total=total, unit="file") as pbar:
            for root, dirs, files in os.walk(src_dir):
                for file in files:
                    src_path = os.path.join(root, file)
                    dest_path = src_path.replace(src_dir, dest_dir, 1)
                    os.makedirs(os.path.dirname(dest_path), exist_ok=True)
                    shutil.copy2(src_path, dest_path)
                    pbar.update(1)
                for dir in dirs:
                    src_path = os.path.join(root, dir)
                    dest_path = src_path.replace(src_dir, dest_dir, 1)
                    os.makedirs(dest_path, exist_ok=True)
        tqdm.write('{0: <13}'.format("[Status]") + f"Copying complete")
    except Exception as e:
        print(f"An error occurred while copying the directory: {e}")


def main()->None:
  parser = argparse.ArgumentParser(
      formatter_class=argparse.ArgumentDefaultsHelpFormatter)
  parser.add_argument(
      '--src',
      help='Path of the src dir.',
      required=True)
  parser.add_argument(
      '--dst',
      help='Path of the dst dir.',
      required=True,
      default="partimag")
  
  args= parser.parse_args()

  dir_sync = DirectorySync()
  dir_sync.copy_dirs_with_subdirs(args.src,args.dst)

if __name__ == '__main__':
  main()
