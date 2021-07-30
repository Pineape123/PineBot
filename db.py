import pymongo
import dotenv
import os 
from dotenv import load_dotenv

load_dotenv()

# userdb = mongo["UserData"]
# usercol = userdb["Data"]
# def cool():
# 	usercol.insert({
# 		"hello" : "bob"
# 	})

class Database(object):
	MONGO_URI = os.getenv("MONGO_CON")
	DB = None

	@staticmethod
	def init():
		client = pymongo.MongoClient(Database.MONGO_URI)
		Database.DB = client['UserData']
		print("DATABASE INITIALIZED")

	@staticmethod
	def insert(collection, data):
		return Database.DB[collection].insert_one(data)

	@staticmethod
	def find(collection, query):
		return Database.DB[collection].find_one(query)

	@staticmethod
	def update(collection, query, data):
		return Database.DB[collection].update_one(query, data)

	@staticmethod
	def delete(collection, query):
		return Database.DB[collection].delete_one(query)
