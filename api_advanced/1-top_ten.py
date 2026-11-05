#!/usr/bin/python3
"""Prints the titles of the first 10 hot posts of a subreddit."""
import requests


def top_ten(subreddit):
    """Print the first 10 hot post titles, or None if invalid subreddit."""
    url = "https://www.reddit.com/r/{}/hot.json".format(subreddit)
    headers = {"User-Agent": "linux:alu-scripting:v1.0 (by /u/alu_student)"}
    try:
        res = requests.get(url, headers=headers, params={"limit": 10},
                           allow_redirects=False, timeout=10)
        if res.status_code != 200:
            print(None)
            return
        posts = res.json().get("data", {}).get("children", [])
    except (requests.RequestException, ValueError):
        print(None)
        return
    for post in posts[:10]:
        print(post.get("data", {}).get("title"))
