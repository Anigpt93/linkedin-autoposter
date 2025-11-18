# Minimal draft generator for GitHub Actions
# This uses Unsplash for an image and uses a simple template for a post.
# If you have an OPENAI API key, the section shown below can be swapped to call OpenAI to generate better copy.

import os
import json
import requests
from datetime import datetime

UNSPLASH_KEY = os.getenv("UNSPLASH_ACCESS_KEY", "")
OPENAI_KEY = os.getenv("OPENAI_API_KEY", "")

def pick_topic():
    # Simple hardcoded topics to start. You can extend this later.
    topics = [
        "payments reliability in fintech",
        "UPI product growth tactics",
        "how product managers prioritize payments features",
        "AI in fraud detection for card payments",
        "building low-latency payment systems"
    ]
    # pick by day for determinism
    index = datetime.utcnow().day % len(topics)
    return topics[index]

def generate_post_text(topic):
    # If you have OPENAI_KEY, replace this with a call to the LLM.
    hook = f"What if {topic} had a simple fix everyone ignored?"
    context = "I noticed recurring operational issues when scaling payment systems."
    insight = "Small architectural choices can reduce retries and increase success rates dramatically."
    example = "At my last project, we moved from sync to async webhook retries and dropped failures by 18%."
    takeaway = "Design for failure and observability from day one."
    hashtags = ["#payments", "#fintech", "#product"]
    return {
        "hook": hook,
        "context": context,
        "insight": insight,
        "example": example,
        "takeaway": takeaway,
        "hashtags": hashtags,
        "full_text": f"{hook}\n\n{context}\n\n{insight}\n\n{example}\n\n{takeaway}\n\n{' '.join(hashtags)}"
    }

def search_unsplash(query):
    if not UNSPLASH_KEY:
        return ""
    url = "https://api.unsplash.com/search/photos"
    params = {"query": query, "per_page": 1}
    headers = {"Accept-Version": "v1", "Authorization": f"Client-ID {UNSPLASH_KEY}"}
    r = requests.get(url, params=params, headers=headers, timeout=15)
    try:
        data = r.json()
        if data.get("results"):
            return data["results"][0]["urls"]["regular"]
    except Exception:
        pass
    return ""

def main():
    topic = pick_topic()
    post = generate_post_text(topic)
    image = search_unsplash(topic)
    output = {
        "topic": topic,
        "post": post,
        "image_url": image,
        "generated_at": datetime.utcnow().isoformat() + "Z"
    }
    print(json.dumps(output, indent=2))

if __name__ == "__main__":
    main()
