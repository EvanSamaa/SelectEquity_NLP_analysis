import nltk
import nltk.classify.util #calculates accuracy
from nltk.classify import NaiveBayesClassifier #imports the classifier Naive Bayes
from nltk.corpus import movie_reviews #imports movie reviews from nltk
from nltk.corpus import stopwords #imports stopwords from nltk
from nltk.corpus import wordnet #imports wordnet(lexical database for the english language) from nltk
from nltk.tokenize import RegexpTokenizer, word_tokenize
from nltk.stem import SnowballStemmer
import pickle
import pandas as pd
from datetime import datetime
from matplotlib import pyplot as plt
import numpy as np


class NBClassifier():
    def __init__(self, model_path):
        nltk.download('movie_reviews')
        nltk.download('punkt')
        nltk.download('wordnet')
        self.model = load_classfier(model_path)
    def classify(self, phrase):
        tokens = self.tokenize(phrase)
        my_dict = dict([(word, True) for word in tokens])
        out = self.model.prob_classify(my_dict)
        pos_prob = out.prob("positive")
        neg_prob = out.prob("negative")

        return pos_prob, neg_prob
    def tokenize(self, phrase):
        words = phrase
        words = word_tokenize(words)
        stemmer = SnowballStemmer("english")
        words = [token.lower() for token in words]
        words = [word for word in words if word not in stopwords.words('english')]
        words = [stemmer.stem(token) for token in words]
        return words
def remove_stopwords(words, stopwords):
    words = word_tokenize(words)
    stemmer = SnowballStemmer("english")
    words = [token.lower() for token in words]
    words = [word for word in words if word not in stopwords.words('english')]
    words = [stemmer.stem(token) for token in words]
    return words
def create_word_features(phrase, stopwords, train=True):
    if train:
        useful_words = remove_stopwords(" ".join(list(phrase)), stopwords)
    else:
        useful_words = remove_stopwords(phrase, stopwords)
    my_dict = dict([(word, True) for word in useful_words])
    return my_dict
def save_classifier(classifier, file_name):
    f = open(file_name, 'wb')
    pickle.dump(classifier, f)
    f.close()
def load_classfier(file_name):
    f = open(file_name, 'rb')
    classifier = pickle.load(f)
    f.close()
    return classifier
def train_bayes(file_csv):
    nltk.download('movie_reviews')
    nltk.download('punkt')
    nltk.download('wordnet')
    neg_reviews = []
    pos_reviews = []
    counter = 0
    neg_count = 0
    pos_count = 0
    training_set = pd.read_csv(file_csv, error_bad_lines=False, encoding="latin-1", header=0)
    for row in training_set.iterrows():
        if neg_count >= 100000 and pos_count >= 100000:
            break
        if row[1][0] == 0:
            if neg_count <= 100000:
                neg_reviews.append((create_word_features(row[1][5], stopwords, False), "negative"))
                neg_count = neg_count + 1
        if row[1][0] != 0:
            if pos_count <= 100000:
                pos_reviews.append((create_word_features(row[1][5], stopwords, False), "positive"))
                pos_count = pos_count + 1
        counter += 1
        if counter % 10 == 0:
            print("{} document modified".format(counter))
    train_set = neg_reviews[:-1000] + pos_reviews[:-1000]
    test_set = neg_reviews[-1000:] + pos_reviews[-1000:]
    classifier = NaiveBayesClassifier.train(train_set)
    accuracy = nltk.classify.util.accuracy(classifier, test_set)
    print(accuracy)
    save_classifier(classifier, "./NB_baseline.pickle")
def frequency_count():
    count = np.zeros((1000, 4))
    df = pd.read_csv("../APIs/data/covid_new_keyword.csv")
    day_1 = datetime.strptime("2019-10-10", "20%y-%m-%d")
    for index, row in df.iterrows():
        date_diff = (datetime.strptime(row['date'], "20%y-%m-%d") - day_1).days
        if row['publisher'] == "CNN":
            count[date_diff, 0] += 1
        elif row['publisher'] == "FinancialTimes":
            count[date_diff, 1] += 1
        elif row['publisher'] == "NYtimes":
            count[date_diff, 2] += 1
        elif row['publisher'] == "The Guardian":
            count[date_diff, 3] += 1
    np.save("frequency_count.npy", count)
