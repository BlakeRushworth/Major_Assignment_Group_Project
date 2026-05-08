import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from src.dataset_index import DatasetIndexer

class WorkflowService:
    def run_full_pipeline(self, selection):
        data = DatasetIndexer((selection["selected_species"]))
        data.build_dataframe()

        