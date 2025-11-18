# parse_issue_and_publish.py
import os
import re
import json
import requests
import argparse

LINKEDIN_TOKEN = os.getenv("LINKEDIN_ACCESS_TOKEN", "")
PERSON_URN = os.getenv("LINKEDIN_PERSON_URN", "")  # e.g. "urn:li:person:XXXX"

def extract_json_from_text(path):
    text = open(path, "r", encoding="utf-8").read()
    m = re.search(r"```json\\n(.*?\\n)```", text, re.S)
    if not m:
        # try simpler: find first { and last }
        start = text.find("{")
        end = text.rfind("}")
        if start == -1 or end == -1:
            raise SystemExit("Could not find JSON in issue body")
        return json.loads(text[start:end+1])
    return json.loads(m.group(1))

def upload_image_to_linkedin(image_url):
    # Simplified flow that skips registerUpload steps for brevity.
    # For a production setup follow LinkedIn registerUpload -> PUT bytes -> create UGC post.
    return None

def create_linkedin_post(text, image_url):
    if not LINKEDIN_TOKEN or not PERSON_URN:
        print("Missing LINKEDIN_ACCESS_TOKEN or LINKEDIN_PERSON_URN. Skipping actual publish.")
        print("Post text:\n", text)
        print("Image url:", image_url)
        return None
    # Here you should implement the full registerUpload -> upload -> ugcPosts flow.
    # For safety we will not implement it fully in this demo script.
    print("Would call LinkedIn API to publish now.")
    return True

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--issue-file", required=True)
    args = parser.parse_args()
    draft = extract_json_from_text(args.issue_file)
    post_text = draft.get("post", {}).get("full_text", "")
    image_url = draft.get("image_url", "")
    print("Draft post text:\n", post_text)
    print("Image:", image_url)
    create_linkedin_post(post_text, image_url)

if __name__ == "__main__":
    main()
