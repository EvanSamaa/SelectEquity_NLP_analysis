import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer
import re
from sklearn.cluster import KMeans
from utilities import *


def normalize_texts(texts):
    NON_ALPHANUM = re.compile(r'[\W]')
    NON_ASCII = re.compile(r'[^a-z0-1\s]')
    normalized_texts = ''
    lower = texts.lower()
    no_punctuation = NON_ALPHANUM.sub(r' ', lower)
    no_non_ascii = NON_ASCII.sub(r'', no_punctuation)
    return no_non_ascii


def get_top_n_words(corpus, n=10):
    vec = CountVectorizer(stop_words='english').fit(corpus)
    bag_of_words = vec.transform(corpus)
    sum_words = bag_of_words.sum(axis=0)
    words_freq = [(word, sum_words[0, idx]) for word, idx in vec.vocabulary_.items()]
    words_freq =sorted(words_freq, key = lambda x: x[1], reverse=True)
    return words_freq[:n]


def load_word2vec():
    # importing wordtovec embeddings
    from gensim.models import KeyedVectors
    pretrained_embeddings_path = "./GoogleNews-vectors-negative300.bin.gz"     # download at: https://s3.amazonaws.com/dl4j-distribution/GoogleNews-vectors-negative300.bin.gz
    word2vec = KeyedVectors.load_word2vec_format(pretrained_embeddings_path, binary=True)
    return word2vec


class WordVecVectorizer(object):
    def __init__(self, word2vec):
        self.word2vec = word2vec
        self.dim = 300

    def fit(self, X, y):
        return self

    def transform(self, X):
        return np.array([
            np.mean([self.word2vec[w] for w in texts.split() if w in self.word2vec]
                    or [np.zeros(self.dim)], axis=0)
            for texts in X
        ])


def elbow(X_train_wtv):
    wcss = []
    # this loop will fit the k-means algorithm to our data and
    # second we will compute the within cluster sum of squares and #appended to our wcss list.
    for i in range(1, 11):
        kmeans = KMeans(n_clusters=i, init='random', max_iter=300, n_init=10, random_state=0)
        # i above is between 1-10 numbers. init parameter is the random #initialization method
        # we select kmeans++ method. max_iter parameter the maximum number of iterations there can be to
        # find the final clusters when the K-meands algorithm is running. we #enter the default value of 300
        # the next parameter is n_init which is the number of times the #K_means algorithm will be run with
        # different initial centroid.
        kmeans.fit(X_train_wtv)
        # kmeans algorithm fits to the X dataset
        wcss.append(kmeans.inertia_)

    # kmeans inertia_ attribute is:  Sum of squared distances of samples #to their closest cluster center.
    # 4.Plot the elbow graph
    plt.plot(range(1, 11), wcss)
    plt.title('The Elbow Method Graph')
    plt.xlabel('Number of clusters')
    plt.ylabel('WCSS')
    plt.show()
    plt.savefig('./plots/elbow_graph.png')


def project_clustering_2d(embedding_dict, y_km_dict):
    X_train_wtv = np.concatenate((embedding_dict["Jan"][0], embedding_dict["Feb"][0], embedding_dict["Mar"][0], embedding_dict["Apr"][0], embedding_dict["May"][0]), axis=0)
    y_km = np.concatenate((y_km_dict["Jan"], y_km_dict["Feb"], y_km_dict["Mar"], y_km_dict["Apr"], y_km_dict["May"]), axis=0)

    from sklearn.discriminant_analysis import LinearDiscriminantAnalysis as LDA
    lda = LDA(n_components=2)  # 2-dimensional LDA

    lda_transformed = pd.DataFrame(lda.fit_transform(X_train_wtv, y_km))
    return lda_transformed, y_km


