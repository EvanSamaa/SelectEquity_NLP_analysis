# Include functions to overlap covid data with metrics (e.g. sentiment score)

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
from utilities import *
from datetime import datetime


def load_metric(path, metric_day_1, metric_day_end, metric_name):
    metric_score = np.load(path)
    index = pd.date_range(metric_day_1, metric_day_end, freq='D').strftime('%m/%d/%y')
    columns = [metric_name]
    metric_score_df = pd.DataFrame(metric_score, index=index, columns=columns)
    return metric_score_df


# overlap key terms' document frequency with state covid data
def overlap_docfreq(daily_states_data, state, docfreq, media_name):
    daily_onestate_data = daily_states_data[[state]]
    roll7_state_data = daily_onestate_data.rolling(7).mean()
    roll7_docfreq = docfreq.rolling(7).mean()

    # normalize the scale of docfreq data
    roll7_covid_np = roll7_state_data.to_numpy()[7:]    # convert to np
    roll7_metric_np = roll7_docfreq.to_numpy()[8:]
    covid_max_idx = np.argmax(roll7_covid_np)       # find idx with max val.
    metric_max_idx = np.argmax(roll7_metric_np)
    covid_max = roll7_covid_np[covid_max_idx][0]    # find max val.
    metric_max = roll7_metric_np[metric_max_idx][0]
    norm_roll7_docfreq = roll7_docfreq * (covid_max/metric_max)

    fig, ax = plt.subplots(figsize=(20, 10))
    daily_onestate_data.plot(kind='bar', ax=ax)
    roll7_state_data.plot(color='red', ax=ax)
    norm_roll7_docfreq.plot(color='green', ax=ax)
    ax.legend(['7-day running average of cases',
               'Normalized 7-day running avg of %s doc frequency' % media_name,
               'actual daily cases'])
    plt.grid()
    ax.xaxis_date()
    my_xLocator = mticker.MultipleLocator(7)
    ax.xaxis.set_major_locator(my_xLocator)
    my_yLocator = mticker.MultipleLocator(1000)
    ax.yaxis.set_major_locator(my_yLocator)
    fig.autofmt_xdate()
    plt.title("Daily Cases and 7-Day Running Average for %s State" % state)
    plt.xlabel('Dates')
    plt.ylabel('Daily new cases & Normalized document frequency')
    # plt.show()
    try:
        plt.savefig(
            './plots/overlap/doc_freq/%s/tweetfreq_%s.png' % (state, media_name))
    except FileNotFoundError:
        mkdir_p("./plots/overlap/doc_freq/%s" % state)
        plt.savefig(
            './plots/overlap/doc_freq/%s/tweetfreq_%s.png' % (state, media_name))


# overlap sentiment score and state covid data
def overlap_sentiscore(daily_states_data, state, senti_score, media_name):
    daily_onestate_data = daily_states_data[[state]]
    roll7_state_data = daily_onestate_data.rolling(7).mean()
    roll7_senti_score = senti_score.rolling(7).mean()

    # normalize the scale of docfreq data
    roll7_covid_np = roll7_state_data.to_numpy()[7:]    # convert to np
    roll7_metric_np = np.absolute(roll7_senti_score.to_numpy()[8:])
    covid_max_idx = np.argmax(roll7_covid_np)       # find idx with max val.
    metric_max_idx = np.argmax(roll7_metric_np)
    covid_max = roll7_covid_np[covid_max_idx][0]    # find max val.
    metric_max = roll7_metric_np[metric_max_idx][0]
    norm_roll7_senti_score = roll7_senti_score * (covid_max/metric_max)

    fig, ax = plt.subplots(figsize=(20, 10))
    daily_onestate_data.plot(kind='bar', ax=ax)
    roll7_state_data.plot(color='red', ax=ax)
    norm_roll7_senti_score.plot(color='green', ax=ax)
    # ax.legend(['7-day running average of cases', 'actual daily cases'])
    ax.legend(['7-day running average of cases',
               'Normalized 7-day running avg of %s Sentiment Scores' % media_name,
               'actual daily cases'])
    plt.grid()
    my_xLocator = mticker.MultipleLocator(7)
    ax.xaxis.set_major_locator(my_xLocator)
    my_yLocator = mticker.MultipleLocator(1000)
    ax.yaxis.set_major_locator(my_yLocator)
    fig.autofmt_xdate()
    plt.title("Daily Cases and 7-Day Running Average for %s State" % state)
    plt.xlabel('Dates')
    plt.ylabel('Daily new cases & Normalized sentiment score')
    # plt.show()
    try:
        plt.savefig('./plots/overlap/senti_score/%s/senti_score_%s.png' % (
        state, media_name))
    except FileNotFoundError:
        mkdir_p("./plots/overlap/senti_score/%s" % state)
        plt.savefig('./plots/overlap/senti_score/%s/senti_score_%s.png' % (
        state, media_name))


