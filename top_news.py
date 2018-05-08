# This file works on getting the news of past 3-4 days
import os
import csv
import itertools
import pandas as pd

# Give the path where your past 3-4 days news is stored
Path = "/home/saksam/test/News_Tab/testing_data/"
filelist = os.listdir(Path)
final_user_id = []
final_title = []

for i in filelist:
	if i.endswith(".csv"):  # You could also add "and i.startswith('f')

		f = open(Path + i)
		csv_f = csv.reader(f)
		list_file = []

		#extracting each row of the csv file and storing it in list_file
		for row in csv_f:
			list_file.append(row)


		#getting the title and storing it
		title= []
		for line in list_file:
			if len(line)==5:
				title.append(line[0])

		
		del title[0]
		del title[0]
		del title[-1]
		final_title.append(title)
		

final_list_title = (list(itertools.chain.from_iterable(final_title))) #title

