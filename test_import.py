import sys
import traceback
import os
sys.path.append(os.getcwd())

try:
    print("Attempting to import run_triage...")
    from skills.orchestrator.langgraph_logic import run_triage
    print("Import Success")
except Exception:
    traceback.print_exc()
