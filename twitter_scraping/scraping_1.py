import GetOldTweets3 as got
import pandas as pd


def scrape_text_query(text_query, since_date, until_date, count):
    # Creation of query object
    tweetCriteria = got.manager.TweetCriteria().setQuerySearch(
        text_query).setSince(since_date).setUntil(until_date).setMaxTweets(count)
    # Creation of list that contains all tweets
    tweets = got.manager.TweetManager.getTweets(tweetCriteria)

    # Creating list of chosen tweet data
    # Add or remove tweet information you want in the below list comprehension
    tweets_list = [
        [tweet.id, tweet.author_id, tweet.username, tweet.to, tweet.text,
         tweet.retweets, tweet.favorites,
         tweet.replies, tweet.date, tweet.formatted_date, tweet.hashtags,
         tweet.mentions, tweet.urls, tweet.permalink, ] for tweet in tweets]

    # Creation of dataframe from tweets
    # Add or remove columns as you remove tweet information
    tweets_df = pd.DataFrame(tweets_list,
                             columns=['Tweet Id', 'Tweet User Id', 'Tweet User',
                                      'Reply to', 'Text', 'Retweets',
                                      'Favorites', 'Replies', 'Datetime',
                                      'Formatted date', 'Hashtags', 'Mentions',
                                      'Urls', 'Permalink'])

    # Removing timezone information to allow excel file download
    tweets_df['Datetime'] = tweets_df['Datetime'].apply(
        lambda x: x.replace(tzinfo=None))

    # Uncomment/comment below lines to decide between creating csv or excel file
    file_name = '{}--{}--{}--tweets.csv'.format(text_query, since_date,
                                              until_date)
    tweets_df.to_csv(file_name, sep=',', index=False)
#     tweets_df.to_excel('{}-tweets.xlsx'.format(text_query), index = False)


if __name__ == "__main__":
    # Input search query to scrape tweets and name csv file
    text_query = 'COVID-19'

    # Input search query to scrape tweets and name csv file
    since_date = '2020-01-01'
    until_date = '2020-03-01'

    # Max recent tweets pulls x amount of most recent tweets from that user
    max_tweets = 500

    # Function scrapes for tweets containing text_query, attempting to pull max_tweet amount and create csv/excel file containing data.
    scrape_text_query(text_query, since_date, until_date, max_tweets)