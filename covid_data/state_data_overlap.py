# Include functions to overlap covid data with metrics (e.g. sentiment score)

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
from utilities import *
from datetime import datetime


def convert2df(score, covid_day_1, covid_day_end, senti_day_1, metric_name):
    diff = (covid_day_1 - senti_day_1).days
    duration = (covid_day_end - covid_day_1).days
    temp = score[diff:]
    if metric_name == "senti_score":
        temp = temp[:duration+1] * 100
    elif metric_name == "term frequency":
        temp = temp[:duration+1] * 30

    index = pd.date_range(covid_day_1, covid_day_end, freq='D').strftime('%m/%d/%y')
    columns = [metric_name]
    score_df = pd.DataFrame(temp, index=index, columns=columns)
    return score_df


def load_metric(path, covid_day_1, covid_day_end, metric_day_1, metric_name):
    metric_score = np.load(path)
    ft_score = metric_score[:, 0]
    cnn_score = metric_score[:, 1]
    nyt_score = metric_score[:, 2]
    guardian_score = metric_score[:, 3]

    ft_score_df = convert2df(ft_score, covid_day_1, covid_day_end, metric_day_1, metric_name)
    cnn_score_df = convert2df(cnn_score, covid_day_1, covid_day_end, metric_day_1, metric_name)
    nyt_score_df = convert2df(nyt_score, covid_day_1, covid_day_end, metric_day_1, metric_name)
    guardian_score_df = convert2df(guardian_score, covid_day_1, covid_day_end, metric_day_1, metric_name)
    media_dict = {"nyt": nyt_score_df, "cnn": cnn_score_df, "ft": ft_score_df, "guardian": guardian_score_df}
    return media_dict


# overlap sentiment score and state covid data
def overlap_sentiscore(daily_states_data, state, senti_score, media_name):
    daily_onestate_data = daily_states_data[[state]]
    roll7_state_data = daily_onestate_data.rolling(7).mean()
    roll7_senti_score = senti_score.rolling(7).mean()

    fig, ax = plt.subplots(figsize=(20, 10))
    daily_onestate_data.plot(kind='bar', ax=ax)
    roll7_state_data.plot(color='red', ax=ax)
    roll7_senti_score.plot(color='green', ax=ax)
    # ax.legend(['7-day running average of cases', 'actual daily cases'])
    ax.legend(['7-day running average of cases', '7-day running avg of %s Sentiment Scores'%media_name, 'actual daily cases'])
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
        plt.savefig('./plots/overlap/senti_score/%s/senti_score_%s.png' % (state, media_name))
    except FileNotFoundError:
        mkdir_p("./plots/overlap/senti_score/%s" % state)
        plt.savefig('./plots/overlap/senti_score/%s/senti_score_%s.png' % (state, media_name))


# overlap key term frequency with state covid data
def overlap_termfreq(daily_states_data, state, termfreq, media_name):
    daily_onestate_data = daily_states_data[[state]]
    roll7_state_data = daily_onestate_data.rolling(7).mean()
    roll7_termfreq = termfreq.rolling(7).mean()

    fig, ax = plt.subplots(figsize=(20, 10))
    daily_onestate_data.plot(kind='bar', ax=ax)
    roll7_state_data.plot(color='red', ax=ax)
    roll7_termfreq.plot(color='green', ax=ax)
    ax.legend(['7-day running average of cases', '7-day running avg of %s term frequency'%media_name, 'actual daily cases'])
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
        plt.savefig('./plots/overlap/term_freq/%s/termfreq_%s.png' % (state, media_name))
    except FileNotFoundError:
        mkdir_p("./plots/overlap/term_freq/%s" % state)
        plt.savefig('./plots/overlap/term_freq/%s/termfreq_%s.png' % (state, media_name))


if __name__ == "__main__":
    # read covid data
    data = pd.read_csv("./data/time_series_covid19_confirmed_US.csv", delimiter=',', index_col=0)
    temp = data.groupby(['Province_State']).sum()
    all_states_data = (temp.iloc[:, 5:]).T  # accumulative cases group by state
    daily_states_data = all_states_data.diff()  # daily cases group by state

    # .npy file path of metric data
    senti_path = "../models/bays_sentiment.npy"
    termfreq_path = "../models/frequency_count.npy"

    # select dates
    metric_day_1 = datetime.strptime("10/10/19", "%m/%d/%y")
    covid_day_1 = datetime.strptime("1/22/20", "%m/%d/%y")
    covid_day_end = datetime.strptime("10/9/20", "%m/%d/%y")

    # load metric data
    senti_media_dict = load_metric(senti_path, covid_day_1, covid_day_end, metric_day_1, metric_name="senti_score")
    termfreq_media_dict = load_metric(termfreq_path, covid_day_1, covid_day_end, metric_day_1, metric_name="term frequency")

    # select state of interest
    state_of_interest = 'New York'

    # Metric 1: Plot Sentiment Score
    # Option 1: plot sentiment scores from all media
    for key in senti_media_dict.keys():
        overlap_sentiscore(daily_states_data, state_of_interest, senti_media_dict[key], key)

    # Option 2: select media of interest and produce 1 plot only
    # media = "cnn"
    # overlap_sentiscore(daily_states_data, state_of_interest, senti_media_dict[media], media)


    # Metric 2: Plot Key Terms' Document Frequency
    # Option 1: plot sentiment scores from all media
    for key in termfreq_media_dict.keys():
        overlap_sentiscore(daily_states_data, state_of_interest, termfreq_media_dict[key], key)

    # Option 2: select media of interest and produce 1 plot only
    # media = "ft"
    # overlap_termfreq(daily_states_data, state_of_interest, termfreq_media_dict[media], media)