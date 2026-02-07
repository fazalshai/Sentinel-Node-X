# Orchestrator Skill: Sentinel-Node X Autonomous Triage

## Objective
Reduce false-positive alert fatigue for Deriv Compliance teams by 97.5%.

## [cite_start]LangGraph State Machine Logic [cite: 11, 20]
1. **Evidence Node:** Pull metadata (IP, Location, Amount) using the `evidence_agent`.
2. **Temporal Node:** Pass data to `temporal_analyst` to calculate 'Behavioral Shift'.
3. **Compliance Node:** If Shift Score > 2.5, trigger `compliance_radar` via Gemini Grounding to check UAE AML rules.
4. **Conclusion Node:** Synthesize logs into a high-confidence JSON Case Summary.

## Technical Signal
- [cite_start]Built for 99.9% availability on AKS[cite: 21].
- [cite_start]Handles high-throughput event-driven architecture[cite: 13, 34].
