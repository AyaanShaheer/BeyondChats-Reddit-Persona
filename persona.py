#!/usr/bin/env python3
"""
BeyondChats AI/LLM Internship – Assignment
Scrapes a Redditor’s profile, builds a GPT-generated user persona with citations.
"""

import os, re, sys, json, datetime, argparse
from pathlib import Path

import praw
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
print("DEBUG reddit id =", os.getenv("REDDIT_CLIENT_ID"))
print("DEBUG secret =", os.getenv("REDDIT_CLIENT_SECRET"))
# -------------------------------------------------
# 1. Reddit API setup
# -------------------------------------------------
reddit = praw.Reddit(
    client_id=os.getenv("REDDIT_CLIENT_ID"),
    client_secret=os.getenv("REDDIT_CLIENT_SECRET"),
    user_agent=os.getenv("REDDIT_USER_AGENT"),
)

# -------------------------------------------------
# 2. Helper: extract username from URL
# -------------------------------------------------
def username_from_url(url: str) -> str:
    m = re.search(r"/user/([^/]+)/?$", url.strip())
    if not m:
        raise ValueError(f"Invalid reddit profile URL: {url}")
    return m.group(1)

# -------------------------------------------------
# 3. Scrape up to 1 000 posts + 1 000 comments
# -------------------------------------------------
def scrape_user(username: str, limit_each=1000):
    redditor = reddit.redditor(username)

    posts = []
    for p in redditor.submissions.new(limit=limit_each):
        posts.append(
            {
                "type": "post",
                "id": p.id,
                "title": p.title,
                "body": p.selftext[:4000],  # truncate for token budget
                "subreddit": str(p.subreddit),
                "url": f"https://redd.it/{p.id}",
                "created_utc": int(p.created_utc),
            }
        )

    comments = []
    for c in redditor.comments.new(limit=limit_each):
        comments.append(
            {
                "type": "comment",
                "id": c.id,
                "body": c.body[:4000],
                "subreddit": str(c.subreddit),
                "url": f"https://reddit.com{c.permalink}",
                "created_utc": int(c.created_utc),
            }
        )
    return posts + comments

# -------------------------------------------------
# 4. Build prompt and call GPT
# -------------------------------------------------
SYSTEM_PROMPT = """
You are a UX researcher.  
Given a list of Reddit posts and comments by a user, write a concise but insightful user persona (≈300–400 words).  
Structure it with these headings:  
- Demographics  
- Interests & Hobbies  
- Personality Traits  
- Goals & Motivations  
- Pain Points & Frustrations  

At the end of every sentence that draws evidence from a post/comment, add a citation in the form [source n], where n is the index of the item in the provided list (starting at 0).  
Do NOT invent information not supported by the sources.
"""

def build_persona(data):
    client = OpenAI()
    text_list = [f"{d['type']} in r/{d['subreddit']}: {d['title'] if d['type']=='post' else ''}{d['body']}" for d in data]
    numbered = [f"[{i}] {t}" for i, t in enumerate(text_list)]

    prompt = SYSTEM_PROMPT + "\n\n" + "\n".join(numbered)

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": "\n".join(numbered)},
        ],
        temperature=0.25,
        max_tokens=800,
    )
    return response.choices[0].message.content.strip()

# -------------------------------------------------
# 5. Save outputs
# -------------------------------------------------
def save_outputs(username, persona, raw):
    ts = datetime.datetime.utcnow().strftime("%Y%m%d_%H%M%S")
    base = Path("output")
    base.mkdir(exist_ok=True)

    txt_file = base / f"persona-{username}.txt"
    txt_file.write_text(persona, encoding="utf-8")

    json_file = base / f"raw-{username}-{ts}.json"
    json_file.write_text(json.dumps(raw, indent=2, ensure_ascii=False), encoding="utf-8")

    print(f"✅ Saved {txt_file} + {json_file}")

# -------------------------------------------------
# 6. CLI
# -------------------------------------------------
def main():
    parser = argparse.ArgumentParser(description="Reddit User Persona Builder")
    parser.add_argument("url")
    args = parser.parse_args()

    username = username_from_url(args.url)
    print(f"🔍 Scraping u/{username} …")
    raw = scrape_user(username)
    if not raw:
        print("⚠️  No posts/comments found.")
        return

    print(f"🧠 Generating persona from {len(raw)} sources …")
    persona = build_persona(raw)

    save_outputs(username, persona, raw)

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"❌ Error: {e}", file=sys.stderr)
        sys.exit(1)