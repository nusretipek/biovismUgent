import os
from glob import glob
from datetime import datetime

PUBLICATION_DIR = "app/content/publications"


def loadPublications():
    publicationItems = []

    for filePath in glob(os.path.join(PUBLICATION_DIR, "*.md")):
        with open(filePath, "r", encoding="utf-8") as f:
            lines = f.read()

        try:
            metadata = {}
            for line in lines.splitlines():
                if ':' in line:
                    key, value = line.split(':', 1)
                    metadata[key.strip()] = value.strip()

            metadata["date"] = datetime.strptime(metadata["date"], "%Y-%m-%d")
            metadata['slug'] = os.path.basename(filePath).split(".")[0]
            metadata["filename"] = os.path.basename(filePath)

            publicationItems.append(metadata)

        except Exception as e:
            print(f"Error parsing {filePath}: {e}")

    return publicationItems
