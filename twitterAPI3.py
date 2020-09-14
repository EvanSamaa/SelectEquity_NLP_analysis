import json
credentials = {}
credentials['CONSUMER_KEY'] = "OzdMB3hZY45k3IYjHJzLKBEZp"
credentials['CONSUMER_SECRET'] = "Mm3g6HijDYI6l2ZBA6cumCMksN4QUWor9CKnwhxHhFL02KGbid"
credentials['ACCESS_TOKEN'] = "1305275324066861057-qK6A0k6PjaBkP1lnilMAtIgqUFnDOh"
credentials['ACCESS_SECRET'] = "E2TljoX48voP3BQGFQjaJj9zGmenzPQIcoY3P3O733aOw"
with open("twitter_credentials.json", "w") as file:
    json.dump(credentials, file)

from twython import Twython
with open("twitter_credentials.json", "r") as file:
    creds = json.load(file)
python_tweets = Twython(creds['CONSUMER_KEY'], creds['CONSUMER_SECRET'])

# Create our query
query = {'q': '#corona',
        'result_type': 'popular',
        'count': 10,
        'lang': 'en',
        'until': '2020-09-07'
        }
import pandas as pd

# Search tweets
dict_ = {'user': [], 'date': [], 'text': [], 'favorite_count': []}
for status in python_tweets.search(**query)['statuses']:
    dict_['user'].append(status['user']['screen_name'])
    dict_['date'].append(status['created_at'])
    dict_['text'].append(status['text'])
    dict_['favorite_count'].append(status['favorite_count'])

# Structure data in a pandas DataFrame for easier manipulation
df = pd.DataFrame(dict_)
df.sort_values(by='favorite_count', inplace=True, ascending=False)
print(df.head(5))