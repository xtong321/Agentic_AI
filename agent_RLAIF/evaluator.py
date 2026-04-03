"""
core of RLAIF
"""

from openai import OpenAI
from config import MODEL

client = OpenAI()

class Evaluator:
    def evaluate(self, query, trajectory):
        prompt = f"""
You are a strict evaluator.

Evaluate the agent performance:

Query: {query}
Trajectory: {trajectory}

Score from 0-10 based on:
- correctness
- reasoning clarity
- efficiency

Return JSON:
{{"score": X, "feedback": "..."}}
"""

        response = client.chat.completions.create(
            model=MODEL,
            messages=[{"role": "user", "content": prompt}]
        )

        return response.choices[0].message.content