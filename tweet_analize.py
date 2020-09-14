import json
import pandas as pd
tweets_data_path = 'twitter_data.txt'
tweets_data = []
tweets_file = open(tweets_data_path, "r")
for line in tweets_file:
    try:
        tweet = json.loads(line)
        tweets_data.append(tweet)
    except:
        continue
print(tweets_data)
print(tweets_data[0]['text'])

