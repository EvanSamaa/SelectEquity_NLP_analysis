# Include functions to overlap covid data with metrics (e.g. sentiment score)

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
from utilities import *
from datetime import datetime


def convert2df(score, covid_day_1, covid_day_end, senti_day_1):
    diff = (covid_day_1 - senti_day_1).days
    duration = (covid_day_end - covid_day_1).days
    temp = score[diff:]
    temp = temp[:duration+1] * 100

    index = pd.date_range(covid_day_1, covid_day_end, freq='D').strftime('%m/%d/%y')
    columns = ['sentiment score']
    score_df = pd.DataFrame(temp, index=index, columns=columns)
    return score_df


# plot daily graph for top1 state in bar graph
def overlap_sentiscore(daily_states_data, state, senti_score, media_name):
    daily_onestate_data = daily_states_data[[state]]
    roll7_state_data = daily_onestate_data.rolling(7).mean()
    roll7_senti_score = senti_score.rolling(7).mean()

    fig, ax = plt.subplots(figsize=(20, 10))
    daily_onestate_data.plot(kind='bar', ax=ax)
    roll7_state_data.plot(color='red', ax=ax)
    roll7_senti_score.plot(color='green', ax=ax)
    # ax.legend(['7-day running average of cases', 'actual daily cases'])
    ax.legend(['7-day running average of cases', '7-day running avg of Sentiment Scores', 'actual daily cases'])
    plt.grid()
    ax.xaxis_date()
    my_xLocator = mticker.MultipleLocator(7)
    ax.xaxis.set_major_locator(my_xLocator)
    my_yLocator = mticker.MultipleLocator(500)
    ax.yaxis.set_major_locator(my_yLocator)
    fig.autofmt_xdate()
    plt.title("Daily Cases and 7-Day Running Average for %s State" % state)
    plt.xlabel('Dates')
    # plt.ylabel('Daily new cases')
    # plt.show()
    try:
        plt.savefig('./plots/overlap/%s/senti_score_%s.png' % (state, media_name))
    except FileNotFoundError:
        mkdir_p("./plots/overlap/%s" % state)
        plt.savefig('./plots/overlap/%s/senti_score_%s.png' % (state, media_name))


if __name__ == "__main__":
    # read covid data
    data = pd.read_csv("./data/time_series_covid19_confirmed_US.csv", delimiter=',', index_col=0)
    temp = data.groupby(['Province_State']).sum()
    all_states_data = (temp.iloc[:, 5:]).T  # accumulative cases group by state
    daily_states_data = all_states_data.diff()  # daily cases group by state

    # load sentiment scores
    senti_score = np.load("../models/bays_sentiment.npy")
    ft_score = senti_score[:, 0]
    cnn_score = senti_score[:, 1]
    nyt_score = senti_score[:, 2]
    guardian_score = senti_score[:, 3]

    senti_day_1 = datetime.strptime("10/10/19", "%m/%d/%y")
    covid_day_1 = datetime.strptime("1/22/20", "%m/%d/%y")
    covid_day_end = datetime.strptime("10/9/20", "%m/%d/%y")

    ft_score_df = convert2df(ft_score, covid_day_1, covid_day_end, senti_day_1)
    cnn_score_df = convert2df(cnn_score, covid_day_1, covid_day_end, senti_day_1)
    nyt_score_df = convert2df(nyt_score, covid_day_1, covid_day_end, senti_day_1)
    guardian_score_df = convert2df(guardian_score, covid_day_1, covid_day_end, senti_day_1)
    media_dict = {"nyt": nyt_score_df, "cnn": cnn_score_df, "ft": ft_score_df, "guardian": guardian_score_df}

    # select state of interest
    state_of_interest = 'New York'

    # select media of interest
    media = "nyt"

    # select plotting options
    overlap_sentiscore(daily_states_data, state_of_interest, media_dict[media], media)
