# manager.py
from img_os_sync import ImgOSync
from img_os_sort import ImgOsSorter


class ImgOsManager:
    def __init__(self) -> None:
        pass

    def sort_imgs(self, dst, xlsx, record):
        img = ImgOsSorter(dst, xlsx, record)
        # load order mapping from xlsx
        img.sort(dst)

        return

    def sync_imgs(self, src, dst, record) -> None:
        img = ImgOSync(record)
        img.sync(src, dst)
        return

    def detect_duplicates(self):
        pass

    def output_dir_names(self):
        pass
