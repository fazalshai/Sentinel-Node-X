---
name: Evidence Retrieval
description: "Fetching mock transaction data and user context."
---

# Evidence Agent Skill

## Objective
Retrieve the "raw material" for an investigation. In a real system, you would query SQL/NoSQL databases. Here, you will **generate realistic mock data**.

## Mock Data Generation Rules
When asked for a transaction or user profile, generate a JSON object with the following properties. Use `random` logic (simulated) to create variety.

### 1. Transaction Data
*   `transaction_id`: UUID string.
*   `amount`: Float (e.g., 500.00 to 50000.00).
*   `currency`: "USD", "AED", "EUR", or "GBP".
*   `timestamp`: ISO 8601 recent timestamp.
*   `merchant`: Name of a business (e.g., "Binance", "Carrefour", "Unknown LLC", "HighRollers Casino").
*   `merchant_category`: "Groceries", "Crypto", "Gambling", "Electronics", "Consulting".
*   `ip_address`: IPv4 address.
*   `device_id`: alphanumeric string.

### 2. User Profile (Historical Context)
*   `user_id`: string (e.g., "user_8842").
*   `account_age_days`: integer.
*   `risk_score_v1`: integer (0-100 legacy score).
*   `kyc_status`: "Verified", "Pending", "None".
*   `nationality`: Country code (e.g., "AE", "IN", "US", "RU").

## Output Format
Return the raw JSON data clearly labeled:

```json
{
  "data_type": "evidence_package",
  "transaction": { ... },
  "user_profile": { ... }
}
```
