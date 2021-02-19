from flask_pymongo import pymongo

user = "admin"
password = "yXNcszPcZExEiJMs"

CONNECTION_STRING = "mongodb+srv://"+user+":"+password+"@cluster0.lbaun.mongodb.net/admin?retryWrites=true&w=majority"
client = pymongo.MongoClient(CONNECTION_STRING)
db = client.get_database('flask_project')
user_collection = pymongo.collection.Collection(db, 'user_collection')
scraping_collection = pymongo.collection.Collection(db, 'Scraping_collection')