def plot_clustering_separate(month_list, embedding_dict, lda_transformed, y_km, num_cluster):
    for month in month_list:
        if month == 'Jan':
            start = 0
            end = embedding_dict[month][1]
        else:
            start = end
            end += embedding_dict[month][1]
        lda_transformed_slice = lda_transformed.iloc[start:end]
        y_km_slice = y_km[start:end]

        fig, ax = plt.subplots()
        for i in range(num_cluster):
            ax.scatter(lda_transformed_slice[y_km_slice == i][0], lda_transformed_slice[y_km_slice == i][1], s=100, label='Cluster %s' % str(i+1))
        ax.legend()
        try:
            plt.savefig('./plots/same_angle/%s_clustering_%s.png' % (month, str(num_cluster)))
        except FileNotFoundError:
            mkdir_p("./plots/same_angle")
            plt.savefig('./plots/same_angle/%s_clustering_%s.png' % (month, str(num_cluster)))
        plt.close()


if __name__ == "__main__":
    word2vec = load_word2vec()
    print('done loading word2vec')

    month_list = ['Jan', 'Feb', 'Mar', 'Apr', 'May']
    path_dict = {'Jan': 'FT_all_between_1and2_title.csv', 'Feb': 'FT_all_between_2and3_title.csv', 'Mar': 'FT_all_between_3and4_title.csv',
                 'Apr': 'FT_all_between_4and5_title.csv', 'May': 'FT_all_between_5and6_title.csv'}
    embedding_dict = {'Jan': None, 'Feb': None, 'Mar': None, 'Apr': None, 'May': None}
    y_km_dict = {'Jan': None, 'Feb': None, 'Mar': None, 'Apr': None, 'May': None}
    for month in month_list:
        # our dataframe
        csv_path = './data/' + path_dict[month]
        headlines = pd.read_csv(csv_path, parse_dates=[0], infer_datetime_format=True)
        headlines.index = headlines['date']

        # normalize and split
        headlines['title'] = headlines['title'].apply(normalize_texts)
        headlines['title'] = headlines['title'].apply(lambda x: ' '.join([w for w in x.split() if len(w) > 2]))

        X = headlines.loc[:, 'title'].values
        count_vect = CountVectorizer(lowercase=True)
        count_vect = count_vect.fit(X)
        X_sparse = count_vect.transform(X)
        vocab = count_vect.vocabulary_
        vocab_inverse = {}
        for word, int_embedding in vocab.items():
            vocab_inverse[int_embedding] = word
        total_words = X_sparse.sum()
        total_words_unique = len(count_vect.vocabulary_)
        print('\ntotal_words: {}'.format(total_words))
        print('total_words_unique: {}'.format(total_words_unique))

        X_train = pd.DataFrame(X)
        X_train.columns = ['head_line']

        # representing each headline by the mean of word embeddings for the words used in the headlines.
        wtv_vect = WordVecVectorizer(word2vec)
        X_train_wtv = wtv_vect.transform(X_train.head_line)
        print(X_train_wtv.shape)
        print('done embedding')
        embedding_dict[month] = (X_train_wtv, X_train_wtv.shape[0])

        # K-Means clustering
        num_cluster = 5
        km = KMeans(n_clusters=num_cluster, init='random', n_init=10, max_iter=300, tol=1e-04, random_state=0)
        y_km = km.fit_predict(X_train_wtv)
        y_km_dict[month] = y_km
        cluster_df = pd.DataFrame({'headlines': X_train.head_line, 'topic_cluster': y_km})
        # print(cluster_df.head())
        print('done clustering')
        cluster_df["month"] = month

        # top words in each cluster
        print("In %s" % month)
        for c in range(num_cluster):
            words = []
            word_values = []
            for i, j in get_top_n_words(cluster_df[cluster_df['topic_cluster'] == c]['headlines'], 15):
                words.append(i)
                word_values.append(j)
            print("Top words in cluster %s are:" % str(c+1), words)

    # combine vectors from each month -> project to 2d simultaneously
    lda_transformed, y_km = project_clustering_2d(embedding_dict, y_km_dict)

    # separate by month and plot individually
    plot_clustering_separate(month_list, embedding_dict, lda_transformed, y_km, num_cluster=5)
