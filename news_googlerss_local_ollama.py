"""
using local Ollama model to retrieve tech news, it is free
"""

import feedparser
#from langchain_community.llms import Ollama
from langchain_ollama import OllamaLLM
from langchain_core.messages import SystemMessage, HumanMessage


# ---------- 1. use Google News RSS to pull tech news (free) ----------
def fetch_google_news_rss(max_items: int = 10):
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


# ---------- 2. construct local LLM (Ollama) ----------
def get_local_llm():
    """return Ollama(
        model="llama3",   # can replace with qwen2.5 / mistral / phi3
        temperature=0.3
    )"""
    return OllamaLLM(
        model="llama3",   # can replace with qwen2.5 / mistral / phi3
        temperature=0.3
    )


# ---------- 3. generate English tech news brief ----------
def generate_daily_brief(news_text: str) -> str:
    llm = get_local_llm()

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
            "1) Produce a structured English daily tech briefing.\n"
            "2) Prioritize items by importance.\n"
            "3) For each item, provide 1–2 sentences explaining the event and its impact.\n"
            "4) End with 3 key trends or developments worth monitoring.\n\n"
            f"News list:\n{news_text}"
        )
    )

    resp = llm.invoke([system, user])
    return resp


# ---------- 4. support further conversation and ask ----------
def chat_with_assistant(context_brief: str):
    llm = get_local_llm()

    system = SystemMessage(
        content=(
            "You are a personal technology news assistant. "
            "The user has already read your daily tech briefing. "
            "Answer follow‑up questions with clarity, depth, and accuracy."
        )
    )

    print("\n===== Daily Tech Briefing =====\n")
    print(context_brief)
    print("\n===== Ask follow‑up questions (q to quit) =====\n")

    history = [system, HumanMessage(content="Here is the briefing:\n" + context_brief)]

    while True:
        user_input = input("You: ").strip()
        if user_input.lower() in ["q", "quit", "exit"]:
            print("Assistant: Alright, see you next time.")
            break

        history.append(HumanMessage(content=user_input))
        resp = llm.invoke(history)
        print("\nAssistant:", resp, "\n")
        history.append(resp)


# ---------- 5. main route ----------

def main():
    print("==> Fetching Google News RSS tech headlines...")
    news_text = fetch_google_news_rss(max_items=10)

    print("==> Generating daily tech briefing (local model)...")
    brief = generate_daily_brief(news_text)

    chat_with_assistant(brief)


if __name__ == "__main__":
    main()
