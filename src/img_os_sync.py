# Main method sync
from utility import Utility
import os
import shutil
from tqdm import tqdm


class ImgOSync(Utility):
    def __init__(self, record_path):
        super().__init__()
        """
    class constructor for dirs tree syncing.

    Example dir tree:

    partimag/
    ├── HP/
    |   ├── 2023-05-01-HP-192254585654/
    |   ├── .../
    ├── Asus/
    |   ├── 2023-0501-Asus-192254585653/
    |   └── .../
    └──/Others/.../
    """

        self.root = os.path.abspath(os.getcwd())
        self.record_path = os.path.join(self.root, record_path)

    def sync(self, media_device, partimag) -> None:
        """
            Copies all directories and files in media_device to partimag, but only if partimag
            has the dir with the same category directory name.

            Image dir with the same name will not be copied.

            Args:
              media_device: source file path
              partimag: destination file path
        """
        if not (os.path.exists(media_device) and os.path.exists(partimag)):
            print('{0: <13}'.format("[Err]") + f"media_device or partimag path not found:"
                  f"\n**************************\n"
                  f"media_device: {media_device}\n"
                  f"partimag: {partimag}\n"
                  f"**************************\n")

            return
        # no found record txt
        if not os.path.exists(self.record_path):
            print('{0: <13}'.format("[Err]") + f"Record file not found:"
                  f"\n**************************\n"
                  f"record: {self.record_path}\n"
                  f"**************************\n")
            return

        def copy_callback(media_image_basename, media_catg_dir):
            dst_partimag_catg_dir = os.path.join(
                partimag, os.path.basename(media_catg_dir))
            if os.path.exists(dst_partimag_catg_dir):
                self.copy_catg_dir_tree(media_catg_dir, dst_partimag_catg_dir)
            else:
                print('{0: <13}'.format(
                    "[Attention]") + f"Directory {media_catg_dir} not exists in [partimag].")

        # cp all catg dirs in media_device to partimag folder
        self.traverse_partimag_exec_cb_in_catg_dirs(
            media_device, copy_callback)

        print('{0: <13}'.format("[End]") +
              f"\n**************************\n"
              f"***Finished syncing.***\n"
              f"**************************")
        return

    def get_records(self, record_path) -> set:
        """
            load file lines into a set.

            Args:
              record_file_path: str
        """
        file_path_record = set()

        try:
            with open(record_path, "r") as file:
                lines = file.readlines()

            file_path_record = set(line.strip() for line in lines)
        except:
            print('{0: <13}'.format(
                "[Err]")+f'Cannot get record from record_path: {record_path}')

        return file_path_record

    def copy_catg_dir_tree(self, src, dst) -> None:
        """
        Copies all files and directories in src to dst for brand dirs,
        but only if dst does not have the same directory name.

        Args:
              src: source file path
              dst: destination file path
        """
        for item in os.listdir(src):
            src_imag = os.path.join(src, item)  # e.g. /media/usr/HP/193...
            dst_imag = os.path.join(dst, item)  # e.g. /partimag/HP/193...

            # skipping image that has been renamed or handled.
            if self.check_file_path_in_record(item, self.record_path):
                print('{0: <13}'.format("[Skipping]") +
                      f'Processed Record already has: {src_imag}')
                continue

            # skipping image already exists in partimag.
            if os.path.exists(dst_imag):
                # print("{0: <13}".format("[Skipping]")+f" Directory '{dst_imag}' already exists.")
                continue

            if not os.path.isdir(src_imag):
                # not a dir, handle unknown file
                print('{0: <13}'.format("[Unkown File]") +
                      f"\n**************************\n"
                      f"file: {item}\n"
                      f"path: {src}\n"
                      f"\n**************************\n")
                continue

            try:
                # copy image in category to destination path
                self.copy_directory_tree(src_imag, dst_imag)
                print('{0: <13}'.format("[Sync]") +
                      f"{src_imag} -----> {dst_imag}")
            except Exception as e:
                print('{0:<13}'.format("[Err]") +
                      f"\n**************************\n"
                      f"{src_imag} - - -> {dst_imag}\n"
                      f"{e}\n"
                      f"\n**************************\n")

            return

    # cp directory with percentage progress bar
    def copy_directory_tree(self, src_dir, dst_dir):
        try:
            total = sum(len(files) for _, _, files in os.walk(src_dir))
            tqdm.write(
                f"Copying {total} files and directories from {src_dir} to {dst_dir}\n")
            with tqdm(total=total, unit="file") as pbar:
                for root, dirs, files in os.walk(src_dir):
                    for file in files:
                        src_path = os.path.join(root, file)
                        dest_path = src_path.replace(src_dir, dst_dir, 1)
                        os.makedirs(os.path.dirname(dest_path), exist_ok=True)
                        shutil.copy2(src_path, dest_path)
                        pbar.update(1)
                    for dir in dirs:
                        src_path = os.path.join(root, dir)
                        dst_path = src_path.replace(src_dir, dst_dir, 1)
                        os.makedirs(dst_path, exist_ok=True)
            tqdm.write('{0: <13}'.format("[Finished]") + f"Copying complete")
        except Exception as e:
            print(f"An error occurred while copying the directory: {e}")
