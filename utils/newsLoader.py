import os
from glob import glob
from datetime import datetime

NEWS_DIR = "app/content/news"


def loadNews():
    newsItems = []

    for filePath in glob(os.path.join(NEWS_DIR, "*.md")):
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
            newsItems.append(metadata)

        except Exception as e:
            print(f"Error parsing {filePath}: {e}")

    newsItems.sort(key=lambda x: x["date"], reverse=True)
    return newsItems


def loadSingleNews(slug):
    path = os.path.join(NEWS_DIR, f"{slug}.md")
    metadata = {}
    if not os.path.exists(path):
        return None

    with open(path, "r", encoding="utf-8") as f:
        lines = f.read()

    try:
        for line in lines.splitlines():
            if ':' in line:
                key, value = line.split(':', 1)
                metadata[key.strip()] = value.strip()

        metadata["date"] = datetime.strptime(metadata["date"], "%Y-%m-%d")

    except Exception as e:
        print(f"Error parsing {path}: {e}")

    return metadata
