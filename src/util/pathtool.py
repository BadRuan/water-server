from pathlib import Path
from core.model import PathModel


def filePath(source: str, dist: str) -> PathModel:
    # 获取当前文件路径
    current_file_path = Path(__file__).resolve()
    # 获取当前文件的所在目录
    current_dir = current_file_path.parent.parent
    file_path = current_dir / f"source/{source}.xlsx"
    save_path = current_dir / f"dist/{dist}.xlsx"
    # 完整路径
    source_filename = str(file_path)
    dist_filename = str(save_path)
    return PathModel(source=source_filename, dist=dist_filename)
