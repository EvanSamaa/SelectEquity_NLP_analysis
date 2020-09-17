import requests
import os
from pprint import pprint
import requests
import pandas as pd
import json
import os
# https://open-platform.theguardian.com/documentation/section
#'''
query = "corona virus","covid19","COV19"
query_fields = "body"
section = "news"  # https://open-platform.theguardian.com/documentation/section
#tag = ""  # https://open-platform.theguardian.com/documentation/tag
from_date = "2020-02-01"
to_date="2020-03-30"
#page=21
page_size=100
query_url = f"https://content.guardianapis.com/search?" \
            f"api-key=eb88ddac-2447-4a97-8899-dbaca0e7b986" \
            f"&q={query}" \
            f"&query-fields={query_fields}" \
            f"&section={section}" \
            f"&from-date={from_date}" \
            f"&to-date={to_date}" \
            f"&page-size={page_size}"\
            f"&order-by=newest"\
            f"&show-fields=headline,body,publication"
            #f"&page={page}"\
r = requests.get(query_url)
#pprint(r.json())
all_results = []
data = r.json()
all_results.extend(data['response']['results'])
#print(all_results)
with open('GuardianNews.json', 'w') as f:
    json.dump(all_results, f,indent=2)
news_df = pd.read_json(r'./GuardianNews.json', orient='columns')
#os.remove('data.json')

file_name = 'GuardianNews.csv'
news_df.to_csv(file_name, index=False)

#with open('data.json', 'w') as f:
 #   json.dump(r.json(), f)
