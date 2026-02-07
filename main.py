from fastapi import FastAPI, BackgroundTasks, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import Dict, Any
import time
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(title="Sentinel-Node X: High-Concurrency Gateway")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000", "*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Production-grade request validation
class TriageRequest(BaseModel):
    transaction: Dict[str, Any] = Field(..., description="Details of the current transaction")
    user_baseline: Dict[str, Any] = Field(..., description="Historical behavioral baseline of the user")

# Global Stats for "War Room" Dashboard
STATS = {
    "processed": 0,
    "suspicious": 0,
    "cases": [] # Store details of the 50 bad actors
}

@app.get("/health")
def health_check():
    return {"status": "Active", "uptime": time.time()}

@app.get("/stats")
def get_stats():
    """Live stats for the dashboard counter"""
    return STATS

@app.post("/reset")
def reset_stats():
    """Reset global stats for a fresh demo run"""
    global STATS
    STATS["processed"] = 0
    STATS["suspicious"] = 0
    STATS["cases"] = []
    return {"status": "Stats Reset", "stats": STATS}

@app.get("/graph")
def get_graph():
    """
    Generate Network Graph for 'Mind-Blowing' Fraud Ring Visualization.
    Uses Star Topology: IP Addresses are Hubs, Cases are Spokes.
    """
    nodes = []
    links = []
    
    # Track unique IPs to create Hub nodes
    seen_ips = {}
    
    for case in STATS["cases"]:
        # 1. Add Case Node (Spoke)
        nodes.append({
            "id": case["id"],
            "type": case["type"],
            "val": 5, # Smaller spokes
            "group": "case"
        })
        
        # 2. Add/Find IP Node (Hub)
        ip = case.get("ip", "N/A")
        if ip != "N/A":
            if ip not in seen_ips:
                nodes.append({
                    "id": ip,
                    "type": "IP_ADDRESS",
                    "val": 15, # Big Hub
                    "group": "ip"
                })
                seen_ips[ip] = True
            
            # 3. Link Spoke to Hub
            links.append({
                "source": case["id"],
                "target": ip
            })
                
    return {"nodes": nodes, "links": links}

@app.post("/triage")
def triage_endpoint(request: TriageRequest, background_tasks: BackgroundTasks):
    """
    High-concurrency triage endpoint backed by 4-worker Uvicorn.
    """
    try:
        # Access data safely via Pydantic model
        data = request.model_dump()
        tx_data = data['transaction']
        
        # Inject Strict Baseline if missing (to ensure 'Soft Computing' metrics work for Demo)
        base_data = data['user_baseline']
        if not base_data or not base_data.get('mean_amt'):
            base_data = {
                "mean_amt": 500,        # Low average to make $36k huge
                "std_amt": 200,         # Low deviation
                "last_loc": "Dubai",    # Default location
                "last_time": "2024-01-01T00:00:00"
            }
        
        # Log the event asynchronously
        print(f"DEBUG INCOMING: Tx={tx_data} | Base={base_data}")
        background_tasks.add_task(print, f"Processing Event: {tx_data.get('timestamp', 'NOW')}")
        
        # Trigger the LangGraph State Machine
        from skills.orchestrator.langgraph_logic import run_triage
        result = run_triage(tx_data, base_data)
        
        # Update Global Stats
        STATS["processed"] += 1
        if result.get("is_suspicious"):
            STATS["suspicious"] += 1
            # Store case details for the "Clickable List"
            STATS["cases"].append({
                "id": f"CASE-{STATS['suspicious']:03d}",
                "timestamp": tx_data.get('timestamp'),
                "amount": tx_data.get('amount'),
                "type": tx_data.get('type', 'TRANSFER'),
                "reason": result.get('temporal_result', {}).get('reasoning', 'Unknown'),
                "ip": tx_data.get('ip_address', 'N/A')
            })
        
        return result
        
    except Exception as e:
        # Graceful error handling for the client
        raise HTTPException(status_code=500, detail=f"Triage Engine Error: {str(e)}")

@app.post("/simulate")
def trigger_simulation(background_tasks: BackgroundTasks):
    """
    Triggers the C# 'Hammer' Stress Test from the UI.
    Runs 'dotnet run' in the csharp_client directory.
    """
    import subprocess
    
    def run_csharp_client():
        print("🔨 UI Triggered Simulation: Starting C# Client...")
        try:
            # Run dotnet run in the csharp_client folder
            subprocess.run(["dotnet", "run"], cwd="csharp_client", check=True)
            print("✅ UI Triggered Simulation: Complete.")
        except Exception as e:
            print(f"❌ UI Triggered Simulation Failed: {str(e)}")

    background_tasks.add_task(run_csharp_client)
    return {"status": "Simulation Started", "message": "The Hammer is striking... Watch the counter!"}

if __name__ == "__main__":
    import uvicorn
    # Allow running directly with 'python main.py' for debugging
    uvicorn.run(app, host="0.0.0.0", port=8000)
