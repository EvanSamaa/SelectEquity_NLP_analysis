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


def plot_clustering_separate(X_train_wtv, y_km, num_cluster, numvec_dict, month_list):
    from sklearn.decomposition import PCA
    from sklearn.discriminant_analysis import LinearDiscriminantAnalysis as LDA
    pca = PCA(n_components=2)
    lda = LDA(n_components=2)  # 2-dimensional LDA

    lda_transformed = pd.DataFrame(lda.fit_transform(X_train_wtv, y_km))

    for month in month_list:
        if month == 'Jan':
            start = 0
            end = numvec_dict[month]
        else:
            start = end
            end += numvec_dict[month]
        lda_transformed_slice = lda_transformed.iloc[start:end]
        y_km_slice = y_km[start:end]

        fig, ax = plt.subplots()
        for i in range(num_cluster):
            ax.scatter(lda_transformed_slice[y_km_slice == i][0], lda_transformed_slice[y_km_slice == i][1], s=100, label='Cluster %s' % str(i+1))
            ax.legend()
        try:
            plt.savefig('./plots/same_angle_2/%s_clustering_%s.png' % (month, str(num_cluster)))
        except FileNotFoundError:
            mkdir_p("./plots/same_angle_2")
            plt.savefig('./plots/same_angle_2/%s_clustering_%s.png' % (month, str(num_cluster)))
        plt.close()


def cluster_distance(X_train_wtv, y_km, num_cluster, numvec_dict, month_list):
    # step 1: find cluster heads, defined as the mean of all vectors in the cluster
    cluster_heads = {'Jan': [], 'Feb': [], 'Mar': [], 'Apr': [], 'May': []}
    for month in month_list:
        if month == 'Jan':
            start = 0
            end = numvec_dict[month]
        else:
            start = end
            end += numvec_dict[month]
        X_train_wtv_slice = X_train_wtv[start:end]
        y_km_slice = y_km[start:end]

        for i in range(num_cluster):
            temp = X_train_wtv_slice[y_km_slice == i].mean(axis=0).reshape(1, 300)
            cluster_heads[month].append(temp)

        # step 2: calculate pointwise distance between cluster heads in the same month
        print("\n%s" % month)
        for i in range(num_cluster):
            print(" ")
            for j in range(num_cluster):
                # print(cluster_heads[month][i] - cluster_heads[month][j])
                euc_dist = np.linalg.norm(cluster_heads[month][i] - cluster_heads[month][j])    # euclidean distance
                print("The euclidean distance between cluster %d and %d is: %f" % (i+1, j+1, euc_dist))
                # from scipy.spatial import distance
                # cos_dist = distance.cosine(cluster_heads[month][i][0], cluster_heads[month][j][0])
                # cos_sim = np.dot(cluster_heads[month][i], cluster_heads[month][j].T) / (np.linalg.norm(cluster_heads[month][i]) * np.linalg.norm(cluster_heads[month][j]))
                # print("The cosine distance between cluster %d and %d is: %f" % (i + 1, j + 1, cos_dist))

    print("-----------------------------------------------------------------------------------------------------------")
    # step 3: calculate pointwise distance between the same cluster's head in different months
    for month_i in month_list:
        print("\n%s" % month_i)
        for month_j in month_list:
            print(" ")
            for ii in range(num_cluster):
                euc_dist = np.linalg.norm(cluster_heads[month_i][ii] - cluster_heads[month_j][ii])  # euclidean distance
                print("The euclidean distance of cluster %d between %s and %s is: %f" % (ii+1, month_i, month_j, euc_dist))


if __name__ == "__main__":
    word2vec = load_word2vec()
    print('done loading word2vec')

    month_list = ['Jan', 'Feb', 'Mar', 'Apr', 'May']
    path_dict = {'Jan': 'FT_all_between_1and2_title.csv', 'Feb': 'FT_all_between_2and3_title.csv', 'Mar': 'FT_all_between_3and4_title.csv',
                 'Apr': 'FT_all_between_4and5_title.csv', 'May': 'FT_all_between_5and6_title.csv'}
    numvec_dict = {'Jan': None, 'Feb': None, 'Mar': None, 'Apr': None, 'May': None}
    for month in month_list:
        csv_path = './data/' + path_dict[month]
        if month != 'Jan':
            temp_headlines = pd.read_csv(csv_path, parse_dates=[0], infer_datetime_format=True)
            headlines = pd.concat([headlines, temp_headlines], ignore_index=True)
            numvec_dict[month] = temp_headlines.shape[0]
        else:
            headlines = pd.read_csv(csv_path, parse_dates=[0], infer_datetime_format=True)
            numvec_dict[month] = headlines.shape[0]
    headlines.index = headlines['date']
    print("numvec_dict: ", numvec_dict)

    # normalize and split
    headlines['title'] = headlines['title'].apply(normalize_texts)
    headlines['title'] = headlines['title'].apply(lambda x: ' '.join([w for w in x.split() if len(w) > 2]))
    # print(headlines.head())
    # top_n_words = get_top_n_words(headlines['title'], 15)
    # print(top_n_words)

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
    print('total_words: {}'.format(total_words))
    print('total_words_unique: {}'.format(total_words_unique))

    X_train = pd.DataFrame(X)
    # headlines_smaller = X_train.sample(frac=0.2, random_state=423)
    X_train.columns = ['head_line']

    # representing each headline by the mean of word embeddings for the words used in the headlines.
    wtv_vect = WordVecVectorizer(word2vec)
    X_train_wtv = wtv_vect.transform(X_train.head_line)
    print(X_train_wtv.shape)
    print('done embedding')

    # K-Means clustering
    num_cluster = 5

    km = KMeans(n_clusters=num_cluster, init='random', n_init=10, max_iter=300, tol=1e-04, random_state=0)
    y_km = km.fit_predict(X_train_wtv)
    cluster_df = pd.DataFrame({'headlines': X_train.head_line, 'topic_cluster': y_km})
    # print(cluster_df.head())
    print('done clustering')

    # use elbow method to find optimal K value
    # elbow(X_train_wtv)

    # top words in each cluster
    for c in range(num_cluster):
        words = []
        word_values = []
        for i, j in get_top_n_words(cluster_df[cluster_df['topic_cluster'] == c]['headlines'], 15):
            words.append(i)
            word_values.append(j)
        print("Top words in cluster %s are:" % str(c+1), words)

    # plot clustering
    # plot_clustering_separate(X_train_wtv, y_km, num_cluster, numvec_dict, month_list)

    # calculate point-wise cluster distance
    cluster_distance(X_train_wtv, y_km, num_cluster, numvec_dict, month_list)