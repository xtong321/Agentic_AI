JUDGE_PROMPT = """
You are a Senior Systems Architect. Please evaluate the following agent's troubleshooting trajectory.
Evaluation Criteria:
1. Accuracy: Did it identify the root cause?
2. Efficiency: Did it use the fewest steps? (No redundant log queries)

Trajectory A: {traj_a}
Trajectory B: {traj_b}

Please output your preference (Chosen/Rejected) and provide a justification.
"""

def generate_preferences(traj_a, traj_b):
    # call LLM to annotate preference
    # return DPO training format: {"prompt": task, "chosen": traj_a, "rejected": traj_b}
    pass