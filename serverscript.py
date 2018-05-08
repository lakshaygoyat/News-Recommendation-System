#!/usr/bin/python
from flask import Flask,json,Response, render_template
import recommend
import csv
import recommendation_news as rn
app = Flask(__name__)

# Creating a dictionary of news_id and title. This is used to retrieve the title when a list of news_id is returned after applying item-item similarity algorithm
my_dict = {}
with open('news_plus_id.csv') as csvfile:
	reader = csv.DictReader(csvfile)
	for row in reader:
		my_dict[row['item_id']] = row['title']



# app.route() -  Used to define a path in flask
@app.route("/")
def home():
    return render_template('./home.html')

@app.route("/search.html")
def search():
	return render_template('./search.html')

# For any random path, it redirects to home page
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catchall(path):
    return render_template('./home.html')

# Calling Collaborative Filtering Python File
@app.route('/recommendation/<int:uid>', methods=["GET"])
def api_article(uid):

	predictDictData = recommend.getResult(uid) 
	res_dict = {}
	i=0
	# Extracting corresponding title 
	for ap in predictDictData:
		res_dict[i] = [ap,my_dict.get(str(ap))]
		i=i+1
	RESPONSE_JSON_DATA = json.dumps(res_dict)
	RESPONSE = Response(RESPONSE_JSON_DATA, status=200, mimetype='application/json')
	return RESPONSE

# Calling NLP Python File
@app.route('/recommendation_nlp/<int:uid>', methods=["GET"])
def api_article1(uid):

	#importing other python file and calling the main function by passing the user id
	predictDictData = rn.main(uid)
	RESPONSE_JSON_DATA = json.dumps(predictDictData)
	RESPONSE = Response(RESPONSE_JSON_DATA, status=200, mimetype='application/json')
	return RESPONSE


if __name__ == '__main__':
	app.debug = True
	app.run()

