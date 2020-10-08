
import requests
import pandas as pd
import json
import time
from datetime import datetime
import os
#12calls/second
#5k calls/day
#free for non-commercial usage
# https://open-platform.theguardian.com/documentation/section
#'''
# https://open-platform.theguardian.com/documentation/search

def guardien_scrapping(query, earliest_date="2000-01-01", latest_date=""):
    # query = "corona virus, covid"
    query_fields = "headline"
    section = "news"  # https://open-platform.theguardian.com/documentation/section
    #tag = ""  # https://open-platform.theguardian.com/documentation/tag
    if latest_date == "":
        latest_date = datetime.today().strftime('%Y-%m-%d')
    page_size = 50
    output_json = {}
    total_count = 0
    for page in range(1, 1000):
        # to ensure we do not go over the limitation of 12 request per sec
        time.sleep(0.2)
        query_url = f"https://content.guardianapis.com/search?" \
                    f"api-key=eb88ddac-2447-4a97-8899-dbaca0e7b986" \
                    f"&q={query}" \
                    f"&query-fields={query_fields}" \
                    f"&section={section}" \
                    f"&from-date={earliest_date}" \
                    f"&to-date={latest_date}" \
                    f"&page-size={page_size}" \
                    f"&order-by=newest" \
                    f"&show-fields=headline,body,publication" \
                    f"&page={page}"
        r = requests.get(query_url)
        all_results = []
        data = r.json()
        if data["response"]['status'] != "error":
            all_results.extend(data['response']['results'])
            total_count = total_count + len(all_results)
            for article in all_results:
                sub_json ={}
                sub_json["title"] = article["webTitle"]
                sub_json["date"] = article["webPublicationDate"].split("T")[0]
                sub_json["raw_body"] = article["fields"]["body"]
                sub_json["url"] = article["webUrl"]
                sub_json["publisher"] = "The Guardian"
                output_json[article["id"]] = sub_json
        elif data["response"]['status'] == "error":
            error_message = data["response"]["message"]
            if error_message != "requested page is beyond the number of available pages":
                print(data["response"]["message"])
            break
        if data["response"]['total'] == 0:
            print("There is no result")
            break
    for page in range(1, 1000):
        # to ensure we do not go over the limitation of 12 request per sec
        time.sleep(0.2)
        query_url = f"https://content.guardianapis.com/search?" \
                    f"api-key=eb88ddac-2447-4a97-8899-dbaca0e7b986" \
                    f"&q={query}" \
                    f"&query-fields=body" \
                    f"&section={section}" \
                    f"&from-date={earliest_date}" \
                    f"&to-date={latest_date}" \
                    f"&page-size={page_size}" \
                    f"&order-by=newest" \
                    f"&show-fields=headline,body,publication" \
                    f"&page={page}"
        r = requests.get(query_url)
        all_results = []
        data = r.json()
        if data["response"]['status'] != "error":
            all_results.extend(data['response']['results'])
            total_count = total_count + len(all_results)
            for article in all_results:
                print(article.keys())
                A[2]
                sub_json ={}
                sub_json["title"] = article["webTitle"]
                sub_json["date"] = article["webPublicationDate"].split("T")[0]
                sub_json["raw_body"] = article["fields"]["body"]
                sub_json["url"] = article["webUrl"]
                sub_json["publisher"] = "The Guardian"
                output_json[article["id"]] = sub_json
        elif data["response"]['status'] == "error":
            error_message = data["response"]["message"]
            if error_message != "requested page is beyond the number of available pages":
                print(data["response"]["message"])
            break
        if data["response"]['total'] == 0:
            print("There is no result")
            break
    print("A total of {} articles are obtained from Guardian.".format(total_count))
    with open('data/temp.txt', 'w') as outfile:
        json.dump(output_json, outfile)
    with open('data/temp.txt') as infile:
        news_df = pd.read_json(infile, orient='index')
    file_name = 'data/GuardianNews.csv'
    os.remove("data/temp.txt")
    news_df.to_csv(file_name, index=False)
    return total_count
if __name__ == "__main__":
    guardien_scrapping(query ="Covid OR corona virus OR pandenmic")