import requests
from datetime import datetime as dt
import json
import pandas as pd
import os
import math as math
import time

def scrape_financial_times(queries, earliest_date="2000-01-01", latest_date="", file_name = 'data/FinancialTimes.csv'):
    queries = queries.split(" OR ")
    tot_articles = 0
    for q in queries:
        tot_articles = tot_articles + financial_times_scrapping(q, earliest_date=earliest_date, latest_date=latest_date, file_name=file_name)
    os.remove("data/FT_temp.txt")
    return tot_articles

def financial_times_scrapping(keyword, earliest_date="2000-01-01", latest_date="", file_name = 'data/FinancialTimes.csv'):
    url = "https://api.ft.com/content/search/v1?apiKey=59cbaf20e3e06d3565778e7b8e6675b8ae9c40cf8923fccc493add4e"
    key = "59cbaf20e3e06d3565778e7b8e6675b8ae9c40cf8923fccc493add4e"
    starting_article_number = 0
    ealiest_date_time = dt.strptime(earliest_date, "20%y-%m-%d")
    if latest_date != "":
        latest_date_time = dt.strptime(latest_date, "20%y-%m-%d")
    ealiest_date = "T".join(str(ealiest_date_time).split(" "))+"Z"
    latest_date = "T".join(str(latest_date_time).split(" ")) + "Z"
    params = {
        "queryString": keyword,
        "queryContext": {
            "curations": ["ARTICLES", "BLOGS", "PAGES"]},
        "resultContext": {
            "maxResults": 100,
            "offset": 0,
            "contextual": True,
            "highlight": False,
            "aspects": ["title", "lifecycle", "location", "summary", "editorial"]}
    }
    if keyword == "_all":
        params = {
        "queryString": "initialPublishDateTime:<{}".format(latest_date) + " AND initialPublishDateTime:>{}".format(ealiest_date),
        "resultContext": {
            "maxResults": 100,
            "offset": 0,
            "contextual": True,
            "highlight": False,
            "aspects": ["title", "lifecycle", "location", "summary", "editorial"]}
    }

    rtv = {}
    try:
        with open('data/FT_temp.txt') as infile:
            rtv = json.load(infile)
    except:
        rtv = {}
    r = requests.post(url, json=params).json()
    try:
        response = r["results"]
    except:
        return 0
    total_articles_count = response[0]["indexCount"]
    # print(total_articles_count)
    try:
        test = response[0]["results"]
    except:
        return 0
    for article in range(0, len(response[0]["results"])):
        a = response[0]["results"][article]
        sub_json = {}
        print(a["lifecycle"]["initialPublishDateTime"].split("T")[0])
        try:
            sub_json["title"] = a["title"]["title"]
        except:
            sub_json["title"] = ""
        sub_json["date"] = a["lifecycle"]["initialPublishDateTime"].split("T")[0]
        try:
            sub_json["raw_body"] = a["summary"]["excerpt"]
        except:
            sub_json["raw_body"] = ""
        sub_json["url"] = a["location"]["uri"]
        sub_json["publisher"] = "FinancialTimes"
        date_of_interest = dt.strptime(sub_json["date"], "20%y-%m-%d")
        if date_of_interest >= ealiest_date_time:
            if latest_date == "":
                rtv[a['id']] = sub_json
            else:
                if date_of_interest <= latest_date_time:
                    rtv[a['id']] = sub_json

    for i in range(1, min(int(total_articles_count/100) + 1, 3000)):
        params["resultContext"]["offset"] = i * 100
        time.sleep(0.5)
        r = requests.post(url, json=params).json()
        try:
            response = r["results"]
        except:
            print("result key not found")
            break
        for article in range(0, len(response[0]["results"])):
            a = response[0]["results"][article]
            print(a["lifecycle"]["initialPublishDateTime"].split("T")[0])
            sub_json = {}
            try:
                sub_json["title"] = a["title"]["title"]
            except:
                sub_json["title"] = ""
            sub_json["date"] = a["lifecycle"]["initialPublishDateTime"].split("T")[0]
            try:
                sub_json["raw_body"] = a["summary"]["excerpt"]
            except:
                sub_json["raw_body"] = ""
            sub_json["url"] = a["location"]["uri"]
            sub_json["publisher"] = "FinancialTimes"
            date_of_interest = dt.strptime(sub_json["date"], "20%y-%m-%d")
            if date_of_interest >= ealiest_date_time:
                if latest_date == "":
                    rtv[a['id']] = sub_json
                else:
                    if date_of_interest <= latest_date_time:
                        rtv[a['id']] = sub_json
            # print(a)
    print("A total of {} articles are obtained from Financial Times.".format(len(rtv)))
    with open('data/FT_temp.txt', 'w') as outfile:
        json.dump(rtv, outfile)
    with open('data/FT_temp.txt') as infile:
        news_df = pd.read_json(infile, orient='index')
    news_df.to_csv(file_name, index=False)
    return total_articles_count
if __name__ == "__main__":
    scrape_financial_times("_all", "2019-12-01", "2020-01-01", file_name="data/FT_all_between_12and1")
    scrape_financial_times("_all", "2019-11-01", "2019-12-01", file_name="data/FT_all_between_11and12")
    scrape_financial_times("_all", "2019-10-01", "2019-11-01", file_name="data/FT_all_between_10and11")