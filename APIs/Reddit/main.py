import praw
import csv

reddit = praw.Reddit(client_id="m-Osz55rLKnyOQ",
                     client_secret="7QxLl4xJ6jv-XgoAY8yCPjDQBig",
                     user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.102 Safari/537.36",
                     username="garnetchar",
                     password="nKEeuDag.m#2Y8p")

subreddit = reddit.subreddit("COVID")
csvfile = open('reddit.csv', 'w', encoding='utf-8', newline='')
csvwriter = csv.writer(csvfile)
csvwriter.writerow(['title', 'score', 'id', 'url'])
# assume you have a Subreddit instance bound to variable `subreddit`
for submission in subreddit.new(limit=100):
    row = [submission.title, submission.score, submission.id, submission.url]
    csvwriter.writerow(row)

csvfile.close()