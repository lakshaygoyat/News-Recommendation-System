#!/usr/bin/env python
# coding:utf-8


# Imports
import sys
import pickle
import urllib2
import httplib
import json
import numpy as np
import user_news as un
import top_news as tn
from collections import Counter
from nltk.corpus import stopwords



class Predictor(object):
    """
    Class that holds functions to recommend news to the users

    model_pickle (pickle): Pickled Logistic Regression model
    tfidf_pickle (pickle): Pickled Tfidf text vectorizer
    """

    def __init__(self, model_pickle, tfidf_pickle):
        # Load the model and the text vectorizer
        self.model = pickle.load(open('/home/saksam/test/' + "data/" + model_pickle))
        self.tfidf = pickle.load(open('/home/saksam/test/' + "data/" + tfidf_pickle))

        # Label dictionary for nice categories
        self.label_dict = {0: "India", 1: "Sports", 2: "Lifestyle", 3: "Entertainment", 4: "technology", 5: "Business", 6: "World"}
        
        # Helper list of all single alphabetic letters
        self.singleletters = [chr(i) for i in range(97,123)] + [chr(i).upper() for i in range(97,123)]


    def fetch_news(self, user):
        """
        Fetches news read by user and saves them
        user (string): user_id
        returns list of news
        """

        # List of news to be filled
        user_rnews = []
	user_read_news = un.user_data[str(user)]

        # Get the news and clean them from non-alphabetic characters. Furthermore, remove single character words.
        for text in user_read_news:
            wordlist = "".join( [char if char in self.singleletters else " " for char in text] ).split()
            cleanwordlist = [word for word in wordlist if word not in self.singleletters + ["RT"]]
            user_rnews.append(" ".join(cleanwordlist))

        # Return the news list
        return user_rnews


    def predict_class(self, news, number_of_classes):
        """
        Predicts which section of the news may be interesting for the user based on news

        news (list of strings): Aggregated news, each in one string
        number_of_classes (int): Number of classes to be recommended (It does not make much sense though, to recommend more than two or maximally three classes, beyond that it's pretty random)
        returns sorted list of most probable classes/category
        """

        # Vectorize news
        vec_news = self.tfidf.transform(news)

        # Predict label for each tweet
        pred = self.model.predict(vec_news)

        # Return most common labels
        try:
            returnlist = [Counter(pred).most_common(number_of_classes)[idx][0] for idx in range(number_of_classes)]
        except:
            print "ERROR:"
            print "It seems like you want to use more classes to recommend news than predicted by the model."
            print "Try using more news and try to predict less classes."
            sys.exit()

        return returnlist


    def recommend_article(self, news, labels):
        """
        Recommend a news based on the provided label

        labels : encoded labels of categories to be used for recommendation
        news (list of strings): Aggregated news in one string
        returns nothing
        """

            # List of Jaccard distances between articles and news
	jaccarddistances = []

            # Split news into individual words and remove stopwords
        tweetwordlist = [word for tweet in news for word in tweet.split() if word not in stopwords.words('english')]

            # Loop over all news and calculate closest news to user's news based on Jaccard distance
        for idx in range(len(tn.final_list_title)):

                # Using the news title(if possible use more details about news like content of the news)
		wordstring = tn.final_list_title[idx]

                # Clean all numbers, punktuation and everything else apart from alphabetic characters. Also remove single character words and stopwords
                wordlist = "".join( [char if char in self.singleletters else " " for char in wordstring] ).split()
                cleanwordlist = [word for word in wordlist if word not in self.singleletters + stopwords.words('english')]

                # Remove stopwords and calculate Jaccard distances and append to list
                jaccarddistances.append(self.jaccard_dist(tweetwordlist, cleanwordlist))

        # Argsort - return indices of the closest news. 
        argsortedarray = np.argsort(jaccarddistances)

        # Recommend closest news (Taking index of top 10 closest news)
        recommended = argsortedarray[0:10]
	
	#Storing news(Final result) into a dictionary
	res = {}


	first = "You are probably interested in the topic: " + self.label_dict[labels[0]]
	if len(labels)==2:
		first + " or " + self.label_dict[labels[1]]
	second = "Maybe you find the following news from this topic interesting..."
	res[0]=first
	res[1]=second
	
	# For all the index in recommended, extract the news title and storing it in a dictionary
	for e in range(0,len(recommended)):		    
		third = "TITLE "+ str(int(e+1)) + ": " + tn.final_list_title[recommended[e]]
		res[e+2]=third

	#returning dictionary
	return res


    def jaccard_dist(self, list1, list2):
        """
        Computes the Jaccard distance between two lists (lists are converted into sets first)

        list1 (list): first list
        list2 (list): second list
        returns Jaccard distance (float)
        """
        # Convert lists to sets
        set1 = set(list1)
        set2 = set(list2)

        # Compute intersect of sets
        intersect = float(len(set1.intersection(set2)))

        # Calculate similarity, i.e. intersect devided by union, convert to distance, then return.
        return 1.0 - intersect / (len(set1) + len(set2) - intersect)



def main(user):
    """
    Main function
    """
    # Make predictor class, fetch news, predict_class
    MyPredictor = Predictor(model_pickle = "log_regression_model.pkl", tfidf_pickle = "tfidf_vectorizer.pkl")

    # Fetch the news with parameter passed to main
    news = MyPredictor.fetch_news(user)

    # Predict the label/category for the user
    labels = MyPredictor.predict_class(news = news, number_of_classes = 1)

    # Recommend an article
    result = MyPredictor.recommend_article(news = news, labels = labels)
    #return the recommended news as dictionary
    return result


