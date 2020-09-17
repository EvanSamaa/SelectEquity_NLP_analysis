import requests
import json
import csv

def GET():
    # Create your own account (https://developer.nytimes.com/get-started) and get your api key if you like. 
    # But you can also use my key, it should work in the same way.
    a = requests.get('https://api.nytimes.com/svc/archive/v1/2020/3.json?api-key=37xNSjQNTdhK18OgxAGjn9WN9QnO1Sn7')

    with open('data.json', 'w') as f:
        json.dump(a.json(), f)


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
    # GET()
    PARSE()