if __name__ == "__main__":
    # read covid data
    data = pd.read_csv("./data/time_series_covid19_confirmed_US.csv",
                       delimiter=',', index_col=0)
    temp = data.groupby(['Province_State']).sum()
    all_states_data = (temp.iloc[:, 5:]).T  # accumulative cases group by state
    daily_states_data = all_states_data.diff()  # daily cases group by state
    us_temp = data.groupby(['Country_Region']).sum()
    us_data = (us_temp.iloc[:, 5:]).T  # accumulative cases of US
    daily_us_data = us_data.diff()  # daily cases of US

    # .npy file path of metric data
    state_abbr = 'TX'
    senti_path = "./data/%s_senti.npy" % state_abbr
    tweetfreq_path = "./data/%s_tweet_freq.npy" % state_abbr

    # select dates
    metric_day_1 = datetime.strptime("3/20/20", "%m/%d/%y")
    metric_day_end = datetime.strptime("9/30/20", "%m/%d/%y")
    covid_day_1 = datetime.strptime("1/22/20", "%m/%d/%y")

    # load metric data
    senti_score_df = load_metric(senti_path, metric_day_1, metric_day_end, metric_name="senti_score")
    tweetfreq_df = load_metric(tweetfreq_path, metric_day_1, metric_day_end, metric_name="tweet frequency")

    # truncate covid case data
    diff = (metric_day_1 - covid_day_1).days
    duration = (metric_day_end - metric_day_1).days
    daily_states_data = daily_states_data[diff:]
    daily_states_data = daily_states_data[:duration + 1]

    # -------------------------------------------------------------------------#
    #                Metric 1: Key Terms' Tweet Frequency                      #
    # -------------------------------------------------------------------------#
    # select state of interest
    state_of_interest = 'Texas'
    # select plotting option
    m1_option = 1 # choose [1, 2, 3, 4], 0 for pass

    # Option 1 (state): plot sentiment scores
    if m1_option == 1:
        overlap_docfreq(daily_states_data, state_of_interest, tweetfreq_df, 'twitter')

    # -------------------------------------------------------------------------#
    #                        Metric 2: Sentiment Score                         #
    # -------------------------------------------------------------------------#
    # select state of interest
    state_of_interest = 'Texas'
    # select plotting option
    m2_option = 1  # choose [1, 2, 3, 4], 0 for pass

    # Option 1 (state): plot sentiment scores from all media
    if m2_option == 1:
        overlap_sentiscore(daily_states_data, state_of_interest, senti_score_df, 'twitter')


########################################
# senti_path = "./data/senti.npy"
# tweetfreq_path = "./data/tweet_freq.npy"
#
# senti_score = np.load(senti_path)
# tweetfreq = np.load(tweetfreq_path)
#
# # plt.plot(senti_score)
# plt.plot(tweetfreq)
# plt.show()