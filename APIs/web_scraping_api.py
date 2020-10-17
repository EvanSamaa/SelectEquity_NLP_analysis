from APIs.CNN import *
from APIs.nytimes import *
from APIs.Guadian import *
from APIs.Googlenews.googlenews import *
from APIs.newsapi_scraping.newsapi_scrape1 import *
from APIs.FinancialTimes import *


def news_search(query_terms, savepath, ealiest_date="2000-01-01", latest_date=""):
    list_of_df = []
    print("Begins Scraping")
    print("NY times scraping starts")
    scrape_NYtimes(query_terms, ealiest_date, latest_date)
    print("Financial times scraping starts")
    scrape_financial_times(query_terms, ealiest_date, latest_date)
    print("CNN scraping starts")
    CNN_scraping(query_terms, ealiest_date, latest_date)
    print("Guardien scraping starts")
    guardien_scrapping(query_terms, ealiest_date, latest_date)
    print(os.listdir("data"))


    for item in os.listdir("data/"):
        full_path = "data/" + item
        df = pd.read_csv(full_path)
        list_of_df.append(df)

    rtv = pd.concat(list_of_df)
    rtv.to_csv(savepath, index=False)


if __name__ == "__main__":
    term = "covid OR SARS OR coronavirus OR cov19 OR pandemic OR novel virus OR covid-19 OR Wuhan Virus"
    path = "./data/covid_new_keyword.csv"
    ealiest_date = "2019-10-10"
    news_search(term, path, ealiest_date)
