import os
import requests
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage

from dotenv import load_dotenv
load_dotenv()
import os
print(os.getenv("OPENAI_API_KEY"))


llm = ChatOpenAI(model="gpt-4o-mini")

resp = llm.invoke([
    SystemMessage(content="You are a testing assistant"),
    HumanMessage(content="Testing whether LangChain is working correctly")
])

print(resp)