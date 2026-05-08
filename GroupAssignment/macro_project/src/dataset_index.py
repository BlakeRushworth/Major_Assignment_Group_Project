import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import cv2
import pandas as pd

from src.config import AppConfig


class DatasetIndexer:
    """Scan the dataset folder and build a tabular image index."""

    def __init__(self, data_dir: Path = AppConfig.RAW_DATA_DIR, selected_species = None ) -> None:
        self.data_dir = Path(data_dir)
        if AppConfig.DATASET_DIR.exists():
            self.data_dir = AppConfig.DATASET_DIR
        else: 
            self.data_dir = AppConfig.RAW_DATA_DIR
        if isinstance(selected_species, dict):
            self.selected_species = selected_species.get("selected_species", [])
        else:
            self.selected_species = selected_species or []

    def build_dataframe(self) -> pd.DataFrame:
        """Return one row per image with file path, label, and dimensions."""

        records = []

        for file_path in self.data_dir.rglob("*"):

            # Skip non-image files
            if file_path.suffix.lower() not in AppConfig.SUPPORTED_EXTENSIONS:
                continue

            # Load image
            image = cv2.imread(str(file_path))

            # Skip unreadable images
            if image is None:
                continue

            # Species label = parent folder name
            label = file_path.parent.name

            # Skip species not selected by the user
            
            clean_selected = [s.strip().lower() for s in self.selected_species]

            if label.strip().lower() not in clean_selected:
                continue
            # Image metadata
            height, width = image.shape[:2]
            channels = image.shape[2] if len(image.shape) == 3 else 1

            # Add record
            records.append(
                {
                    "file_path": str(file_path),
                    "label": label,
                    "width": width,
                    "height": height,
                    "channels": channels,
                }
            )

        print(f"Indexed {len(records)} images")
        df = pd.DataFrame(records)
        print(df["label"].unique())
        return df