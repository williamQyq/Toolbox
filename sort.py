# sorting.py
import argparse
from src.img_os_manager import ImgOsManager


def sort() -> None:
    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument(
        '--dst',
        help='Path of the "Partimag".',
        required=True)
    parser.add_argument(
        '--xlsx',
        help='Path of the id excel.',
        required=True,
        default="DISKFORMAT-LIANG.xlsx")
    parser.add_argument(
        '--record',
        help='Path of the processed image record.',
        required=True,
        default="processed_origin_record.txt")

    args = parser.parse_args()

    # init sorter
    manager = ImgOsManager()
    # load order mapping from xlsx
    manager.sort_imgs(args.dst, args.xlsx, args.record)


if __name__ == '__sorting__':
    sort()
