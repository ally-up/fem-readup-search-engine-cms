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
    def run(self, logger, data_path, results_path, type, clean=False):

        # Make results path
        os.makedirs(os.path.join(results_path, type), exist_ok=True)

        # Clean results path
        if clean:
            files = glob.glob(os.path.join(results_path, type, "*"))
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
                        key = line.split("=", 1)[0].strip().replace("\"", "").replace("'", "")
                        value = line.split("=", 1)[1].strip().replace("\"", "").replace("'", "")
                        value = str(value)

                        if key == "languages":
                            values[key] = value.replace("[", "").replace("]", "").split(",")
                        else:
                            values[key] = value

                # Add ID based on file name
                values["id"] = file_base_name

                # Check for type
                if "type" in values and values["type"] == type:

                    # Write json file
                    with open(os.path.join(results_path, type, f"{file_base_name}.json"), 'w') as json_file:
                        json.dump(values, json_file)
