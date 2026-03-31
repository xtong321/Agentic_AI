"""
"""
import os
import feedparser
from datetime import datetime
from dotenv import load_dotenv

from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# ---------- 1. use Google News RSS to pull tech news ----------
def fetch_google_news_rss(max_items: int = 10):
    """
    using Google News RSS to retrieve tech news (free)
    """
    RSS_URL = (
        "https://news.google.com/rss/topics/"
        "CAAqBwgKMJmAmgsw9Zz-Aw?hl=en-US&gl=US&ceid=US:en"
    )

    feed = feedparser.parse(RSS_URL)
    entries = feed.entries[:max_items]

    if not entries:
        return "No tech news found today."

    lines = []
    for i, entry in enumerate(entries, start=1):
        title = entry.title
        summary = entry.summary if hasattr(entry, "summary") else ""
        link = entry.link
        published = entry.published if hasattr(entry, "published") else ""

        lines.append(
            f"{i}. {title}\n"
            f"   {summary}\n"
            f"   Published: {published}\n"
            f"   Link: {link}\n"
        )

    return "\n".join(lines)

# ---------- 2. construct LLM ----------
def get_llm():
    return ChatOpenAI(
        model="gpt-4o-mini",
        temperature=0.3,
    )

# ---------- 3. generate 'today tech news brief ----------
def generate_daily_brief(news_text: str) -> str:
    llm = get_llm()
    system = SystemMessage(
        content=(
            "You are a personal technology news assistant. "
            "Your job is to summarize English tech news into a concise, structured, "
            "professional daily briefing suitable for a tech‑savvy audience."
        )
    )
    user = HumanMessage(
        content=(
            "Here is today's list of English technology news. Please:\n"
            "1) Produce a structured **English** daily tech briefing.\n"
            "2) Prioritize items by importance.\n"
            "3) For each item, provide 1–2 sentences explaining the event and its impact.\n"
            "4) End with 5 key trends or developments worth monitoring.\n\n"
            f"News list:\n{news_text}"
        )
    )
    resp = llm.invoke([system, user])
    return resp.content


# ---------- 4. support further conversation and asking ----------
def chat_with_assistant(context_brief: str):
    llm = get_llm()
    system = SystemMessage(
        content=(            
            "You are a personal tech news assistant. The user has already viewed your generated 'Today's Tech Highlights Briefing.'"
            "The user will then ask further questions based on this briefing. You need to:\n"
            "1) Provide more in-depth explanations based on the briefing content;\n"
            "2) If necessary, you can reasonably infer background information, but be sure to indicate that it is an inference;\n"
            "3) Do not fabricate specific figures or internal company information."
        )
    )

    print("\n===== Today Tech News Brief =====\n")
    print(context_brief)
    print("\n===== You can start to ask (type q to quit) =====\n")

    history = [system, HumanMessage(content="This is the brief generated before:\n" + context_brief)]

    while True:
        user_input = input("You: ").strip()
        if user_input.lower() in ["q", "quit", "exit"]:
            print("Assistant: Ok, that's all for today. ")
            break

        history.append(HumanMessage(content=user_input))
        resp = llm.invoke(history)
        print("\nAssistant: ", resp.content, "\n")
        history.append(resp)

# ---------- 5. main route ----------
def main():
    print("==> in retrieving Google News RSS tech news ...")
    news_text = fetch_google_news_rss(max_items=10)

    print("==> in generating today tech news brief ...")
    brief = generate_daily_brief(news_text)

    chat_with_assistant(brief)

if __name__ == "__main__":
    main()
