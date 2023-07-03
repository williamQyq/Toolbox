import argparse
from img_os_manager import ImgOsManager


def sync() -> None:
    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument(
        '--src',
        help='Path of the media storage device.',
        required=True)
    parser.add_argument(
        '--dst',
        help='Path of the partimag dir.',
        required=True)
    parser.add_argument(
        '--record',
        help='Path of txt record.',
        required=True,
        default="processed_origin_record.txt")

    args = parser.parse_args()

    manager = ImgOsManager()
    manager.sync_imgs(args.src, args.dst, args.record)


if __name__ == '__sync__':
    sync()
