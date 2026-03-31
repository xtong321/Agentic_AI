import os
import json
from datetime import datetime
from subprocess import check_output
from typing import Collection
from openclaw import Claw

OUTPUT_DIR = "output"
EMAIL_CONFIG = "email_config.json"


def run_claw_task():
    """Run the OpenClaw task and return the output text."""
    #result = check_output(["claw", "run", "daily_tech_briefing"], text=True)
    claw = Claw("claw.json")
    result = claw.run("daily_tech_briefing")
    print(result)
    return result


def save_markdown(text: str):
    """Save briefing to markdown file."""
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    today = datetime.now().strftime("%Y-%m-%d")
    path = os.path.join(OUTPUT_DIR, f"{today}-tech-brief.md")

    with open(path, "w", encoding="utf-8") as f:
        f.write(text)

    return path


def send_email_if_configured(path: str):
    """Send email if email_config.json exists."""
    if not os.path.exists(EMAIL_CONFIG):
        return

    import smtplib
    from email.mime.text import MIMEText

    cfg = json.load(open(EMAIL_CONFIG, "r", encoding="utf-8"))

    with open(path, "r", encoding="utf-8") as f:
        content = f.read()

    msg = MIMEText(content, "plain", "utf-8")
    msg["Subject"] = "Daily Tech Brief"
    msg["From"] = cfg["from"]
    msg["To"] = cfg["to"]

    with smtplib.SMTP(cfg["smtp_server"], cfg["smtp_port"]) as server:
        server.starttls()
        server.login(cfg["from"], cfg["password"])
        server.send_message(msg)


def main():
    print("Running OpenClaw tech news agent...")
    output = run_claw_task()

    print("Saving markdown...")
    path = save_markdown(output)

    print("Sending email (if configured)...")
    send_email_if_configured(path)

    print("Done.")


if __name__ == "__main__":
    main()
