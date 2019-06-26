#coding : utf-8

import sys

sys.path.insert(0,'/home/ziwo/DB/')
import db

import json
import subprocess
from flask import Flask, jsonify, Response, request
from bson import BSON
from bson import json_util
from flask_cors import CORS
import random

app = Flask(__name__)
CORS(app)

if __name__ == "__main__":
	app.run(debug=True)

def getDB():
	return db.DB().connectDB()


# @app.route('/')
# def first():
# 	database = getDB()
# 	return str(database)


@app.route('/login', methods=['POST', 'GET'])
def login():
	if request.method == 'POST':
		username = request.form['username']
		password = request.form['password']
		database = getDB()
		try:
			collection = database['user']
			if len(list(collection.find({'username':username, 'password':password}))) > 0:
				return json.dumps({"connected":"ok"}, sort_keys=True, default=json_util.default)
			else:
				return json.dumps({"connected":"none"}, sort_keys=True, default=json_util.default)

		except Exception as e:
			return json.dumps({"error":str(e)}, default=json_util.default)

	return json.dumps({"error":"request method != POST"}, default=json_util.default)


@app.route('/launchScript', methods=['GET', 'POST'])
def launchScript():
	if request.method == 'GET':
		try:
			script = subprocess.check_output('python3 /home/ziwo/app/Agents_mp3.py', shell=True)
			return json.dumps({"error":"none"}, default=json_util.default)

		except Exception as e:
			return json.dumps({"error":str(e)}, default=json_util.default)
			
	return json.dumps({"error":"request method != GET"}, default=json_util.default)


@app.route('/delete/<callId>', methods=['GET', 'POST'])
def deleteCall(callId):
	if request.method == 'GET':
		database = getDB()
		try:
			collection = database['call']
			try:
				collection.delete_many({"callID":callId})
			except:
				collection.delete_one({"callID":callId})
			return json.dumps({"error":"none"}, default=json_util.default)

		except Exception as e:
			return json.dumps({"error":str(e)}, default=json_util.default)

	return json.dumps({"error":"request method != GET"}, default=json_util.default)



@app.route('/call/printCall', methods=['GET', 'POST'])
def printCall():
	if request.method == 'GET':
		database = getDB()
		try:
			collection = database['call']
			data = list(collection.find())
			return json.dumps(data, sort_keys=True, default=json_util.default)

		except Exception as e:
			return json.dumps({"error":str(e)}, default=json_util.default)

	return json.dumps({"error":"request method != GET"}, default=json_util.default)


@app.route('/call/insert', methods=['POST', 'GET'])
def insert():
	if request.method == 'POST':
		agentID = request.form['agentID']
		callID = request.form['callID']
		number = request.form['number']
		duration = request.form['duration']
		agent = request.form['agent']
		date = request.form['date']
		database = getDB()
		try:
			collection = database['call']
			find = collection.find({"agent":agent, "number":number, "duration":duration, "callID":callID, "agentID":agentID, "date":date})
			if find.count() == 0:
				collection.insert_one({"agent":agent, "number":number, "duration":duration, "callID":callID, "agentID":agentID, "date":date})
			return json.dumps({"error":"none"}, default=json_util.default)

		except Exception as e:
			return json.dumps({"error":str(e)}, default=json_util.default)

	return json.dumps({"error":"request method != POST"}, default=json_util.default)


@app.route('/call/count/allCall', methods=['POST', 'GET'])
def countCall():
	if request.method == 'GET':
		database = getDB()
		try:
			collection = database['call']
			find = collection.find()
			return json.dumps({"nbCall":len(list(find))}, default=json_util.default)

		except Exception as e:
			return json.dumps({"error":str(e)}, default=json_util.default)

	return json.dumps({"error":"request method != GET"}, default=json_util.default)


@app.route('/call/WadiveutUnCallIDetUnTEXTEtSilPEutYPrenDReUnPEUdeBeaFIlENveUT', methods=['POST', 'GET'])
def wadi():
	if request.method == 'GET':
		database = getDB()
		try:
			collection = database['call']
			find = collection.find()
			agent = dict()
			for elem in find:
				try:
					agent.update({str(elem['callID']) : elem['text']})
				except:
					continue
			return json.dumps({"callText":agent}, default=json_util.default)

		except Exception as e:
			return json.dumps({"error":str(e)}, default=json_util.default)

	return json.dumps({"error":"request method != GET"}, default=json_util.default)


