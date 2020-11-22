import requests
import json
import csv
import time
from datetime import datetime
import pandas as pd
import os
def scrape_NYtimes(queries, earliest_date="2000-01-01", latest_date="", file_name='data/NYtimes.csv'):
    queries = queries.split(" OR ")
    tot_articles = 0
    for q in queries:
        tot_articles = tot_articles + search_ny_times(q, earliest_date=earliest_date, latest_date=latest_date, file_name=file_name)
    os.remove("data/NY_temp.txt")
    return tot_articles
def search_ny_times(query, earliest_date="2000-01-01", latest_date="", file_name='data/NYtimes.csv'):
    # Create your own account (https://developer.nytimes.com/get-started) and get your api key if you like. 
    # But you can also use my key, it should work in the same way.
    earliest_date = "".join(earliest_date.split("-"))
    if latest_date == "":
        latest_date = datetime.today().strftime('%Y-%m-%d')
    latest_date = "".join(latest_date.split("-"))
    params = {"q":query, "api-key":"37xNSjQNTdhK18OgxAGjn9WN9QnO1Sn7", "sort":"oldest", "page":0, "begin_date":earliest_date, "end_date":latest_date}
    if query == "_all":
        params = {"api-key":"37xNSjQNTdhK18OgxAGjn9WN9QnO1Sn7", "sort":"oldest", "page":0, "begin_date":earliest_date, "end_date":latest_date}
    if latest_date != "":
        params["end_date"] = latest_date
    url = "https://api.nytimes.com/svc/search/v2/articlesearch.json"
    total_count = 0
    rtv_dict = {}
    try:
        with open('data/NY_temp.txt') as infile:
            rtv_dict = json.load(infile)
    except:
        rtv_dict = {}
    for i in range(0, 200000):
        time.sleep(6)
        try:
            params["page"] = i
        except:
            break
        a = requests.get(url, params = params).json()
        try:
            if a["status"] == "OK":
                data = a["response"]["docs"]
                if len(data) > 0:
                    for article in data:
                        # for item in article.keys():
                        #     print(item, article[item])
                        print(article["pub_date"].split("T")[0])
                        sub_json = {}
                        sub_json["title"] = article["headline"]["main"]
                        sub_json["date"] = article["pub_date"].split("T")[0]
                        sub_json["raw_body"] = article["abstract"] + "\n" + article["lead_paragraph"]
                        sub_json["url"] = article["web_url"]
                        sub_json["publisher"] = "NYtimes"
                        rtv_dict[article["_id"]] = sub_json
                else:
                    break
            else:
                print("have trouble connecting with NYT server")
                break
        except:
            break
    # with open('data.json', 'w') as f:
    #     json.dump(a.json(), f)
    total_count = len(rtv_dict)
    print("A total of {} articles are obtained from NY times.".format(total_count))
    with open('data/NY_temp.txt', 'w') as outfile:
        json.dump(rtv_dict, outfile)
    with open('data/NY_temp.txt') as infile:
        news_df = pd.read_json(infile, orient='index')
    news_df.to_csv(file_name, index=False)
    return total_count
def PARSE():
    # first, inspect with the Tree View Mode in https://countwordsfree.com/jsonviewer . Then pick the elements we want.
    with open('data.json') as f:
        bulk = json.load(f)
    meta_counts = bulk['response']['meta']['hits']
    csvfile = open('march_%d.csv'%meta_counts, 'w', newline='', encoding="utf-8")
    csvwriter = csv.writer(csvfile)
    # most_need_titles = ['abstract', 'lead_paragraph', 'source', 'headline','keywords','keyword_type','pub_date', 'document_type',
    # 'news_desk', 'section_name', 'subsection_name', 'type_of_material', '_id']
    csvwriter.writerow(['abstract', 'web_url', 'lead_paragraph', 'source', 'headline','keywords', 'keyword_type',
                        'pub_date', 'document_type', 'news_desk', 'section_name', 'subsection_name', 'type_of_material', '_id'])
    for article in bulk['response']['docs']:
        row = []
        for i in ['abstract', 'web_url', 'lead_paragraph', 'source', 'headline','keywords', 'pub_date',
                  'document_type', 'news_desk', 'section_name', 'subsection_name', 'type_of_material', '_id']:
            if i == 'headline':
                try:
                    a = article[i]['main']
                except:
                    a = ''
            elif i == 'keywords':
                try:
                    keywords = article[i]
                    a = []
                    b = []
                    for node in article[i]:
                        b.append(node['value'])
                        a.append(node['name'])
                    row.append(str(b))
                except:
                    a = ''
            else:
                try:
                    a = article[i]
                except:
                    a = ''

            row.append(str(a))
        csvwriter.writerow(row)

if __name__ == '__main__':
    scrape_NYtimes("_all", "2020-02-01", "2020-05-01", "data/NYtimes_feb2May.csv")
    key = "37xNSjQNTdhK18OgxAGjn9WN9QnO1Sn7"
