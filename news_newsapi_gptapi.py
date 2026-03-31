import os
import requests
from datetime import datetime, timedelta
from dotenv import load_dotenv

from langchain_openai import ChatOpenAI
# from langchain.schema import SystemMessage, HumanMessage
from langchain_core.messages import SystemMessage, HumanMessage

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
NEWS_API_KEY = os.getenv("NEWS_API_KEY")


# ---------- 1. retrieve tech news of today ----------
def fetch_tech_news(page_size: int = 10):
    """
    use NewsAPI to retrieve today's tech news, title+summary+link
    """
    if not NEWS_API_KEY:
        raise ValueError("! Pls set NEWS_API_KEY in .env")

    today = datetime.utcnow().date()
    #today = datetime.datetime.now(datetime.UTC)
    from_date = today - timedelta(days=1)

    url = "https://newsapi.org/v2/top-headlines"
    params = {
        "category": "technology",
        "language": "en",
        "pageSize": page_size,
        "from": from_date.isoformat(),
        "apiKey": NEWS_API_KEY,
    }

    resp = requests.get(url, params=params)
    resp.raise_for_status()
    data = resp.json()

    articles = data.get("articles", [])
    if not articles:
        return "! No tech news found today."

    lines = []
    for i, a in enumerate(articles, start=1):
        title = a.get("title", "")
        desc = a.get("description", "") or ""
        url = a.get("url", "")
        lines.append(f"{i}. {title}\n   {desc}\n   Link: {url}\n")

    return "\n".join(lines)

# ---------- 2. construct LLM（LangChain） ----------
def get_llm():
    if not OPENAI_API_KEY:
        raise ValueError("! Pls set OPENAI_API_KEY in .env")
    return ChatOpenAI(
        model="gpt-4o-mini",  # or any model you can access
        temperature=0.3,
    )

# ---------- 3. generate 'today's tech news brief ----------
def generate_daily_brief(news_text: str) -> str:
    llm = get_llm()
    system = SystemMessage(
        content=(            
            "You are a personal technology news assistant, skilled at summarizing English technology news,"
            "in concise, structured language, targeting readers with a technical background."            
        )
    )
    user = HumanMessage(
        content=(
            "There is English technology news list below, please: \n"
            "1）create a 'Today's Tech Highlights Brief'; \n"
            "2）Sort by importance; \n"
            "3）Describe the event and its impact in 1-2 sentences for each item; \n"
            "4）Finally, provide 3 directions you believe are worth pursuing in depth. \n\n"
            f"News List：\n{news_text}"
        )
    )
    resp = llm.invoke([system, user])
    return resp.content

# ---------- 4. support further conversation ----------
def chat_with_assistant(context_brief: str):
    """
    Simple REPL: You can continue to ask questions based on today's briefing
    """
    llm = get_llm()
    system = SystemMessage(
        content=(           
            "You are a personal tech news assistant. The user has already viewed your generated 'Today's Tech Highlights Briefing.'"
            "The user will then ask further questions based on this briefing. You need to: \n"
            "1) Provide more in-depth explanations based on the briefing content; \n"
            "2) If necessary, you can reasonably infer background information, but be sure to indicate that it is an inference; \n"
            "3) Do not fabricate specific figures or internal company information."
        )
    )

    print("\n===== Today's Tech Highlights Brief =====\n")
    print(context_brief)
    print("\n===== You can ask questions now (type q to exit) =====\n")

    history = [system, HumanMessage(content="this is the new list before: \n" + context_brief)]

    while True:
        user_input = input("You: ").strip()
        if user_input.lower() in ["q", "quit", "exit"]:
            print("Assistant: Okay, that's all for today")
            break

        history.append(HumanMessage(content=user_input))
        resp = llm.invoke(history)
        print("\nAssistant: ", resp.content, "\n")
        history.append(resp)

# ---------- 5. main route ----------
def main():
    print("=> In retrieving today's tech news...")
    news_text = fetch_tech_news(page_size=10)

    print("=> In generating today's tech news briefing...")
    brief = generate_daily_brief(news_text)

    # to interactive mode
    chat_with_assistant(brief)

if __name__ == "__main__":
    main()
