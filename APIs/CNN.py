import requests
from datetime import datetime as dt
import json
import pandas as pd
import os
def CNN_scraping(query, earliest_date="2000-01-01", latest_date=""):
    queries = query.split(" OR ")
    for q in queries:
        query_CNN_by_keyword_alt(q, earliest_date=earliest_date, latest_date=latest_date)
    with open('data/CNN_temp.txt') as infile:
        news_df = pd.read_json(infile, orient='index')
    file_name = 'data/CNNNews.csv'
    os.remove('data/CNN_temp.txt')
    news_df.to_csv(file_name, index=False)
def query_CNN_by_keyword_alt(keyword, earliest_date="2000-01-01", latest_date="", date_param="firstPublishDate"):
    # earliest_date and latest_date should in the form for
    url = "https://search.api.cnn.io/content/"
    ealiest_date = dt.strptime(earliest_date, "20%y-%m-%d")
    if latest_date != "":
        latest_date = dt.strptime(earliest_date, "20%y-%m-%d")
    rtv = {}
    try:
        with open('data/CNN_temp.txt') as infile:
            rtv = json.load(infile)
    except:
        rtv = {}
    if True:
        starting_article_number = 0
        increment = 100
        oldest_article_date = ""
        total = 0
        while True:
            params = {"q": keyword, "sort": "newest", "size": 100, "from": starting_article_number}
            r = requests.get(url, params).json()
            # error protection
            if len(r['result']) == 0:
                break
            # storing result
            for a in r['result']:
                # try:
                #     print(a["ticker"])
                # except:
                #     pass
                # print(a.keys())
                date_of_interest = a[date_param].split("T")[0]
                date_of_interest = dt.strptime(date_of_interest, "20%y-%m-%d")
                if date_of_interest >= ealiest_date:
                    sub_json = {}
                    sub_json["title"] = a["headline"]
                    sub_json["date"] = a["firstPublishDate"].split("T")[0]
                    sub_json["raw_body"] = a["body"]
                    sub_json["url"] = a["url"]
                    sub_json["publisher"] = "CNN"
                    sub_json["keyword"] = keyword
                    rtv[a['_id']] = sub_json
            # calculating stopping condition
            oldest_article_date_this_batch = r['result'][0]['firstPublishDate']
            if oldest_article_date_this_batch != oldest_article_date:
                oldest_article_date = oldest_article_date_this_batch
            else:
                break
            starting_article_number += increment
    # with open(save_path, 'w') as fp:
    #     json.dump(rtv, fp)
    with open('data/CNN_temp.txt', 'w') as outfile:
        json.dump(rtv, outfile)
    print("A total of {} articles are obtained from CNN.".format(len(rtv)))

if __name__ == "__main__":
    # call("https://search.api.cnn.io/content?q=coronavirus&sort=newest&category=business,us,politics,world,opinion,health&size=100&from={}", 20000)
    # call("https://search.api.cnn.io/content?q=coronavirus&sort=newest&size=100&from={}")
    CNN_scraping("Covid19 OR coronavirus OR pandemic", earliest_date="2000-01-01", latest_date="")
    key = "ta229fqya3ffskn2vv5exm2k"


