from pymongo import MongoClient

# Database Connection Online
MONGODB_URI = "mongodb://admin:csclassroom1@ds133762.mlab.com:33762/csclassroom"
client = MongoClient(MONGODB_URI, connectTimeoutMS=30000)
db = client.get_database("csclassroom")


# Database Connection Offline
'''
client = MongoClient('localhost', 27017)
db = client.csclassroom
'''