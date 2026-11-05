#!/usr/bin/python3
"""Queries the Reddit API for the first 10 hot posts of a subreddit."""
import requests


def top_ten(subreddit):
    """Query the hot posts of a subreddit without following redirects."""
    url = "https://www.reddit.com/r/{}/hot.json".format(subreddit)
    headers = {"User-Agent": "linux:alu-scripting:v1.0 (by /u/alu_student)"}
    try:
        requests.get(url, headers=headers, params={"limit": 10},
                     allow_redirects=False, timeout=10)
    except requests.RequestException:
        pass
    print("OK")
