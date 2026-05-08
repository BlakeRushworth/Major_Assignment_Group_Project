import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from src.setup_check import run_setup
from src.services.workflow_service import WorkflowService
 
def main() -> None:
    selection: dict = run_setup() 
    #print(selection["selected_species"])                       
    workflow = WorkflowService()
    workflow.run_full_pipeline(selection)

if __name__ == "__main__":
    main()
