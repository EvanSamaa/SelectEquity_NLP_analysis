# Include functions to evaluate metrics similarity with covid data

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
from utilities import *
from data_overlap import load_metric
from datetime import datetime


def mse_eval_docfreq(covid_df, metric_df, state, media):
    roll7_covid = covid_df.rolling(7).mean()        # rolling average
    roll7_metric = metric_df.rolling(7).mean()
    roll7_covid_np = roll7_covid.to_numpy()[7:]     # convert to np
    roll7_metric_np = roll7_metric.to_numpy()[8:]

    covid_max_idx = np.argmax(roll7_covid_np)       # find idx with max val.
    metric_max_idx = np.argmax(roll7_metric_np)
    covid_max = roll7_covid_np[covid_max_idx][0]    # find max val.
    metric_max = roll7_metric_np[metric_max_idx][0]
    norm_roll7_metric_np = roll7_metric_np * (covid_max/metric_max) * (100/covid_max)   # normalize
    norm_roll7_covid_np = roll7_covid_np * (100/covid_max)

    disp = int(covid_max_idx - metric_max_idx)
    if disp > 0:
        shift_norm_roll7_metric_np = norm_roll7_metric_np[:-disp]   # align peaks
        shift_norm_roll7_covid_np = norm_roll7_covid_np[disp:]
    elif disp < 0:
        disp = -disp
        shift_norm_roll7_metric_np = norm_roll7_metric_np[disp:]   # align peaks
        shift_norm_roll7_covid_np = norm_roll7_covid_np[:-disp]
    else:
        shift_norm_roll7_metric_np = norm_roll7_metric_np
        shift_norm_roll7_covid_np = norm_roll7_covid_np

    # plot
    fig, ax = plt.subplots(figsize=(20, 10))
    plt.plot(shift_norm_roll7_covid_np, color="red")
    plt.plot(shift_norm_roll7_metric_np, color="green")
    ax.legend(['shifted 7-day running average of cases',
               '7-day running avg of %s doc frequency' % media])
    plt.title("Shifted and Normalized Doc Freq and %s State Cases" % state)
    plt.ylabel('Normalized to a scale of 0-100')
    # plt.show()
    try:
        plt.savefig(
            './plots/overlap_eval/doc_freq/%s/eval_docfreq_%s.png' % (state, media))
    except FileNotFoundError:
        mkdir_p("./plots/overlap_eval/doc_freq/%s" % state)
        plt.savefig(
            './plots/overlap_eval/doc_freq/%s/eval_docfreq_%s.png' % (state, media))

    # compute mse
    mse = ((shift_norm_roll7_covid_np - shift_norm_roll7_metric_np)**2).mean()
    print("%s mse = " % media, mse)
    return mse


def mse_eval_docfreq_us(covid_df, metric_df, media):
    roll7_covid = covid_df.rolling(7).mean()        # rolling average
    roll7_metric = metric_df.rolling(7).mean()
    roll7_covid_np = roll7_covid.to_numpy()[7:]     # convert to np
    roll7_metric_np = roll7_metric.to_numpy()[8:]

    covid_max_idx = np.argmax(roll7_covid_np)       # find idx with max val.
    metric_max_idx = np.argmax(roll7_metric_np)
    covid_max = roll7_covid_np[covid_max_idx][0]    # find max val.
    metric_max = roll7_metric_np[metric_max_idx][0]
    norm_roll7_metric_np = roll7_metric_np * (covid_max/metric_max) * (100/covid_max)   # normalize
    norm_roll7_covid_np = roll7_covid_np * (100/covid_max)

    disp = int(covid_max_idx - metric_max_idx)
    if disp > 0:
        shift_norm_roll7_metric_np = norm_roll7_metric_np[:-disp]   # align peaks
        shift_norm_roll7_covid_np = norm_roll7_covid_np[disp:]
    elif disp < 0:
        disp = -disp
        shift_norm_roll7_metric_np = norm_roll7_metric_np[disp:]   # align peaks
        shift_norm_roll7_covid_np = norm_roll7_covid_np[:-disp]
    else:
        shift_norm_roll7_metric_np = norm_roll7_metric_np
        shift_norm_roll7_covid_np = norm_roll7_covid_np

    # plot
    fig, ax = plt.subplots(figsize=(20, 10))
    plt.plot(shift_norm_roll7_covid_np, color="red")
    plt.plot(shift_norm_roll7_metric_np, color="green")
    ax.legend(['shifted 7-day running average of cases',
               '7-day running avg of %s doc frequency' % media])
    plt.title("Shifted and Normalized Doc Freq and US Cases")
    plt.ylabel('Normalized to a scale of 0-100')
    # plt.show()
    try:
        plt.savefig(
            './plots/overlap_eval/doc_freq/US/eval_docfreq_%s.png' % media)
    except FileNotFoundError:
        mkdir_p("./plots/overlap_eval/doc_freq/US")
        plt.savefig('./plots/overlap_eval/doc_freq/US/eval_docfreq_%s.png' % media)

    # compute mse
    mse = ((shift_norm_roll7_covid_np - shift_norm_roll7_metric_np)**2).mean()
    print("%s mse = " % media, mse)
    return mse


