import copy, os, pymongo
from dotenv import load_dotenv

load_dotenv()


class VERSION1(object):
	BASE_STRUCTURE = {
		"GUILD_ID": 0,
		"DATA_VERSION": 1,
		"custom_prefix": None,
		"word_blacklist": []
		}

	@staticmethod
	def create(guild_id):
		new_data = copy.deepcopy(VERSION1.BASE_STRUCTURE)
		new_data["GUILD_ID"] = guild_id
		return new_data
	
	@staticmethod
	def upgrade(database, version0_data):
		print("CANNOT UPGRADE FROM BASE VERSION.")
		return version0_data

DATABASE_VERSIONS = {
	1:VERSION1
}

class Database(object):
	URI = os.getenv("MONGODB_URI")
	DB_NAME = os.getenv("MONGODB_DB")
	print(URI)
	print(DB_NAME)

	DB = None
	GUILDS_COLLECTION = "servers"
	LATEST_DATA_VERSION = 1

	@staticmethod
	def init():
		client = pymongo.MongoClient(Database.URI)
		Database.DB = client[Database.DB_NAME]

	@staticmethod
	def get_collections():
		return Database.DB.list_collection_names()

	@staticmethod
	def insert_one(collection:str, data:dict = {}):
		return Database.DB[collection].insert_one(data)

	@staticmethod
	def find(collection:str, query:dict = {}):
		return Database.DB[collection].find(query) 

	@staticmethod
	def find_one(collection:str, query:dict = {}):
		return Database.DB[collection].find_one(query)

	@staticmethod
	def replace_one(collection:str, query:dict = {}, data:dict = {}, upsert:bool = False):
		return Database.DB[collection].replace_one(query, data, upsert=upsert)

	@staticmethod
	def delete_one(collection:str, query:dict = {}):
		return Database.DB[collection].delete_one(query)

	@staticmethod
	def get_guild(guild_id: int):
		guild_data = Database.find_one(Database.GUILDS_COLLECTION, {"GUILD_ID":guild_id})

		if guild_data is None:
			guild_data = DATABASE_VERSIONS[Database.LATEST_DATA_VERSION].create(guild_id)
		else:
			guild_data_version = guild_data["DATA_VERSION"]

			while guild_data_version < Database.LATEST_DATA_VERSION:
				guild_data = DATABASE_VERSIONS[guild_data_version + 1].upgrade(Database, guild_data)
				guild_data_version = guild_data["DATA_VERSION"]

		return guild_data

	@staticmethod
	def set_guild(guild_id: int, new_guild_data: dict):
		return Database.replace_one(Database.GUILDS_COLLECTION, {"GUILD_ID":guild_id}, new_guild_data, True)
