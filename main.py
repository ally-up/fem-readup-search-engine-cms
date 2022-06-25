import getopt
import os
import sys

file_path = os.path.realpath(__file__)
script_path = os.path.dirname(file_path)

# Make library available in path
library_paths = [
    os.path.join(script_path, 'lib'),
    os.path.join(script_path, 'lib', 'data_transformation'),
    os.path.join(script_path, 'lib', 'data_upload'),
    os.path.join(script_path, 'lib', 'log'),
]

for p in library_paths:
    if not (p in sys.path):
        sys.path.insert(0, p)

# Import library classes
from logger_facade import LoggerFacade
from content_transformer import ContentTransformer
from data_uploader_firebase_firestore import FirebaseFirestoreUploader


#
# Main
#

def main(argv):
    # Set default values
    clean_data = True

    # Read command line arguments
    try:
        opts, args = getopt.getopt(argv, "h", ["help"])
    except getopt.GetoptError:
        print(
            "main.py --help")
        sys.exit(2)
    for opt, arg in opts:
        if opt in ("-h", "--help"):
            print("main.py")
            print("--help                           show this help")
            sys.exit()

    # Set paths
    log_path = os.path.join(script_path, "log")
    data_path = os.path.join(script_path, "content")
    results_path = os.path.join(script_path, "results")

    # Initialize logger
    logger = LoggerFacade(log_path, console=True, file=False)

    #
    # Transformation
    #

    ContentTransformer().run(
        logger=logger,
        data_path=os.path.join(data_path),
        results_path=os.path.join(results_path),
        clean=clean_data
    )

    #
    # Upload
    #

    FirebaseFirestoreUploader().run(
        logger=logger,
        results_path=os.path.join(results_path),
        clean=clean_data
    )


if __name__ == "__main__":
    main(sys.argv[1:])
