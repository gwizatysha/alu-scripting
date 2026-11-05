#!/usr/bin/python3
"""Recursively queries the Reddit API for all hot post titles."""
import requests


def recurse(subreddit, hot_list=[], after=None):
    """Return a list of all hot post titles, or None if invalid subreddit."""
    url = "https://www.reddit.com/r/{}/hot.json".format(subreddit)
    headers = {"User-Agent": "linux:alu-scripting:v1.0 (by /u/alu_student)"}
    params = {"limit": 100}
    if after:
        params["after"] = after
    try:
        res = requests.get(url, headers=headers, params=params,
                           allow_redirects=False, timeout=10)
    except requests.RequestException:
        return hot_list if after else None
    if res.status_code != 200:
        return hot_list if after else None
    try:
        data = res.json().get("data", {})
    except ValueError:
        return hot_list if after else None

    titles = [c.get("data", {}).get("title") for c in data.get("children", [])]
    hot_list = hot_list + titles
    next_after = data.get("after")
    if next_after:
        return recurse(subreddit, hot_list, next_after)
    return hot_list or None
