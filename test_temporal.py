from skills.temporal_analyst.temporal_engine import detect_behavioral_shift
import numpy as np
from datetime import datetime, timedelta

# Mock Data
dp_iso = datetime(2023, 10, 27, 10, 0, 0).isoformat()
baseline = {
    'mean_amt': 100.0,
    'std_amt': 20.0,
    'last_loc': 'Dubai',
    'last_time': dp_iso
}

# Case 1: Normal
txn_normal = {
    'amount': 110.0,
    'loc': 'Dubai', 
    'timestamp': datetime(2023, 10, 27, 11, 0, 0).isoformat()
}

# Case 2: High Amount (Spike) -> Z-Score = (5000 - 100)/20 = 245
txn_spike = {
    'amount': 5000.0, 
    'loc': 'Dubai',
    'timestamp': datetime(2023, 10, 27, 12, 0, 0).isoformat()
}

# Case 3: Velocity (London 1h later)
txn_travel = {
    'amount': 100.0,
    'loc': 'London',
    'timestamp': datetime(2023, 10, 27, 11, 0, 0).isoformat() # 1 hour later
}

print("--- Test Results ---")
print(f"Normal: {detect_behavioral_shift(txn_normal, baseline)}")
print(f"Spike: {detect_behavioral_shift(txn_spike, baseline)}")
print(f"Travel: {detect_behavioral_shift(txn_travel, baseline)}")
