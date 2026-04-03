"""
Learning Loop
"""

from agent import Agent
from evaluator import Evaluator
from memory import Memory
import json

agent = Agent()
evaluator = Evaluator()
memory = Memory()

queries = [
    "Find top EV companies and compare them",
    "What is Tesla revenue?"
]

for epoch in range(3):
    print(f"\n=== Epoch {epoch} ===")

    for q in queries:
        traj = agent.run(q)
        result = evaluator.evaluate(q, traj)

        print("Query:", q)
        print("Trajectory:", traj)
        print("Eval:", result)

        try:
            parsed = json.loads(result)
            score = parsed["score"]
        except:
            score = 5

        memory.add(traj, score)