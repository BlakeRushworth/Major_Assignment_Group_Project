import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from src.dataset_index import DatasetIndexer

class WorkflowService:
    def __init__(self):
        self.indexer = None

    def initialize_data(self, species_list):
        # Create the indexer and build the dataframe once
        self.indexer = DatasetIndexer(species_list)
        return self.indexer.build_dataframe()

    def display_summary(self, df):
        # Bridge to the function that already exists in DatasetIndexer
        if self.indexer:
            self.indexer.get_summary(df)
        