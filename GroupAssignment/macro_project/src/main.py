from src.setup_check import run_setup
from src.services.workflow_service import WorkflowService

def main() -> None:
    run_setup()                         
    workflow = WorkflowService()
    workflow.run_full_pipeline()

if __name__ == "__main__":
    main()