def mse_eval_sentiscore(covid_df, metric_df, state, media):
    roll7_covid = covid_df.rolling(7).mean()        # rolling average
    roll7_metric = metric_df.rolling(7).mean()
    roll7_covid_np = roll7_covid.to_numpy()[7:]     # convert to np
    roll7_metric_np = roll7_metric.to_numpy()[8:]
    rev_roll7_metric_np = roll7_metric_np * (-1)

    covid_max_idx = np.argmax(roll7_covid_np)       # find idx with max val.
    metric_max_idx = np.argmax(rev_roll7_metric_np)
    covid_max = roll7_covid_np[covid_max_idx][0]    # find max val.
    metric_max = rev_roll7_metric_np[metric_max_idx][0]
    norm_roll7_metric_np = rev_roll7_metric_np * (covid_max/metric_max) * (100/covid_max)   # normalize
    norm_roll7_covid_np = roll7_covid_np * (100/covid_max)

    disp = int(covid_max_idx - metric_max_idx)
    if disp > 0:
        shift_norm_roll7_metric_np = norm_roll7_metric_np[:-disp]   # align peaks
        shift_norm_roll7_covid_np = norm_roll7_covid_np[disp:]
    elif disp < 0:
        disp = -disp
        shift_norm_roll7_metric_np = norm_roll7_metric_np[disp:]   # align peaks
        shift_norm_roll7_covid_np = norm_roll7_covid_np[:-disp]
    else:
        shift_norm_roll7_metric_np = norm_roll7_metric_np
        shift_norm_roll7_covid_np = norm_roll7_covid_np

    # plot
    fig, ax = plt.subplots(figsize=(20, 10))
    plt.plot(shift_norm_roll7_covid_np, color="red")
    plt.plot(shift_norm_roll7_metric_np, color="green")
    ax.legend(['shifted 7-day running average of cases',
               'Normalized 7-day running avg of %s Sentiment Score' % media])
    plt.title("Shifted and Normalized Sentiment Score and %s State Cases" % state)
    plt.ylabel('Normalized to a scale of 0-100')
    # plt.show()
    try:
        plt.savefig(
            './plots/overlap_eval/senti_score/%s/eval_sentiscore_%s.png' % (state, media))
    except FileNotFoundError:
        mkdir_p("./plots/overlap_eval/senti_score/%s" % state)
        plt.savefig(
            './plots/overlap_eval/senti_score/%s/eval_sentiscore_%s.png' % (state, media))

    # compute mse
    mse = ((shift_norm_roll7_covid_np - shift_norm_roll7_metric_np)**2).mean()
    print("%s mse = " % media, mse)
    return mse


