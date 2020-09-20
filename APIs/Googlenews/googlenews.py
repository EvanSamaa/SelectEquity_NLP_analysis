from GoogleNews import GoogleNews
from newspaper import Article
from newspaper import Config
import pandas as pd
import nltk

def google_new_scrape():
    googlenews=GoogleNews(start='05/01/2020',end='05/03/2020')
    googlenews.search('Coronavirus')
    result=googlenews.result()


    df=pd.DataFrame(result)


    for i in range(2,4):
        googlenews.getpage(i)
        result=googlenews.result()
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
