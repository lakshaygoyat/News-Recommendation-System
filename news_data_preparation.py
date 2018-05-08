#!/usr/bin/env python
# coding:utf-8

"""
Script for cleaning and preparing the DON news data

"""

# Imports
import glob
import json
import pandas as pd
import numpy as np
import os


class DataPolisher(object):
    """
    Class that holds functions to clean and prepare the news
    """

    def __init__(self):
        # Dataframe to keep the data
        self.data = pd.DataFrame()


    def loaddata(self):
        """
        Loads the data

        folder (string): folder in which to look for the datafiles
        returns nothing
        """
        df = pd.read_json('/home/saksam/test/meri_news.json')
        self.data = df
	

    def cleandata(self):
        """
        Cleans the data

        returns nothing
        """
	# The "data" is a DataFrame and it has "Allwords" column which has the news content. Include as much of the content as possible.
        
        # Make length feature
        self.data["length"] = self.data["Allwords"].apply(lambda x: len(x.split()))

        # Reset index and drop added column
        self.data = self.data.reset_index()
        self.data.drop('index', axis=1, inplace=True)

        # Shuffle the dataframe, reset index and clean
        self.data = self.data.reindex(np.random.permutation(self.data.index))
        self.data = self.data.reset_index()
        self.data.drop('index', axis=1, inplace=True)


    def writedata(self, filename):
        """
        Writes the data to pickle

        filename (string): filename for pickled datafile
        returns nothing
        """

        # Make folder for saving the data if it does not already exist
        if not os.path.isdir('/home/saksam/test/' + "data"):
            cmd = "mkdir {}data".format('/home/saksam/test/')
            os.system(cmd)

        self.data.to_pickle('/home/saksam/test/' + "data/" + filename)



def main():
    """
    Main function
    """
    # Make class, then load, clean and write data
    MyDataPolisher = DataPolisher()
    MyDataPolisher.loaddata()
    MyDataPolisher.cleandata()
    MyDataPolisher.writedata(filename = "clean_nyt_training_data.pkl")



if __name__ == '__main__':
    main()
