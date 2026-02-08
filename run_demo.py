import os
import subprocess
import time
import sys

def kill_port(port):
    try:
        cmd = f"lsof -t -i:{port} | xargs kill -9"
        subprocess.run(cmd, shell=True, stderr=subprocess.DEVNULL, stdout=subprocess.DEVNULL)
        print(f"🧹 Port {port} cleared.")
    except Exception:
        pass

def main():
    print("🚀 SITUATION ROOM: Initializing Sentinel-Node X Demo Sequence...")
    
    # 1. Kill Zombies
    kill_port(8000)
    time.sleep(1)
    
    # 2. Start Backend using the current python environment's uvicorn
    # We use subprocess.Popen to let it run in background but keep this script alive if needed
    # Or better, just replace this process
    print("🔥 Igniting Core Engine (Uvicorn)...")
    
    # Check if uvicorn is available in path, or use module execution
    # FORCE VENV usage to avoid "No module named uvicorn"
    venv_python = "./.venv/bin/python"
    cmd = [venv_python, "-m", "uvicorn", "main:app", "--host", "127.0.0.1", "--port", "8000", "--workers", "1", "--log-level", "error"]
    
    try:
        # We run it and wait
        subprocess.run(cmd)
    except KeyboardInterrupt:
        print("\n🛑 Demo Stopped.")

if __name__ == "__main__":
    main()
