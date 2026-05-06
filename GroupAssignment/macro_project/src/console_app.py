import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from src.setup_check import run_setup
from src.services.workflow_service import WorkflowService

def main() -> None:
    run_setup()                  
    workflow = WorkflowService()
    app = ConsoleApp(workflow) # we need to create a function for this
    app.run()
