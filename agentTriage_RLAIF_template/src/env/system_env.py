class SystemEnv:
    def __init__(self):
        self.status = "Issue: GPU Memory Leak in Node_01"
        self.logs = ["10:00:01 - Info: System Start", "10:05:20 - Error: Out of Memory"]

    def run_tool(self, action, params):
        """simulate tool calling, such as: check_logs, inspect_gpu, get_config"""
        if action == "check_logs":
            return self.logs
        if action == "inspect_gpu":
            return "Node_01: Process 5402 consuming 98% VRAM"
        return "Unknown command"