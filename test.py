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
    SystemMessage(content="你是一个测试助手"),
    HumanMessage(content="测试一下 LangChain 是否正常")
])

print(resp)