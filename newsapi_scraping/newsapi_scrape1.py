import pprint
import requests
import pandas as pd


def scrape_newsapi(url, parameters):
    response = requests.get(url, params=parameters)

    # Convert the response to JSON format and pretty print it
    response_json = response.json()
    pprint.pprint(response_json)

    # print just the titles
    # for i in response_json['articles']:
    #     print(i['title'])

    import json
    import os
    with open('./data.json', 'w') as outfile:
        json.dump(response_json["articles"], outfile)

    news_df = pd.read_json(r'./data.json', orient='columns')
    os.remove('data.json')

    file_name = '{}--{}--newsapi.csv'.format(text_query, language)
    news_df.to_csv(file_name, sep=',', index=False)


if __name__ == "__main__":
    # Global variables
    api_key = 'c054cfb5c898479c96aaf26ddbd26dee'    # your own API key
    url = 'https://newsapi.org/v2/everything?'      # Define the endpoint

    # customize your search
    # documentation: https://newsapi.org/docs/
    text_query = 'coronavirus'                      # query phrase
    page_size = 20                                  # maximum is 100
    language = 'en'

    parameters = {
        'q': text_query,
        'pageSize': page_size,
        'language': language,
        'apiKey': api_key
    }

    scrape_newsapi(url, parameters)