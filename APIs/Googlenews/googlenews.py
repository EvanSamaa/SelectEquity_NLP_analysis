from GoogleNews import GoogleNews
from newspaper import Article
from newspaper import Config
import pandas as pd
from datetime import datetime as dt
import json
import os

def google_new_scrape(keyword=0, earliest_date="2000-01-01", end_date=""):
    ealiest_date = dt.strptime(earliest_date, "20%y-%m-%d")
    ealiest_date = ealiest_date.strftime("%m/%d/20%y")
    googlenews = None
    if end_date != "":
        end_date = dt.strptime(end_date, "20%y-%m-%d")
        end_date = end_date.strftime("%m/%d/20%y")
        googlenews = GoogleNews(start=earliest_date,end=end_date)
    else:
        googlenews = GoogleNews(start=earliest_date)
    googlenews.search('trump')
    for i in range(1,1000):
        googlenews.getpage(i)
        result=googlenews.result()
        print(len(result), result)
        df=pd.DataFrame(result)
    list=[]
    for ind in df.index:
        dict={}
        article = Article(df['link'][ind])
        article.download()
        article.parse()
        #article.nlp()
        dict['Date']=df['date'][ind]
        dict['Media']=df['media'][ind]
        dict['Title']=article.title
        dict['Article']=article.text
        dict['Summary']=article.summary
        list.append(dict)
    news_df=pd.DataFrame(list)
    print(news_df)
    file_name = 'googlenews.csv'
    news_df.to_csv(file_name)
if __name__ == "__main__":
    google_new_scrape()