@app.route('/call/countHappy', methods=['POST', 'GET'])
def getHappyCall():
	if request.method == 'GET':
		database = getDB()
		try:
			collection = database['call']
			find = collection.find({'feel':{'$gte':50}})

			return json.dumps({"countHappy":len(list(find))}, default=json_util.default)

		except Exception as e:
			return json.dumps({"error":str(e)}, default=json_util.default)

	return json.dumps({"error":"request method != GET"}, default=json_util.default)


@app.route('/call/countAngry', methods=['POST', 'GET'])
def getAngryCall():
	if request.method == 'GET':
		database = getDB()
		try:
			collection = database['call']
			find = collection.find({'feel':{'$lt':50}})

			return json.dumps({"countAngry":len(list(find))}, default=json_util.default)

		except Exception as e:
			return json.dumps({"error":str(e)}, default=json_util.default)

	return json.dumps({"error":"request method != GET"}, default=json_util.default)


@app.route('/call/<callID>', methods=['POST', 'GET'])
def getDataFromCallID(callID):
	if request.method == 'GET':
		database = getDB()
		try:
			collection = database['call']
			find = collection.find({'callID':callID})

			return list(find)[0]['text']

		except Exception as e:
			return json.dumps({"error":str(e)}, default=json_util.default)

	return json.dumps({"error":"request method != GET"}, default=json_util.default)



@app.route('/update/feel', methods=['POST', 'GET'])
def updateFeel():
	if request.method == 'POST':
		callID = request.form['callID']
		feel = int(round(float(request.form['feel']), 2)*100)
		database = getDB()
		try:
			collection = database['call']
			find = collection.update_one({"callID":callID}, {'$set':{'feel':feel}}, upsert = True)
			return json.dumps({"error":"none"}, default=json_util.default)

		except Exception as e:
			return json.dumps({"error":str(e)}, default=json_util.default)

	return json.dumps({"error":"request method != POST"}, default=json_util.default)


@app.route('/update/tag', methods=['POST', 'GET'])
def updateTag():
	if request.method == 'POST':
		callID = request.form['callID']
		tag = request.form['tag']
		database = getDB()
		try:
			collection = database['call']
			find = collection.update({"callID":callID}, {'$set':{'tag':tag}}, upsert = True)
			return json.dumps({"error":"none"}, default=json_util.default)

		except Exception as e:
			return json.dumps({"error":str(e)}, default=json_util.default)

	return json.dumps({"error":"request method != POST"}, default=json_util.default)


@app.route('/update/text', methods=['POST', 'GET'])
def updateText():
	if request.method == 'POST':
		callID = request.form['callID']
		text = request.form['text']
		database = getDB()
		try:
			collection = database['call']
			find = collection.update({"callID":callID}, {'$set':{'text':text}}, upsert = True)
			return json.dumps({"error":"none"}, default=json_util.default)

		except Exception as e:
			return json.dumps({"error":str(e)}, default=json_util.default)

	return json.dumps({"error":"request method != POST"}, default=json_util.default)



@app.route('/agent/name/call/count', methods=['POST', 'GET'])
def getNameAndNbCallAgent():
	if request.method == 'GET':
		database = getDB()
		try:
			collection = database['call']
			find = list(collection.find())
			agent = dict()
			agentList = list()
			i = 0
			while i != len(find):
				if find[i]['agent'] not in agentList:
					agentList.append(find[i]['agent'])
					tmp = dict()
					j = 0
					k = 0
					while j != len(find):
						if find[j]['agent'] == find[i]['agent']:
							k += 1
						j += 1
					tmp[find[i]['agent']] = k
					agent.update(tmp)
				i += 1

			return json.dumps({"CallPerAgent":agent}, default=json_util.default)

		except Exception as e:
			return json.dumps({"error":str(e)}, default=json_util.default)

	return json.dumps({"error":"request method != GET"}, default=json_util.default)


@app.route('/agent/count/allAgent', methods=['POST', 'GET'])
def count():
	if request.method == 'GET':
		database = getDB()
		try:
			collection = database['call']
			find = collection.find()
			nbAgent = []
			for elem in find:
				if elem['agent'] not in nbAgent:
					nbAgent.append(elem['agent'])
			return json.dumps({"nbAgent":len(nbAgent)}, default=json_util.default)

		except Exception as e:
			return json.dumps({"error":str(e)}, default=json_util.default)

	return json.dumps({"error":"request method != GET"}, default=json_util.default)

# @app.route('/authenticate', methods=['GET'])
# def get_template():
# 	return render_template('form.html', form=form)

# @app.route('/launchScript')
# def launchScript():
