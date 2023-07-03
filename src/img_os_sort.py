# prefix sorting.py
from utility import Utility
import pandas as pd
import re
import os
import shutil
from typing import Tuple


# Main method : sort


class ImgOsSorter(Utility):
    def __init__(self, target_dir, excel_path, record_path):
        super().__init__()  # inherit parent attributes: root
        self.target_dir = target_dir  # target partimag dir
        self.excel_path = excel_path
        self.record_path = record_path

    def sort(self, partimag_dir) -> None:
        """
        Add the sorting id to imag basename. 4 digits upc patern matched
        dir path will be saved in record.txt

        Args:
          dst: the path of destination dir.
          iloc_dict: the dict contains the index and upc mapping.
        """
        if not os.path.exists(partimag_dir):
            print('{0: <13}'.format("[Err]") +
                  f"\n**************************\n"
                  f"Partimag path not found!\n"
                  f"partimag: {partimag_dir}\n"
                  f"**************************")
            return

        if not os.path.exists(self.record_path):
            print('{0: <13}'.format("[Err]") +
                  f"\n**************************\n"
                  f"Record path not found!\n"
                  f"record: {self.record_path}\n"
                  f"**************************")
            return

        upc_index_dict, df = self.get_id_from_excel(
            sheet_name="image location",
            col_upc="UPC",
            col_id="No",
            col_catg="Catg")
        self.modify_os_imgs_with_id_prefix(upc_index_dict)

    def get_id_from_excel(self, sheet_name, col_upc, col_id, col_catg) -> Tuple[dict[str, int], pd.DataFrame]:
        """
          load excel contains upc_sku and index mapping, create dict

          Args:
            sheet_name: the name of sheet contains the mapping
            col_upc: the name of "UPC" column
            col_id: the name of "#id" column
            col_catg: the name of "col_catg" column

        """

        """
      create catg, upc, iloc dict
      format example:
        {
          "HP": {
            "192333222111": 1
          }
        }

      """
        # dict store upc, id mapping
        upc_iloc_dict = {}

        try:
            # load the upc, id sheet
            df = pd.read_excel(self.excel_path, sheet_name)
            df.dropna(subset=df.columns[2], inplace=True)
            # Check that the required columns exist in the DataFrame
            required_columns = [col_upc, col_id, col_catg]
            for col in required_columns:
                if col not in df.columns:
                    raise ValueError(f"Column '{col}' not found in DataFrame")

            # create catgory, upc, id dict
            for index, row in df.iterrows():
                upc = row[col_upc]
                id = row[col_id]
                catg = row[col_catg]

                # create dict[catg] if not exist.
                if catg not in upc_iloc_dict:
                    upc_iloc_dict[catg] = {}
                # add map(upc, id) under catg in dict.
                upc_iloc_dict[catg][upc] = id

        except FileNotFoundError:
            print("[Error] Excel file not found")
        except ValueError:
            print(f"[Error] {ValueError}")
        except Exception as e:
            print('{0: <13}'.format(
                "[Error]" + f"Excel Cant Open: {self.excel_path}\n{e}"))

        return upc_iloc_dict, df

    def modify_os_imgs_with_id_prefix(self, iloc_dict):
        def rename_os_img_basename_cb(origin_imag_basename, catg_path) -> None:
            # find basename of renamed or not renamed image dir 
            pattern = r"^.*?#(.*)$"
            basename = re.sub(pattern,r"\1",origin_imag_basename)
            # skip already renamed imag
            is_in_record = self.check_file_path_in_record(
                basename, self.record_path)
            if is_in_record:
                print(
                    f"[Attention] Skipping! Already in record: {origin_imag_basename}")
                return

            # extract the upc last 4 digits: "^.*HP(\d)?{1234}.*$"
            last_four_digits_upc_pattern = r'[A-Za-z]+(\d{0,}\d{4})$'
            match = re.search(
                last_four_digits_upc_pattern,
                origin_imag_basename)

            if match:
                # add leading mapping id to the dir_basename
                four_digits_upc = match.group(1)
                catg = str(os.path.basename(catg_path)).upper()
                id = self.get_id_from_mapping_dict(
                    four_digits_upc, catg, iloc_dict)
                # add leading id to matched dir and rename dir
                if not id:
                    print('{0: <13}'.format("[Warning]" +
                                            f"\n******************************\n"
                                            f"Skipping! upc digits not found in Excel: {origin_imag_basename}\n"
                                            f"brand category: {catg}\n"
                                            f"Hint: Is the image in excel record?\n"
                                            f"******************************"))
                    return 

                # format and align dir basename
                formatted_id = "{:03d}".format(int(id))
                new_dirname_with_id = f"{formatted_id}#{origin_imag_basename}"
                self.rename_dir(
                    os.path.join(catg_path, origin_imag_basename),
                    os.path.join(catg_path, new_dirname_with_id))

            # else no upc digits pattern match
            else:
                print('{0: <13}'.format("[Warning]" +
                                        f"\n******************************\n"
                                        f"Skipping! upc digits not found: {origin_imag_basename}\n"
                                        f"brand category: {catg}\n"
                                        f"Hint: Does image dir match the pattern(case ignored)? e.g. HP2345\n"
                                        f"******************************"))
            return  # end of rename callback

        self.traverse_partimag_exec_cb_in_catg_dirs(
            self.target_dir, rename_os_img_basename_cb)
        print('{0: <13}'.format("[End]") +
              f"\n****************************************\n"
              f"*********Finished syncing.**************\n"
              f"****************************************")
        return

    def rename_dir(self, src, dst) -> None:
        is_in_record = self.check_file_path_in_record(
            os.path.basename(src), self.record_path)

        if not os.path.exists(src):
            print('{0: <13}'.format("[Rename Err]") +
                  f"\n**************************\n"
                  f"Source Dir Not Found: '{src}'\n"
                  f"**************************")
        elif is_in_record:
            print('{0: <13}'.format("[Rename Err]") +
                  f"\n**************************\n"
                  f"New Name Dir Already Renamed: '{os.path.basename(src)}'.\n"
                  f"**************************")
        else:
            shutil.move(src, dst)
            # add dir path processed record to /partimag/processed_record.txt
            with open(self.record_path, "a") as f:
                f.write(f"{src}\n")
            print('{0: <13}'.format("[Success]") +
                  f"Renamed '{src}' ---> '{dst}'\n")

        return

    def get_id_from_mapping_dict(self, last_4_digits, catg, my_dict):
        # found mapping id in dict category
        for upc in my_dict[catg]:
            upc_last_four_digits = upc[-4:]
            if last_4_digits == upc_last_four_digits:
                return my_dict[catg][upc]

        return None
