import os
import tweepy as tw
import pandas as pd
access_token = "1305275324066861057-qK6A0k6PjaBkP1lnilMAtIgqUFnDOh"
access_token_secret = "E2TljoX48voP3BQGFQjaJj9zGmenzPQIcoY3P3O733aOw"
consumer_key = "OzdMB3hZY45k3IYjHJzLKBEZp"
consumer_secret = "Mm3g6HijDYI6l2ZBA6cumCMksN4QUWor9CKnwhxHhFL02KGbid"
auth = tw.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tw.API(auth, wait_on_rate_limit=True)
search_words = "cov19"
date_since = "2000-02-01"
tweets = tw.Cursor(api.search,
              q=search_words,
              lang="en",
              since=date_since).items(20)
#for tweet in tweets:
 #   print(tweet.user.created_at)
users_locs = [[tweet.user.screen_name, tweet.user.location,tweet.text,tweet.user.created_at] for tweet in tweets]
tweet_text = pd.DataFrame(data=users_locs,
                    columns=['user', "location","text","time"])
print(tweet_text)