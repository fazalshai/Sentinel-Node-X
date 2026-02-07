import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# Total alerts to filter down to 50
TOTAL_ALERTS = 2000
ATTACK_RATE = 0.025 # Exact 2.5% to hit the 50-case target

rows = []
for i in range(TOTAL_ALERTS):
    is_attack = np.random.random() < ATTACK_RATE
    if is_attack:
        scenario = np.random.choice(['Geopolitical', 'Structuring'])
        
        if scenario == 'Geopolitical':
            # Attack A: Huge amount, high velocity, suspicious loc (NK/Russia)
            rows.append({
                "amount": np.random.randint(20000, 100000), 
                "loc": "North Korea" if i % 2 == 0 else "Russia",
                "timestamp": datetime.now().isoformat(), 
                "mean_amt": 100, 
                "std_amt": 20,
                "last_loc": "Dubai", 
                "last_time": (datetime.now() - timedelta(minutes=5)).isoformat(),
                "type": "TRANSFER",
                "ip_address": "89.14.22.11" # Known Bad Actor IP
            })
        else:
            # Attack B: The "0.01 Profit" Laundering (Deriv Specific)
            # Deposit $500 -> Withdrawal $500.01 in 10 mins
            rows.append({
                "amount": 500.01, 
                "loc": "Dubai",
                "timestamp": datetime.now().isoformat(), 
                "mean_amt": 5000, # User usually trades big, but this is micro
                "std_amt": 1000,
                "last_loc": "Dubai", 
                "last_time": (datetime.now() - timedelta(minutes=10)).isoformat(),
                "type": "WITHDRAWAL_QUICK_FLIP",
                "ip_address": "192.168.1.105" # Suspicious Shared IP
            })
    else:
        # Noise: Standard Dubai spending
        rows.append({
            "amount": np.random.randint(50, 150), 
            "loc": "Dubai", 
            "timestamp": datetime.now().isoformat(),
            "mean_amt": 100, 
            "std_amt": 20, 
            "last_loc": "Dubai", 
            "last_time": (datetime.now() - timedelta(days=1)).isoformat(),
            "type": "POS_PAYMENT",
            "ip_address": f"10.0.0.{np.random.randint(1, 255)}" # Normal IP
        })

# Save to csharp_client so the .NET runner sees it immediately
output_path = "csharp_client/attack_data.csv"
pd.DataFrame(rows).to_csv(output_path, index=False)
print(f"Dataset generated at {output_path} with {int(TOTAL_ALERTS * ATTACK_RATE)} hidden attacks.")
