import psutil
import platform
import argparse
import GPUtil
import os
import pymongo
from datetime import datetime

from statistics import mean
TITLE = "hostname,timestamp,cpu,ram,gpu-load,gpu-ram\n"


def current_time():
    now = datetime.now()
    return now.strftime("%Y-%m-%d %H:%M:%S"), now.strftime("%Y-%m")


# def write_record(instance_name, record):
try:
    conn = pymongo.MongoClient("mongodb://monitoring:monitoring@127.0.0.1:10017/monitoring?authSource=monitoring&retryWrites=true&w=majority")
    print(conn)
except ConnectionError as e:
    print("could not connect to MongoDB")
    print(e)
    
    
parser = argparse.ArgumentParser()
parser.add_argument("instance_name", help="The unique name of the instance. They way we define it.")
args = parser.parse_args()
print(args)

instance_name = args.instance_name
gpus = GPUtil.getGPUs()
record = {
    "hostname": args.instance_name,
    "cpu": psutil.cpu_percent(),
    "ram": psutil.virtual_memory().percent,
    "gpu-load": mean([gpu.load * 100 for gpu in gpus]),
    "gpu-ram": mean([gpu.memoryUsed / gpu.memoryTotal * 100 for gpu in gpus]),
}

db = conn["monitoring"]
print(f"DB is: {db}")
collection = db["records"]
print(f"Collection is: {collection}")

document_id = collection.insert_one(record)
print("Document inserted with id: ", document_id.inserted_id)

conn.close()