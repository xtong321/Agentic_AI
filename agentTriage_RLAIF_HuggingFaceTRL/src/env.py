"""
Define a class that encapsulates faults and tools, demonstrating an understanding of Agent-Environment Interaction.
"""

import random

class SystemTriageEnv:
    def __init__(self):
        self.reset()

    def reset(self):
        # simulate failure scenarios
        scenarios = [
            {"issue": "GPU_MEM_LEAK", "root_cause": "Process 5402", "logs": "Err: VRAM Full"},
            {"issue": "NETWORK_LATENCY", "root_cause": "Port 8080 congestion", "logs": "Warn: High Latency"}
        ]
        self.current_scenario = random.choice(scenarios)
        self.steps = 0
        return f"System Alert: {self.current_scenario['issue']}"

    def step(self, action, params=None):
        self.steps += 1
        if action == "check_logs":
            return self.current_scenario['logs']
        if action == "inspect_process":
            return f"Found activity on {self.current_scenario['root_cause']}"
        if action == "final_report":
            return f"Reported: {params}"
        return "Command not found."