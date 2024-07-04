from datetime import datetime
from pathlib import Path


class PathModel:
    def __init__(self, source: str, dist: str):
        self.source = source
        self.dist = dist


def filePath(source: str, dist: str) -> PathModel:
    base_dir = Path(__file__).resolve().parent.parent
    source_path = base_dir / f"source/{source}.xlsx"
    dist_path = base_dir / f"download/{dist}.xlsx"

    return PathModel(source=str(source_path), dist=str(dist_path))


def today_or_yesterday(today, yesterday):
    current_hour = datetime.now().hour
    if current_hour > 10:
        return today
    else:
        return yesterday
