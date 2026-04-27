from langchain.chat_models import ChatOpenAI

class DiagnosticAgent:
    def __init__(self, model_path):
        self.llm = ChatOpenAI(model=model_path)

    def solve(self, task):
        # record: (Thought -> Action -> Observation)
        trajectory = []
        # implementation: LLM generate thoight process and decide call which tools
        # ... 
        return trajectory