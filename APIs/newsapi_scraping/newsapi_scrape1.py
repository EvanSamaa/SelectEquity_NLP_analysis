import pprint
import requests
import pandas as pd
import json
import os


def scrape_everything(url, parameters):
    response = requests.get(url, params=parameters)

    # Convert the response to JSON format and pretty print it
    response_json = response.json()
    # pprint.pprint(response_json)

    # delete useless info
    for i in range(page_size):
        response_json["articles"][i].pop('content', None)
        response_json["articles"][i].pop('urlToImage', None)

    with open('./data.json', 'w') as outfile:
        json.dump(response_json["articles"], outfile)

    news_df = pd.read_json(r'./data.json', orient='columns')
    os.remove('data.json')

    file_name = '{}--{}--newsapi.csv'.format(text_query, language)
    news_df.to_csv(file_name, sep=',', index=False)


def scrape_headlines(url, parameters):
    # use this function to scrape important news only

    response = requests.get(url, params=parameters)

    # Convert the response to JSON format and pretty print it
    response_json = response.json()
    # pprint.pprint(response_json)

    # delete useless info
    for i in range(page_size):
        response_json["articles"][i].pop('content', None)
        response_json["articles"][i].pop('urlToImage', None)

    with open('./data.json', 'w') as outfile:
        json.dump(response_json["articles"], outfile)

    news_df = pd.read_json(r'./data.json', orient='columns')
    os.remove('data.json')

    file_name = '{}--{}--newsapi--headlines.csv'.format(text_query, language)
    news_df.to_csv(file_name, sep=',', index=False)


if __name__ == "__main__":
    # Global variables
    api_keys = []
    api_key = 'c054cfb5c898479c96aaf26ddbd26dee'    # your own API key
    api_keys.append(api_key)
    api_keys.append("2d8d34d10e834f018cb7684a989ce7bf")
    api_keys.append("2cb933f2aa724380bb555eb474d5b720")
    api_keys.append("f90bad89f8ae45479df51f61fee40487")

    url_everything = 'https://newsapi.org/v2/everything?'
    url_headlines = 'https://newsapi.org/v2/top-headlines?'

    # customize your search
    # documentation: https://newsapi.org/docs/
    text_query = 'coronavirus'                      # query phrase
    page_size = 20                                   # maximum is 100
    language = 'en'
    since_time = "2020-01-01"
    until_time = "2020-03-01"

    parameters = {
        'q': text_query,
        'pageSize': page_size,
        'language': language,
        # 'from': since_time,
        # 'to': until_time,
        'apiKey': api_key
    }

    scrape_everything(url_everything, parameters)
    scrape_headlines(url_headlines, parameters)