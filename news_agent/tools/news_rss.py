import feedparser

def fetch_tech_news_rss(max_items: int = 10) -> str:
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
