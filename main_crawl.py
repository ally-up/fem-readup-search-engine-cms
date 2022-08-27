#!/usr/bin/env python3

import getopt
import os
import sys

file_path = os.path.realpath(__file__)
script_path = os.path.dirname(file_path)

# Make library available in path
library_paths = [
    os.path.join(script_path, "lib"),
    os.path.join(script_path, "lib", "crawler"),
    os.path.join(script_path, "lib", "log"),
]

for p in library_paths:
    if not (p in sys.path):
        sys.path.insert(0, p)

from logger_facade import LoggerFacade
from boell_crawler import BoellCrawler
from lfr_crawler import LfrCrawler


#
# Main
#

def main(argv):
    # Set default values
    clean = False
    quiet = False

    # Read command line arguments
    try:
        opts, args = getopt.getopt(argv, "hcq",
                                   ["help", "clean", "quiet"])
    except getopt.GetoptError as error:
        print(argv)
        print(error)
        print(
            "main.py --help --clean --quiet")
        sys.exit(2)
    for opt, arg in opts:
        if opt in ("-h", "--help"):
            print("python main.py [OPTION]...")
            print("")
            print("-h, --help                                         show this help")
            print("-c, --clean                                        clean intermediate results before start")
            print("-q, --quiet                                        do not log outputs")
            sys.exit()
        elif opt in ("-c", "--clean"):
            clean = True
        elif opt in ("-q", "--quiet"):
            quiet = True

    log_path = os.path.join(script_path, "log")
    workspace_path = os.path.join(script_path, "workspace")
    results_path = os.path.join(script_path, "content")

    # Initialize logger
    logger = LoggerFacade(log_path, console=True, file=False)

    BoellCrawler().run(logger=logger, workspace_path=workspace_path, results_path=results_path, clean=clean, quiet=quiet)
    LfrCrawler().run(logger=logger, workspace_path=workspace_path, results_path=results_path, clean=clean, quiet=quiet)


if __name__ == "__main__":
    main(sys.argv[1:])
