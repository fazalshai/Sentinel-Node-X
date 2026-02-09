import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import time

# Total alerts to filter down
TOTAL_ALERTS = 2000
ATTACK_RATE = 0.10 # 10% Attack Rate

# Use the current timestamp to make every attack unique
def get_dynamic_attack():
    return {
        "amount": np.random.randint(20000, 99999),
        "loc": np.random.choice(["Russia", "North Korea", "Iran"]),
        "timestamp": datetime.now().isoformat(),
        # Z-Score will be calculated by backend, but we inject values that trigger it
        "mean_amt": 100, 
        "std_amt": 10,  # Tiny std dev -> Huge Z-Score
        "last_loc": "Dubai",
        "last_time": (datetime.now() - timedelta(minutes=1)).isoformat(), # Velocity Violation
        "type": "WITHDRAWAL_QUICK_FLIP",
        "ip_address": "89.14.22.11"
    }

rows = []
for i in range(TOTAL_ALERTS):
    # FORCE first 100 to be attacks (Deterministic Demo)
    is_attack = i < 100 
    
    if is_attack:
        # Generate a fresh, unique attack
        attack_data = get_dynamic_attack()
        rows.append(attack_data)
    else:
        # NOISE (Normal Behavior)
        rows.append({
            "amount": np.random.randint(50, 150), 
            "loc": "Dubai", 
            "timestamp": datetime.now().isoformat(),
            "mean_amt": 500, 
            "std_amt": 100, 
            "last_loc": "Dubai", 
            "last_time": (datetime.now() - timedelta(days=1)).isoformat(),
            "type": "POS_PAYMENT",
            "ip_address": f"10.0.0.{np.random.randint(1, 255)}"
        })

# Save to csharp_client so the .NET runner sees it immediately
output_path = "csharp_client/attack_data.csv"
pd.DataFrame(rows).to_csv(output_path, index=False)
print(f"Dataset generated at {output_path} with {int(TOTAL_ALERTS * ATTACK_RATE)} dynamic attacks.")
