from APIs.CNN import *
from APIs.nytimes import *
from APIs.Guadian import *
from APIs.Googlenews.googlenews import *
from APIs.newsapi_scraping.newsapi_scrape1 import *
import os

def news_search(query_terms, savepath, ealiest_date="2000-01-01", latest_date=""):

    print("Begins Scraping")
    print("CNN scraping starts")
    CNN_scraping(query_terms, ealiest_date, latest_date)
    print("Guardien scraping starts")
    guardien_scrapping(query_terms, ealiest_date, latest_date)
    print("NY times scraping starts")
    scrape_NYtimes(query_terms, ealiest_date, latest_date)
    print(os.listdir("data"))
    list_of_df = []

    for item in os.listdir("data/"):
        full_path = "data/" + item
        print(full_path)
        df = pd.read_csv(full_path)
        print(df)
        list_of_df.append(df)

    rtv = pd.concat(list_of_df)
    rtv.to_csv(savepath, index=False)


if __name__ == "__main__":
    term = "corona virus OR covid"
    path = "./data/covid.json"
    ealiest_date = "2016-01-01"
    news_search(term, path, ealiest_date)
