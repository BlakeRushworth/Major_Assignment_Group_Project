import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from src.setup_check import run_setup
from src.menu_system import main_menu
from src.services.workflow_service import WorkflowService
 
def main() -> None:
    selection: dict = run_setup()                    
    workflow = WorkflowService()
    workflow.run_full_pipeline(selection)
    main_menu()


if __name__ == "__main__":
    main()
