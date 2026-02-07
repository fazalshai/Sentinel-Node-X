---
name: Temporal Analysis
description: "detecting 'Behavioral Shifts' by comparing new transactions against historical user baselines."
---

# Temporal Analyst Skill

## Objective
Your goal is to identify **Behavioral Shifts** in financial activity. You compare a specific "Current Transaction" against a "Historical Baseline" for the same user.

## Input Data
You will receive:
1.  **Current Transaction**: A JSON object containing `user_id`, `amount`, `currency`, `timestamp`, `ip_address`, `device_id`, and `merchant_category`.
2.  **Historical Baseline**: A summary of the user's past 6 months of activity. Examples:
    *   `avg_weekly_spend`: Average amount spent per week.
    *   `common_merchants`: List of frequently visited merchant categories.
    *   `common_ips`: List of known IP addresses.
    *   `device_fingerprints`: List of known device IDs.
    *   `typical_transaction_time`: Time ranges when the user is usually active.

## Analysis Logic (Python Implementation)

The core logic for detecting behavioral shifts is implemented in `temporal_engine.py`. The agent should conceptually follow this logic, or execute the script if environment permits.

```python
import numpy as np
import logging
from datetime import datetime
from math import radians, cos, sin, asin, sqrt

# ... (See temporal_engine.py for full imports)

def detect_behavioral_shift(current_txn, user_baseline):
    """
    Detects behavioral shifts by comparing current transaction against user baseline.
    """
    reasons = []
    shift_score = 0.0
    
    # 1. Z-Score Calculation (Amount)
    std_dev = user_baseline.get('amount_std', 1.0) 
    if std_dev == 0: std_dev = 1.0
    z_score = (current_txn['amount'] - user_baseline['amount_mean']) / std_dev
    
    # Sigmoid contribution for risk
    amount_risk_contribution = 1 / (1 + np.exp(-(z_score - 3))) 
    
    if z_score > 3:
        reasons.append(f"Amount Z-Score {z_score:.2f} (>3σ from mean {user_baseline['amount_mean']})")
        shift_score += 0.5 
        
    # 2. Geographic Velocity (Impossible Travel)
    if user_baseline.get('last_lat') is not None:
        # Haversine distance calculation (simplified)
        # ...
        # If speed > 800km/h:
        # reasons.append(f"High Velocity: {speed_kmh:.0f} km/h")
        # shift_score += 1.0 (if impossible)
        pass 
    
    # 3. Final Score Aggregation
    final_score = min(shift_score + (amount_risk_contribution * 0.5), 1.0)
    is_suspicious = final_score > 0.7
    
    return {
        "is_suspicious": is_suspicious,
        "shift_score": round(final_score, 4),
        "reasoning": "; ".join(reasons)
    }
```

### Heuristics Explained
1.  **Velocity Check**: Calculates Z-Score of the transaction amount. Deviations > 3 Sigma significantly increase the risk score.
2.  **Geo-Velocity**: data calculates speed between the previous and current transaction locations. Speeds > 800 km/h (commercial flight speed) trigger alerts.
3.  **Shift Score**: A normalized score (0-1) indicating the confidence of a behavioral shift.

## Output Format
Return a JSON object:
```json
{
  "agent": "Temporal Analyst",
  "analysis_timestamp": "ISO_DATE_STRING",
  "behavioral_shift_detected": true/false,
  "confidence_score": 0.0-1.0,
  "flags": [
    "VELOCITY_SPIKE",
    "UNRECOGNIZED_DEVICE"
  ],
  "reasoning": "User spent $5,000 on Crypto exchange from a new device in Lagos, Nigeria, while historical baseline is ~$200/week on local groceries in Dubai. High confidence of account takeover or money laundering layering phase."
}
```
