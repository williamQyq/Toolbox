# utility.py
import os


class Utility:
    def __init__(self):
        pass

    def traverse_partimag_exec_cb_in_catg_dirs(self, partimag_dir, cb) -> None:
        """
          Traverse [partimag] dir tree and execute, run callback, passing img dir basename and Brand Category name.
          Args:
            parent_dir: partimage dir path
            cb(subject_dir_basename,catg_dir_abs_path): your callback function
        """

        for catg_dir in os.listdir(partimag_dir):
            catg_dir = os.path.join(partimag_dir, catg_dir)
            if os.path.isdir(catg_dir):
                for item in os.listdir(catg_dir):
                    imag_dir = os.path.join(catg_dir, item)
                    if os.path.isdir(imag_dir) and item != '.ipynb_checkpoints':
                        # pass the base name and the catgory dir abs path. e.g. 2023-05-01-HP-192254585654/, /partimag/HP/
                        cb(item, catg_dir)
        return

    def check_file_path_in_record(self, search, record_path) -> bool:
        try:
            with open(record_path, "r") as file:
                file_content = file.read()

            if search in file_content:
                return True
        except:
            print('{0: <13}'.format("[Err]") +
                  f'Cannot open record_path: {record_path}')

        return False
