# This file extracts the data for each user. It stores the titles that each user has seen/interacted.
import os
import csv
import itertools
import pandas as pd

# Give the path where the user and news interaction data is stored (Google Analytics Data)
Path = "/home/saksam/test/News_Tab/"
filelist = os.listdir(Path)
final_user_id = []
final_title = []

#Getting newsID corresponding to the userID according to the click
#news from 1st June to 10th JULY
for i in filelist:
	if i.endswith(".csv"):  # You could also add "and i.startswith('f')
		
		f = open(Path + i)
		csv_f = csv.reader(f)
		list_file = []

		#extracting each row of the csv file and storing it in list_file
		for row in csv_f:
			list_file.append(row)
		
		#getting the title and user_id and storing it
		title= []
		user_id = []
		for line in list_file:
			if len(line)==6:
				title.append(line[0])
				user_id.append(line[1])
		
		del user_id[0]
		del user_id[-1]
		del title[0]
		del title[-1]
		final_user_id.append(user_id)
		final_title.append(title)
		

l1 = (list(itertools.chain.from_iterable(final_user_id))) # combining all lists of 'user_id' into one single list
l2 = (list(itertools.chain.from_iterable(final_title)))   # combining all lists of 'title' into one single list

#Storing all the data in a dictionary. The values of dictionary is in list format
from collections import defaultdict
user_data = defaultdict(list)

for item1,item2 in zip(l1,l2):
	user_data[item1].append(item2)

'''
with open('user_news_data.csv', 'wb') as csv_file:
    writer = csv.writer(csv_file)
    for key, value in user_data.items():
	for ele in value:
		writer.writerow([key, ele])
'''
