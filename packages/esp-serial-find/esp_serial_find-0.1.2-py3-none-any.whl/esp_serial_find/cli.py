"""Console script for esp_serial_find."""

import argparse
import logging
import os
import plistlib
from typing import Dict, List, Tuple

from .esp_serial_find import find_serial_and_path, find_subtree_paths

logging.basicConfig(level=logging.ERROR)
logger = logging.getLogger(__name__)


def main():
    """Main entrypoint."""

    argparser = argparse.ArgumentParser()

    argparser.add_argument("--verbose", "-v", action="store_true", help="Print verbose output")

    # if provided a serial number, only print the path for that serial number
    argparser.add_argument(
        "--serial",
        "-s",
        type=str,
        default=None,
        help="Print the path for the given serial number",
    )

    args = argparser.parse_args()

    if args.verbose:
        logging.basicConfig(level=logging.DEBUG)

    # read the plist
    plist = os.popen("ioreg -i -t -r -c AppleUSBACMData -l -a").read()
    data: List = plistlib.loads(plist.encode())
    paths = find_subtree_paths(data)

    logging.info("Found {} ESP32 devices".format(len(paths)))

    serial_and_path: List[Tuple[str, str]] = [
        (
            path[-2].get("USB Serial Number"),
            path[-1].get("IORegistryEntryChildren")[0].get("IODialinDevice"),
        )
        for path in paths
    ]

    if args.serial:
        # find the path for the given serial number
        serial = args.serial
        path_device = None
        for serial, path in serial_and_path:
            if serial == args.serial:
                path_device = path
                break

        # if the serial number was not found, print an error
        if not path_device:
            logging.error("Serial number {} not found".format(args.serial))
            exit(1)
        else:
            print(path_device)
            exit(0)

    for serial, path in serial_and_path:
        print("{} {}".format(serial, path))


if __name__ == "__main__":
    main()  # pragma: no cover
