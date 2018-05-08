
import pandas as pd
import graphlab
import csv


my_dict = {}
def getResult(uid):

	# pass in column names for each CSV and read them using pandas. 

	#Reading news file:
	r_cols = ['user_id', 'item_id']
	data = pd.read_csv('/home/saksam/test/user_news', sep='\t', names=r_cols,header=None,index_col=None,usecols=[0, 1],encoding='latin-1')
	
	# Conerting the data into SFrame
	rate_sframe= graphlab.SFrame(data)

	rsf = graphlab.SFrame(rate_sframe)
	
	#Applying item-item similarity to all the news and user_id
	m = graphlab.item_similarity_recommender.create(rsf)
	recs = m.recommend()

	#Getting recommendations for a specific user id
	p = recs.filter_by(uid,'user_id')

	#Storing the user_id to list
	res = list(p['item_id'])

	return res


