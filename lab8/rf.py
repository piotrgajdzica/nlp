import pandas as pd
from nltk import map_tag
from nltk import pos_tag
from nltk import sent_tokenize
from nltk import word_tokenize
from nltk.corpus import stopwords

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import classification_report
from sklearn.model_selection import GridSearchCV
from sklearn.model_selection import StratifiedShuffleSplit
from sklearn.multiclass import OneVsRestClassifier
from sklearn.pipeline import Pipeline
from sklearn.svm import LinearSVC
from sklearn.svm import SVC

# Load NLTK's English stop-words list


#
# embeddings vector representations
#

def tag_pos(x):
    sentences = sent_tokenize(x.decode("utf8"))
    sents = []
    for s in sentences:
        text = word_tokenize(s)
        pos_tagged = pos_tag(text)
        simplified_tags = [
            (word, map_tag('en-ptb', 'universal', tag)) for word, tag in pos_tagged]
        sents.append(simplified_tags)
    return sents


def post_tag_documents(data_df):
    x_data = []
    y_data = []
    total = len(data_df['plot'].as_matrix().tolist())
    plots = data_df['plot'].as_matrix().tolist()
    genres = data_df.drop(['plot', 'title', 'plot_lang'], axis=1).as_matrix()
    for i in range(len(plots)):
        sents = tag_pos(plots[i])
        x_data.append(sents)
        y_data.append(genres[i])
        i += 1
        if i % 5000 == 0:
            print i, "/", total

    return x_data, y_data



# train classifiers and argument handling
#

def train_test_svm(x_data, y_data, genres):

    stratified_split = StratifiedShuffleSplit(n_splits=2, test_size=0.33)
    for train_index, test_index in stratified_split.split(x_data, y_data):
        x_train, x_test = x_data[train_index], x_data[test_index]
        y_train, y_test = y_data[train_index], y_data[test_index]

    """
    print "LinearSVC"
    pipeline = Pipeline([
        ('clf', OneVsRestClassifier(LinearSVC(), n_jobs=1)),
    ])
    parameters = {
        "clf__estimator__C": [0.01, 0.1, 1],
        "clf__estimator__class_weight": ['balanced', None],
    }
    grid_search(x_train, y_train, x_test, y_test, genres, parameters, pipeline)

    print "LogisticRegression"
    pipeline = Pipeline([
        ('clf', OneVsRestClassifier(LogisticRegression(solver='sag'), n_jobs=1)),
    ])
    parameters = {
        "clf__estimator__C": [0.01, 0.1, 1],
        "clf__estimator__class_weight": ['balanced', None],
    }
    grid_search(x_train, y_train, x_test, y_test, genres, parameters, pipeline)
    """

    print "LinearSVC"
    pipeline = Pipeline([
        ('clf', OneVsRestClassifier(SVC(), n_jobs=1)),
    ])
    """
    parameters = {
        "clf__estimator__C": [0.01, 0.1, 1],
        "clf__estimator__class_weight": ['balanced', None],
    }
    """
    parameters = [

        {'clf__estimator__kernel': ['rbf'],
         'clf__estimator__gamma': [1e-3, 1e-4],
         'clf__estimator__C': [1, 10]
        },

        {'clf__estimator__kernel': ['poly'],
         'clf__estimator__C': [1, 10]
        }
         ]

    grid_search(x_train, y_train, x_test, y_test, genres, parameters, pipeline)


def grid_search(train_x, train_y, test_x, test_y, genres, parameters, pipeline):
    grid_search_tune = GridSearchCV(pipeline, parameters, cv=2, n_jobs=3, verbose=10)
    grid_search_tune.fit(train_x, train_y)

    print
    print("Best parameters set:")
    print grid_search_tune.best_estimator_.steps
    print

    # measuring performance on test set
    print "Applying best classifier on test data:"
    best_clf = grid_search_tune.best_estimator_
    predictions = best_clf.predict(test_x)

    print classification_report(test_y, predictions, target_names=genres)



def main():
    classifier = 'linearSVC'
    vectors = 'tfidf'
    # load pre-processed data
    print "Loading already processed training data"
    data_df = pd.read_csv("training/full_text/labeled.txt", delimiter='\t')

    test_data_df = pd.read_csv("testing/ten_percent/labeled.txt", delimiter='\t')
    # all the list of genres to be used by the classification report
    genres = list(data_df.drop(['text'], axis=1).columns.values)
    test_genres = list(data_df.drop(['text'], axis=1).columns.values)

    if vectors == 'tfidf':

        # split the data, leave 1/3 out for testing
        data_x = data_df[['text']].as_matrix()
        data_y = data_df.drop(['text'], axis=1).as_matrix()


        test_data_x = test_data_df[['text']].as_matrix()
        test_data_y = test_data_df.drop(['text'], axis=1).as_matrix()
        # stratified_split = StratifiedShuffleSplit(n_splits=2, test_size=0.33)
        # for train_index, test_index in stratified_split.split(data_x, data_y):
        #     x_train, x_test = data_x[train_index], data_x[test_index]
        #     y_train, y_test = data_y[train_index], data_y[test_index]

        # transform matrix of plots into lists to pass to a TfidfVectorizer
        train_x = [x[0] for x in data_x.tolist()]
        y_train = [x[0] for x in data_y.tolist()]
        y_test = [x[0]for x in test_data_y.tolist()]
        test_x = [x[0] for x in test_data_x.tolist()]
        # train_x = [x[0].strip() for x in x_train.tolist()]
        # test_x = [x[0].strip() for x in x_test.tolist()]



        if classifier == 'linearSVC':
            # LinearSVC
            pipeline = Pipeline([
                ('tfidf', TfidfVectorizer()),
                ('clf', OneVsRestClassifier(LinearSVC(), n_jobs=1)),
            ])
            parameters = {
                'tfidf__max_df': (0.25, 0.5, 0.75),
                'tfidf__ngram_range': [(1, 1), (1, 2), (1, 3)],
                "clf__estimator__C": [0.01, 0.1, 1],
                "clf__estimator__class_weight": ['balanced', None],
            }
            grid_search(train_x, y_train, test_x, y_test, genres, parameters, pipeline)
            print('ten_percent')
            exit(-1)






if __name__ == "__main__":
    main()
