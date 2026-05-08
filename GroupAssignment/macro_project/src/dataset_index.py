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
        record_folder = {}
        for file_path in self.data_dir.rglob("*"):
            if file_path.suffix.lower() not in AppConfig.SUPPORTED_EXTENSIONS:
                continue

            image = cv2.imread(str(file_path))
            if image is None:
                continue
            height, width = image.shape[:2]
            channels = image.shape[2] if len(image.shape) == 3 else 1
            label = file_path.stem
            species = file_path.parent.name
            if self.species_filter is not None and species not in self.species_filter:
                continue
            if species not in record_folder:
                record_folder[species] = []

            record_folder[species].append(
                {
                "label": label,
                "species": species,
                "width": width,
                "height": height,
                "channels": channels,
                "file_path": str(file_path)

                }
            )
        records = []
        for folder_name, info_list in record_folder.items(): # nested for loop for a dictionary
            print(f"\n{folder_name}: {len(info_list)} total images")
            for info in info_list:
                print(info)
            records.extend(info_list) # to collect all data into one flat record for data frame
        data_frame = pd.DataFrame(records)
        return data_frame
