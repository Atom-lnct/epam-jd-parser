import os
import certifi
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
MONGO_DB = os.getenv("MONGO_DB", "jd_parser")

client = MongoClient(
    MONGO_URI,
    
    tls = True,
    tlsCAFile = certifi.where(), #TLS certificate
    serverSelectionTimeoutMS=15000, # if cluster is pause
     connectTimeoutMS=10000,
    socketTimeoutMS=10000, # bad internet connection  => fail
     retryWrites=True, # retry again
     w="majority",
)

db = client[MONGO_DB]
jd_collection = db["parsed_jds"]