---
title: uniqueWords
category: Leetcode Solutions
difficulty: Advanced
show_back_link: true
---

# uniqueWords

```bash
# Read from the file words.txt and output the word frequency list to stdout.
cat words.txt | tr -s ' ' '\n' | sort | uniq -c | sort -r | awk '{ print $2, $1 }'```
