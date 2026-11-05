#!/usr/bin/python3
"""Recursively counts keywords in the hot post titles of a subreddit."""
import requests


def count_words(subreddit, word_list, after=None, counts=None):
    """Print a sorted count of keywords found in hot post titles."""
    if counts is None:
        counts = {}
    url = "https://www.reddit.com/r/{}/hot.json".format(subreddit)
    headers = {"User-Agent": "linux:alu-scripting:v1.0 (by /u/alu_student)"}
    params = {"limit": 100}
    if after:
        params["after"] = after
    try:
        res = requests.get(url, headers=headers, params=params,
                           allow_redirects=False, timeout=10)
        data = res.json().get("data", {}) if res.status_code == 200 else None
    except (requests.RequestException, ValueError):
        data = None

    if data is None:
        if after:
            _print_counts(counts, word_list)
        return

    keywords = set(w.lower() for w in word_list)
    for child in data.get("children", []):
        title = child.get("data", {}).get("title", "") or ""
        for word in title.lower().split():
            if word in keywords:
                counts[word] = counts.get(word, 0) + 1

    next_after = data.get("after")
    if next_after:
        return count_words(subreddit, word_list, next_after, counts)
    _print_counts(counts, word_list)


def _print_counts(counts, word_list):
    """Print counts (duplicates in word_list summed), sorted as required."""
    lowered = [w.lower() for w in word_list]
    totals = {w: n * lowered.count(w) for w, n in counts.items()}
    for word, total in sorted(totals.items(), key=lambda x: (-x[1], x[0])):
        if total > 0:
            print("{}: {}".format(word, total))
