import requests
from datetime import datetime as dt
import json

def query_CNN_by_keyword(keyword, earliest_date="2000-01-01", latest_date="", date_param="firstPublishDate", save_path=""):
    # earliest_date and latest_date should in the form for
    url = "https://search.api.cnn.io/content?q={}&sort=newest&size=100&from="
    url.format(keyword) + "{}"
    ealiest_date = dt.strptime(earliest_date, "20%y-%m-%d")
    if latest_date != "":
        latest_date = dt.strptime(earliest_date, "20%y-%m-%d")

    rtv = {}

    with requests.Session() as req:
        starting_article_number = 0
        increment = 100
        oldest_article_date = ""
        total = 0
        while True:
            r = req.get(url.format(starting_article_number)).json()
            total = total + len(r['result'])
            # error protection
            if len(r['result']) == 0:
                break
            # storing result
            for a in r['result']:
                date_of_interest = a[date_param].split("T")[0]
                date_of_interest = dt.strptime(date_of_interest, "20%y-%m-%d")
                if date_of_interest >= ealiest_date:
                    rtv[a["_id"]] = a
            # calculating stopping condition
            oldest_article_date_this_batch = r['result'][0]['firstPublishDate']
            if oldest_article_date_this_batch != oldest_article_date:
                oldest_article_date = oldest_article_date_this_batch
            else:
                break
            starting_article_number += increment
        if save_path == "":
            return rtv
        else:
            with open(save_path, 'w') as fp:
                json.dump(rtv, fp)
            return rtv



if __name__ == "__main__":
    # call("https://search.api.cnn.io/content?q=coronavirus&sort=newest&category=business,us,politics,world,opinion,health&size=100&from={}", 20000)
    # call("https://search.api.cnn.io/content?q=coronavirus&sort=newest&size=100&from={}")
    query_CNN_by_keyword("China", earliest_date="2020-08-30", save_path="./CNN_China_info.json")
    key = "ta229fqya3ffskn2vv5exm2k"


