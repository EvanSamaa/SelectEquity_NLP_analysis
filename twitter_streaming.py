#Import the necessary methods from tweepy library
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream

#Variables that contains the user credentials to access Twitter API
access_token = "1305275324066861057-qK6A0k6PjaBkP1lnilMAtIgqUFnDOh"
access_token_secret = "E2TljoX48voP3BQGFQjaJj9zGmenzPQIcoY3P3O733aOw"
consumer_key = "OzdMB3hZY45k3IYjHJzLKBEZp"
consumer_secret = "Mm3g6HijDYI6l2ZBA6cumCMksN4QUWor9CKnwhxHhFL02KGbid"


#This is a basic listener that just prints received tweets to stdout.
class StdOutListener(StreamListener):

    def on_data(self, data):
        print(data)
        return True

    def on_error(self, status):
        print(status)


if __name__ == '__main__':

    #This handles Twitter authetification and the connection to Twitter Streaming API
    l = StdOutListener()
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    stream = Stream(auth, l)

    #This line filter Twitter Streams to capture data by the keywords: 'python', 'javascript', 'ruby'
    stream.filter(track=['cov19','corona virus'])
