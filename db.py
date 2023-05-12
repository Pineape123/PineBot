import copy, os
import motor.motor_asyncio as motor
from dotenv import load_dotenv

load_dotenv()


class VERSION1(object):
    BASE_STRUCTURE = {
        "GUILD_ID": 0,
        "DATA_VERSION": 2,
        "custom_prefix": None,
        "word_blacklist": [],
    }

    @staticmethod
    def create(guild_id):
        new_data = copy.deepcopy(VERSION1.BASE_STRUCTURE)
        new_data["GUILD_ID"] = guild_id
        return new_data

    @staticmethod
    def upgrade(version0_data):
        print("CANNOT UPGRADE FROM BASE VERSION.")
        return version0_data


class VERSION2(object):
    BASE_STRUCTURE = {
        "GUILD_ID": 0,
        "DATA_VERSION": 2,
        "custom_prefix": None,
        "word_blacklist": [],
        "warns": {},
        "coins": {},
    }

    @staticmethod
    def create(guild_id):
        new_data = copy.deepcopy(VERSION2.BASE_STRUCTURE)
        new_data["GUILD_ID"] = guild_id
        return new_data

    @staticmethod
    def upgrade(version1_data):
        version2_data = version1_data
        version2_data["DATA_VERSION"] = 2
        version2_data["warn_list"] = []
        version2_data["coins"] = {}
        return version2_data


LATEST_DATA_VERSION = 2
DATABASE_VERSIONS = {1: VERSION1, 2: VERSION2}


class Database(object):
    URI = os.getenv("MONGODB_URI")
    DB_NAME = os.getenv("MONGODB_DB")

    DB = None
    GUILDS_COLLECTION = "guilds"

    @staticmethod
    def init():
        client = motor.AsyncIOMotorClient(Database.URI)
        Database.DB = client[Database.DB_NAME]

    @staticmethod
    async def get_collections():
        return await Database.DB.list_collection_names()

    @staticmethod
    async def insert_one(collection: str, data: dict = {}):
        return await Database.DB[collection].insert_one(data)

    @staticmethod
    async def find(collection: str, query: dict = {}):
        return await Database.DB[collection].find(query)

    @staticmethod
    async def find_one(collection: str, query: dict = {}):
        return await Database.DB[collection].find_one(query)

    @staticmethod
    async def replace_one(
        collection: str, query: dict = {}, data: dict = {}, upsert: bool = False
    ):
        return await Database.DB[collection].replace_one(query, data, upsert=upsert)

    @staticmethod
    async def delete_one(collection: str, query: dict = {}):
        return await Database.DB[collection].delete_one(query)

    @staticmethod
    async def get_guild(guild_id: int):
        guild_data = await Database.find_one(
            Database.GUILDS_COLLECTION, {"GUILD_ID": guild_id}
        )

        if guild_data is None:
            guild_data = DATABASE_VERSIONS[LATEST_DATA_VERSION].create(guild_id)
        else:
            guild_data_version = guild_data["DATA_VERSION"]

            while guild_data_version < LATEST_DATA_VERSION:
                guild_data = DATABASE_VERSIONS[guild_data_version + 1].upgrade(
                    guild_data
                )
                guild_data_version = guild_data["DATA_VERSION"]
            await Database.set_guild(guild_id, guild_data)

        return guild_data

    @staticmethod
    async def set_guild(guild_id: int, new_guild_data: dict):
        return await Database.replace_one(
            Database.GUILDS_COLLECTION, {"GUILD_ID": guild_id}, new_guild_data, True
        )
