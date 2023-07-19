#!/usr/bin/python3
""" 3-count.py """

import json
import operator
import requests



def count_words(subreddit, word_list, after=None, word_count=None):
    """ Prints a sorted count of given keywords """
    if word_count is None:
        word_count = {}
    
    if len(word_list) == 0:
        sorted_list = sorted(word_count.items(), key=lambda x: (-x[1], x[0]))
        for key, count in sorted_list:
            print(f"{key}: {count}")
        return

    url = f"https://www.reddit.com/r/{subreddit}/hot.json"
    headers = {"User-Agent": "Mozilla/5.0"}
    params = {"after": after} if after else None

    result = requests.get(url, headers=headers, params=params, allow_redirects=False)

    if result.status_code != 200:
        return

    body = json.loads(result.text)

    for post in body["data"]["children"]:
        title_words = post["data"]["title"].lower().split()
        for word in word_list:
            if word.lower() in title_words:
                if word in word_count:
                    word_count[word] += 1
                else:
                    word_count[word] = 1

    after = body["data"]["after"]
    return count_words(subreddit, word_list, after, word_count)

# Example usage:
count_words("programming", ["react", "python", "java", "javascript", "scala", "no_results_for_this_one"])
