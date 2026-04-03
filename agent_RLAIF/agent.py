from openai import OpenAI
from config import MODEL
from tools import calculator, search_tool

client = OpenAI()

class Agent:
    def __init__(self):
        self.system_prompt = """
You are an AI agent using ReAct reasoning.

Format:
Thought: ...
Action: [search/calculator/finish]
Action Input: ...
Observation: ...
"""

    def run(self, query):
        trajectory = []
        messages = [{"role": "system", "content": self.system_prompt},
                    {"role": "user", "content": query}]

        for step in range(5):
            response = client.chat.completions.create(
                model=MODEL,
                messages=messages
            )

            output = response.choices[0].message.content
            messages.append({"role": "assistant", "content": output})

            trajectory.append({"step": step, "content": output})

            # simple parsing
            if "Action: finish" in output:
                return trajectory

            if "Action: search" in output:
                result = search_tool(query)
            elif "Action: calculator" in output:
                result = calculator("2+2")
            else:
                result = "No action"

            messages.append({"role": "assistant", "content": f"Observation: {result}"})

        return trajectory