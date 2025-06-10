import os
from glob import glob
from datetime import datetime

PEOPLE_DIR = "app/content/people"


def loadPeoples():
    peopleItems = []

    for filePath in glob(os.path.join(PEOPLE_DIR, "*.md")):
        with open(filePath, "r", encoding="utf-8") as f:
            lines = f.read()

        try:
            metadata = {}
            for line in lines.splitlines():
                if ':' in line:
                    key, value = line.split(':', 1)
                    metadata[key.strip()] = value.strip()

            metadata['slug'] = os.path.basename(filePath).split(".")[0]
            metadata["filename"] = os.path.basename(filePath)

            peopleItems.append(metadata)

        except Exception as e:
            print(f"Error parsing {filePath}: {e}")

    return peopleItems
