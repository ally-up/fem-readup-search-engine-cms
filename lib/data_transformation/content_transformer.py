import glob
import json
import os
from pathlib import Path

from tqdm import tqdm
from tracking_decorator import TrackingDecorator


#
# Main
#

class ContentTransformer:

    @TrackingDecorator.track_time
    def run(self, logger, data_path, results_path, clean=False):

        # Make results path
        os.makedirs(results_path, exist_ok=True)

        # Clean results path
        if clean:
            files = glob.glob(os.path.join(results_path, "*"))
            for f in files:
                os.remove(f)

        # Iterate over markdown files
        for file_path in tqdm(iterable=list(Path(data_path).rglob("*.md")), unit="file", desc="Transform markdown files"):

            file_name = os.path.basename(file_path)
            file_base_name = file_name.replace(".md", "")

            with open(file_path, encoding="utf-8") as f:

                values = {}

                # Extract keys and values from md file
                for line in f.readlines():
                    if "=" in line:
                        key = line.split("=")[0].strip().replace("\"", "").replace("'", "")
                        value = line.split("=")[1].strip().replace("\"", "").replace("'", "")
                        value = str(value)

                        if key == "sports" or key == "types":
                            values[key] = value.replace("[", "").replace("]", "").split(",")
                        else:
                            values[key] = value

                    # Add ID based on file name
                    values["id"] = file_base_name

                # Write json file
                with open(os.path.join(results_path, f"{file_base_name}.json"), 'w') as json_file:
                    json.dump(values, json_file)
