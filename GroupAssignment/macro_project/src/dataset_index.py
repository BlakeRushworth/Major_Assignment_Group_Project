import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import cv2
import re
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
            # Skip non-image files
            if file_path.suffix.lower() not in AppConfig.SUPPORTED_EXTENSIONS:
                continue

            # Load image
            image = cv2.imread(str(file_path))

            # Skip unreadable images
            if image is None:
                continue

            # Species label = parent folder name
            species = file_path.parent.name

            # Image metadata
            height, width = image.shape[:2]
            channels = image.shape[2] if len(image.shape) == 3 else 1
            label = file_path.stem

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
        for folder_name, info_list in record_folder.items(): # loop for a dictionary
            records.extend(info_list) # to collect all data into one flat record for data frame
        data_frame = pd.DataFrame(records)
        return data_frame

    def get_summary(self, df: pd.DataFrame):
        """Prints a clean summary of the dataset grouping by species."""
        if df.empty:
            print("No data available to summarize.")
            return

        # groupby() is used to find a specific column and perform an action
        summary = df.groupby('species').agg({
            'label': 'count',      # Total images
            # the keyword: 'mean' tells panda to run (sum/count)
            'width': 'mean',       # Average width
            'height': 'mean',      # Average height
            'file_path': 'first'   # Just take the first path as an example
        }).reset_index()

        print("\n" + "="*50)
        print("DATASET SUMMARY")
        print("="*50)

        for _, row in summary.iterrows():
            # Clean the label (remove numbers if they are like 'oak_01')
            # This regex keeps only alphabetic characters
            clean_name = re.sub(r' .*', '', str(row['species']))
            print(f"\nSpecies: {row['species']}")
            print(f" - Name:            {clean_name}")
            print(f" - Total Images:    {row['label']}")
            print(f" - Avg Dimensions:  {row['width']:.1f}x{row['height']:.1f}")
            print(f" - Base Filepath:   {Path(row['file_path']).parent}")
        print("="*50)