def moving_average(a, n=3) :
    ret = np.cumsum(a, dtype=float)
    ret[n:] = ret[n:] - ret[:-n]
    return ret[n - 1:] / n
if __name__ == "__main__":
    # polarty is used in this paper
    #   https://webdocs.cs.ualberta.ca/~zaiane/postscript/dawak17.pdf

    df = pd.read_excel("alldata.xlsx")
    TP = 0
    TN = 0
    FP = 0
    FN = 0
    model = NBClassifier("NB_baseline.pickle")
    for index, row in df.iterrows():
        pos_prob, neg_prob = model.classify(row["Title"])
        if pos_prob >= 0.5 and row["Label"] == "pos":
            TP = TP + 1
        elif pos_prob >= 0.5 and row["Label"] == "neg":
            FP = FP + 1
        elif neg_prob >= 0.5 and row["Label"] == "pos":
            FN = FN + 1
        elif neg_prob >= 0.5 and row["Label"] == "neg":
            TN = TN + 1
    print(TP, TN, FP, FN)

    A[2]

    # train_bayes("../APIs/data/training.1600000.processed.noemoticon.csv")
    # plt.title("The Guardian")
    # figure, axes = plt.subplots(nrows=3, ncols=1)
    # count = np.load("DifferentKeyWord/novel virus_article_count.npy")
    # axes[0].plot(count.sum(axis=1)[:370])
    # axes[0].set_title("novel virus")
    # count = np.load("DifferentKeyWord/SARS_article_count.npy")
    # axes[1].set_ylabel("Number of Articles")
    # axes[1].set_title("SARS")
    # axes[1].plot(count.sum(axis=1)[:370])
    # count = np.load("DifferentKeyWord/covid-19_article_count.npy")
    # axes[2].set_title("covid-19")
    # axes[2].plot(count.sum(axis=1)[:370])
    # figure.tight_layout(pad=1.0)
    # plt.xlabel("Days since Oct 10 2019")
    # plt.show()
    # A[2]
    model = NBClassifier("NB_baseline.pickle")
    df = pd.read_csv("../APIs/data/covid_by_keyword.csv")
    count = np.zeros((1000, 4))
    pos_count = np.zeros((1000, 4))
    neg_count = np.zeros((1000, 4))
    cts_sum = np.zeros((1000, 4))
    day_1 = datetime.strptime("2019-10-10", "20%y-%m-%d")
    for index, row in df.iterrows():
        date_diff = (datetime.strptime(row['date'], "20%y-%m-%d") - day_1).days
        try:
            pos_prob, neg_prob = model.classify(row["raw_body"] + " " + row["title"])
            if row['publisher'] == "CNN":
                count[date_diff, 0]= count[date_diff, 0] + 1
                if pos_prob > 0.5:
                    pos_count[date_diff, 0] += 1
                else:
                    neg_count[date_diff, 0] += 1
                cts_sum[date_diff, 0] += pos_prob-0.5
            elif row['publisher'] == "FinancialTimes":
                count[date_diff, 1] = count[date_diff, 1] + 1
                if pos_prob > 0.5:
                    pos_count[date_diff, 1] += 1
                else:
                    neg_count[date_diff, 1] += 1
                cts_sum[date_diff, 1] += pos_prob - 0.5
            elif row['publisher'] == "NYtimes":
                count[date_diff, 2] = count[date_diff, 2] + 1
                if pos_prob > 0.5:
                    pos_count[date_diff, 2] += 1
                else:
                    neg_count[date_diff, 2] += 1
                cts_sum[date_diff, 2] += pos_prob - 0.5
            elif row['publisher'] == "The Guardian":
                count[date_diff, 3] = count[date_diff, 2] + 1
                if pos_prob > 0.5:
                    pos_count[date_diff, 3] += 1
                else:
                    neg_count[date_diff, 3] += 1
                cts_sum[date_diff, 3] += pos_prob - 0.5
        except:
            print(row)
    polarity = np.divide((pos_count - neg_count), count+1)
    np.save("polarity_time_series.npy", polarity)
    np.save("positive_articles_time_series.npy", pos_count)
    np.save("negative_articles_time_series.npy", neg_count)
    np.save("pos-neg_time_series.npy", pos_count-neg_count)
    np.save("pos_prob-neg_prob_time_series.npy", pos_count - neg_count)