def mse_eval_sentiscore_us(covid_df, metric_df, media):
    roll7_covid = covid_df.rolling(7).mean()  # rolling average
    roll7_metric = metric_df.rolling(7).mean()
    roll7_covid_np = roll7_covid.to_numpy()[7:]  # convert to np
    roll7_metric_np = roll7_metric.to_numpy()[8:]
    rev_roll7_metric_np = roll7_metric_np * (-1)

    covid_max_idx = np.argmax(roll7_covid_np)  # find idx with max val.
    metric_max_idx = np.argmax(rev_roll7_metric_np)
    covid_max = roll7_covid_np[covid_max_idx][0]  # find max val.
    metric_max = rev_roll7_metric_np[metric_max_idx][0]
    norm_roll7_metric_np = rev_roll7_metric_np * (covid_max / metric_max) * (
                100 / covid_max)  # normalize
    norm_roll7_covid_np = roll7_covid_np * (100 / covid_max)

    disp = int(covid_max_idx - metric_max_idx)
    if disp > 0:
        shift_norm_roll7_metric_np = norm_roll7_metric_np[:-disp]  # align peaks
        shift_norm_roll7_covid_np = norm_roll7_covid_np[disp:]
    elif disp < 0:
        disp = -disp
        shift_norm_roll7_metric_np = norm_roll7_metric_np[disp:]  # align peaks
        shift_norm_roll7_covid_np = norm_roll7_covid_np[:-disp]
    else:
        shift_norm_roll7_metric_np = norm_roll7_metric_np
        shift_norm_roll7_covid_np = norm_roll7_covid_np

    # plot
    fig, ax = plt.subplots(figsize=(20, 10))
    plt.plot(shift_norm_roll7_covid_np, color="red")
    plt.plot(shift_norm_roll7_metric_np, color="green")
    ax.legend(['shifted 7-day running average of cases',
               'Normalized 7-day running avg of %s Sentiment Score' % media])
    plt.title(
        "Shifted and Normalized Sentiment Score and US Cases")
    plt.ylabel('Normalized to a scale of 0-100')
    # plt.show()
    try:
        plt.savefig(
            './plots/overlap_eval/senti_score/US/eval_sentiscore_%s.png' % media)
    except FileNotFoundError:
        mkdir_p("./plots/overlap_eval/senti_score/US")
        plt.savefig(
            './plots/overlap_eval/senti_score/US/eval_sentiscore_%s.png' % media)

    # compute mse
    mse = ((shift_norm_roll7_covid_np - shift_norm_roll7_metric_np) ** 2).mean()
    print("%s mse = " % media, mse)
    return mse


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
    senti_path = "../models/bays_sentiment.npy"
    docfreq_path = "../models/frequency_count.npy"

    # select dates
    metric_day_1 = datetime.strptime("10/10/19", "%m/%d/%y")
    covid_day_1 = datetime.strptime("1/22/20", "%m/%d/%y")
    covid_day_end = datetime.strptime("10/9/20", "%m/%d/%y")

    # load metric data
    senti_media_dict = load_metric(senti_path, covid_day_1, covid_day_end,
                                   metric_day_1, metric_name="senti_score")
    docfreq_media_dict = load_metric(docfreq_path, covid_day_1, covid_day_end,
                                     metric_day_1, metric_name="doc frequency")

    # -------------------------------------------------------------------------#
    #         Evaluation of Metric 1: Key Terms' Document Frequency            #
    # -------------------------------------------------------------------------#
    # select state of interest
    state_of_interest = 'Georgia'
    # select plotting option
    m1_option = 0 # choose [1, 2, 3, 4], 0 for pass

    # Option 1 (state): plot sentiment scores from all media
    if m1_option == 1:
        for key in docfreq_media_dict.keys():
            mse = mse_eval_docfreq(daily_states_data[[state_of_interest]], docfreq_media_dict[key], state_of_interest, key)
    # Option 2 (state): select media of interest and produce 1 plot only
    elif m1_option == 2:
        media = "nyt"
        mse = mse_eval_docfreq(daily_states_data[[state_of_interest]],
                               docfreq_media_dict[media], state_of_interest, media)
    # Option 3 (US): plot sentiment scores from all media
    elif m1_option == 3:
        for key in docfreq_media_dict.keys():
            mse_eval_docfreq_us(daily_us_data, docfreq_media_dict[key], key)
    # Option 4 (US): select media of interest and produce 1 plot only
    elif m1_option == 4:
        media = "cnn"
        mse_eval_docfreq_us(daily_us_data, docfreq_media_dict[media], media)

    # -------------------------------------------------------------------------#
    #                 Evaluation of Metric 2: Sentiment Score                  #
    # -------------------------------------------------------------------------#
    # select state of interest
    state_of_interest = 'Georgia'
    # select plotting option
    m2_option = 3 # choose [1, 2, 3, 4], 0 for pass

    # Option 1 (state): plot sentiment scores from all media
    if m2_option == 1:
        for key in senti_media_dict.keys():
            mse = mse_eval_sentiscore(daily_states_data[[state_of_interest]], senti_media_dict[key], state_of_interest, key)
    # Option 2 (state): select media of interest and produce 1 plot only
    elif m2_option == 2:
        media = "nyt"
        mse = mse_eval_sentiscore(daily_states_data[[state_of_interest]], senti_media_dict[media], state_of_interest, media)
    # Option 3 (US): plot sentiment scores from all media
    if m2_option == 3:
        for key in senti_media_dict.keys():
            mse = mse_eval_sentiscore_us(daily_us_data, senti_media_dict[key], key)
    # Option 4 (US): select media of interest and produce 1 plot only
    elif m2_option == 4:
        media = "nyt"
        mse = mse_eval_sentiscore_us(daily_us_data, senti_media_dict[media], media)