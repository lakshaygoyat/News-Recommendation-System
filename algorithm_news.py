#!/usr/bin/env python
# coding:utf-8


"""
    This algorithm class has methods for training the algorithm which classifies the news into their sections
"""

# Imports
import pickle
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.feature_extraction.text import TfidfVectorizer
from nltk.corpus import stopwords



class Algorithm(object):
    
    def __init__(self):
        # Dataframe to keep the data
        self.data = pd.DataFrame()

        # Set the algorithm's model and its text vectorizer
        self.model = LogisticRegression()
        self.tfidf = TfidfVectorizer(stop_words = 'english', ngram_range=(1,1), max_features=10000, min_df=50, max_df=.25, analyzer='word')


    def loaddata(self, filename):
        """
        Loads the data

        filename (string): filename of the pickled data
        returns nothing
        """
        self.data = pd.read_pickle('/home/saksam/test/' + "data/" + filename)


    def fitdata(self):
        """
        Parametrizes the Tfidf vectorizer and trains the classifier

        returns nothing
        """
        # Vectorize the data
        print "Vectorizing the data..."
        X, y = self.tfidf.fit_transform(self.data.Allwords).todense(), self.data.Label
        print "Vectorization done\n"

	
        # Fit the model
        print "Fitting the model..."
        self.model.fit(X, y)
        print "Fitting done\n"
	

    def writemodel(self, filename_model, filename_tfidf, filename_stopwords):
        """
        Writes the model and the Tfidf vectorizer to pickle

        filename_model (string): filename of the pickled model
        filename_tfidf (string): filename of the pickled tfidf vectorizer
        returns nothing
        """
        with open('/home/saksam/test/' + "data/" + filename_model, 'w') as f:
            pickle.dump(self.model, f)
        with open('/home/saksam/test/' + "data/" + filename_tfidf, 'w') as f:
            pickle.dump(self.tfidf, f)

        # We need a pickled version of the stopwords for the website, as it's difficult to download the stopword corpus in the heroku cloud
        with open('/home/saksam/test/' + "data/" + filename_stopwords, 'w') as f:
            pickle.dump(stopwords.words('english'), f)



def main():
    """
    Main function
    """
    MyAlgorithm = Algorithm()
    MyAlgorithm.loaddata(filename = "clean_nyt_training_data.pkl")
    MyAlgorithm.fitdata()
    MyAlgorithm.writemodel(filename_model = "log_regression_model.pkl", filename_tfidf = "tfidf_vectorizer.pkl", filename_stopwords = "stopwords.pkl")



if __name__ == '__main__':
    main()
