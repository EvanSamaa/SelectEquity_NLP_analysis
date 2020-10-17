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
        out = self.model.classify(my_dict)
        print(out)
        return out
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


if __name__ == "__main__":

    # plottt = np.load("bays_sentiment.npy")
    # plt.plot(plottt)
    # plt.show()
    # train_bayes("../APIs/data/training.1600000.processed.noemoticon.csv")



    model = NBClassifier("NB_baseline.pickle")
    df = pd.read_csv("../APIs/data/covid.csv")
    count = np.zeros((1000, 4))
    day_1 = datetime.strptime("2019-10-10", "20%y-%m-%d")
    for index, row in df.iterrows():
        date_diff = (datetime.strptime(row['date'], "20%y-%m-%d") - day_1).days
        if row['publisher'] == "CNN":
            count[date_diff, 0] += 1
            try:
                out = model.classify(row["title"])
                if out == "positive":
                   count[date_diff, 0] = count[date_diff, 0] + 1
                else:
                   count[date_diff, 0] = count[date_diff, 0] - 1
            except:
                print(row["title"])
        elif row['publisher'] == "FinancialTimes":
            count[date_diff, 0] += 1
            try:
                out = model.classify(row["title"])
                if out == "positive":
                    count[date_diff, 1] = count[date_diff, 1] + 1
                else:
                    count[date_diff, 1] = count[date_diff, 1] - 1
            except:
                print(row["title"])
        elif row['publisher'] == "NYtimes":
            count[date_diff, 0] += 1
            try:
                out = model.classify(row["title"])
                if out == "positive":
                    count[date_diff, 2] = count[date_diff, 2] + 1
                else:
                    count[date_diff, 2] = count[date_diff, 2] - 1
            except:
                print(row["title"])
        elif row['publisher'] == "The Guardian":
            count[date_diff, 0] += 1
            try:
                out = model.classify(row["title"])
                if out == "positive":
                    count[date_diff, 3] = count[date_diff, 3] + 1
                else:
                    count[date_diff, 3] = count[date_diff, 3] - 1
            except:
                print(row["title"])
    # plt.title("The Guardian")
    # plt.plot(np.arange(0, 1000), count[:, 0])
    # plt.plot(np.arange(0, 1000), count[:, 1])
    # plt.plot(np.arange(0, 1000), count[:, 2])
    np.save("bays_sentiment.npy", count)