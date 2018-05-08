# This file stores all the news content and store it in the json format

import os
import csv
import itertools
import pandas as pd
Path = "/home/saksam/test/News_Tab/allnews/"
filelist = os.listdir(Path)

news_id = []
title = []
description = []
category = []

for i in filelist:
	if i.endswith("news.csv"):  # You could also add "and i.startswith('f')
		
		f = open(Path + i)
		csv_f = csv.reader(f)
		
		allwords = []
		#extracting each row of the csv file and storing it in list_file
		for row in csv_f:
			news_id.append(row[0])
			title.append(row[2])
			description.append(row[3])
			category.append(row[7])

final_cat = []
label = []

#correcting the category and giving label		
for ele in category:
	if 'India' in ele or 'india' in ele:
		final_cat.append('India')
		label.append(0)
	elif 'Sports' in ele:
		final_cat.append('Sports')
		label.append(1)
	elif 'Lifestyle' in ele:
		final_cat.append('Lifestyle')
		label.append(2)
	elif 'Entertainment' in ele:
		final_cat.append('Entertainment')
		label.append(3)
	elif 'Technology' in ele:
		final_cat.append('Technology')
		label.append(4)
	elif 'Business' in ele:
		final_cat.append('Business')
		label.append(5)
	elif 'World' in ele:
		final_cat.append('World')
		label.append(6)

allwords = []

#combining title and description
for x,y in zip(title, description):
	allwords.append(x+y)

final = []
for a,b,c,d in zip(news_id,allwords,final_cat,label):
	l = [a,b,c,d]
	final.append(l)


col = ['News_id','Allwords','Category','Label']
df = pd.DataFrame.from_records(final, columns=col)

out= df.to_json(orient='records')

with open('meri_news.json','w') as f:
	f.write(out)
