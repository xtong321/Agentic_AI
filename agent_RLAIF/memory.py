"""
pool/memory of experience
"""

class Memory:
    def __init__(self):
        self.good_trajectories = []

    def add(self, traj, score):
        if score >= 7:
            self.good_trajectories.append(traj)

    def get_examples(self):
        return self.good_trajectories[-3:]