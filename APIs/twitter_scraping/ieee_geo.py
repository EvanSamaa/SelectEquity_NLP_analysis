import pandas as pd
import os
import json
from matplotlib import pyplot as plt
import numpy as np


def senti_oftheday(out_path, csv_path, state):
    # load data and extract tweet_id only
    dataframe = pd.read_csv(csv_path, header=None)
    tweet_id = dataframe[0]
    tweet_id.to_csv(out_path + "/temp.txt", index=False, header=None)

    # twarc command line hydrate tweets
    os.system("cd %s && activate capstone && twarc hydrate temp.txt > temp.jsonl" % out_path)

    # load all tweets
    with open(out_path + '/temp.jsonl', 'r') as json_file:
        json_list = list(json_file)

    chosen_tweets = []
    chosen_id = []
    for json_str in json_list:
        result = json.loads(json_str)
        try:
            if result['place']['full_name'][-2:] == state:
                chosen_tweets.append(result)
                chosen_id.append(result['id'])
        except:
            continue

    tweet_freq = len(chosen_id)
    print(tweet_freq, " tweets are from %s state" % state)
    chosen_tweets_senti = dataframe[dataframe[0].isin(chosen_id)]

    # senti_aggre = chosen_tweets_senti[1].sum()
    senti_aggre = chosen_tweets_senti[1].loc[chosen_tweets_senti[1] < 0].sum()
    print("aggregate sentiment score: ", senti_aggre)

    return senti_aggre, tweet_freq


if __name__ == "__main__":
    path = "../../../ieee_covid_tweet/"     # put the tweet dataset parallel to the github folder
    dirs = os.listdir(path)
    out_path = "../../../ieee_covid_tweet/ready"
    state = 'TX'
    senti_list = []
    freq_list = []
    months = ['march', 'april', 'may', 'june', 'july', 'august', 'september', 'october']
    for (month, next_month) in zip(months, months[1:]):
        if month in ['march', 'may', 'july', 'august']:
            limit = 31
        elif month == 'october':
            limit = 7
        else:
            limit = 30
        for i in range(1, limit+1):
            if i == limit:
                csv_path = month + str(i) + '_' + next_month + str(1) + '.csv'
            else:
                csv_path = month + str(i) + '_' + month + str(i+1) + '.csv'
            try:
                print(csv_path)
                senti_aggre, tweet_freq = senti_oftheday(out_path, path+csv_path, state)
                senti_list.append(senti_aggre)
                freq_list.append(tweet_freq)
            except FileNotFoundError:
                continue

    senti_np = np.array(senti_list)
    np.save('../../covid_data/data/%s_senti.npy' % state, senti_np)
    plt.plot(senti_list)

    freq_np = np.array(freq_list)
    np.save('../../covid_data/data/%s_tweet_freq.npy' % state, freq_np)
    plt.plot(freq_list)
