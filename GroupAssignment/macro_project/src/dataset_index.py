import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import cv2
import pandas as pd
from src.config import AppConfig

class DatasetIndexer:
    """Scan the dataset folder and build a tabular image index."""

    def __init__(self, selected, data_dir: Path = AppConfig.RAW_DATA_DIR) -> None:
        self.data_dir = data_dir
        self.species_filter = selected
        if AppConfig.DATASET_DIR.exists():
            self.data_dir = AppConfig.DATASET_DIR
        else:
            self.data_dir = AppConfig.RAW_DATA_DIR
    
    def build_dataframe(self) -> pd.DataFrame:
        """Return one row per image with file path, label, and dimensions."""
        records = []
        for file_path in self.data_dir.rglob("*"):
            if file_path.suffix.lower() not in AppConfig.SUPPORTED_EXTENSIONS:
                continue

            image = cv2.imread(str(file_path))
            if image is None:
                continue
            height, width = image.shape[:2]
            channels = image.shape[2] if len(image.shape) == 3 else 1
            label = file_path.parent.name
            if self.species_filter is not None and label not in self.species_filter:
                continue

            records.append(
                {
                "file_path": str(file_path),
                "label": label,
                "width": width,
                "height": height,
                "channels": channels,
                }
            )
        print(records)
        return pd.DataFrame(records)
