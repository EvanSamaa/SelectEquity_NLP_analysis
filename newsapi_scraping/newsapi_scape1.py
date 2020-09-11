import pprint
import requests

# Global variables
api_key = 'c054cfb5c898479c96aaf26ddbd26dee'
url = 'https://newsapi.org/v2/everything?'  # Define the endpoint

# Specify the query and number of returns
parameters = {
    'q': 'big data',  # query phrase
    'pageSize': 20,  # maximum is 100
    'apiKey': api_key  # your own API key
}
# documentation: https://newsapi.org/docs/


def make_request(url, parameters):
    response = requests.get(url, params=parameters)

    # Convert the response to JSON format and pretty print it
    response_json = response.json()
    pprint.pprint(response_json)

    # print just the titles
    # for i in response_json['articles']:
    #     print(i['title'])


if __name__ == "__main__":
    make_request(url, parameters)