import time
import datetime
from locust import User, task, constant, tag
import pymongo
from time import perf_counter
import bson
from bson import json_util
from bson.json_util import loads
from bson import ObjectId
import os
import string
import random
import pickle

class Mongouser(User):
    client = pymongo.MongoClient(os.environ['MDBCONNSTRING'])
    db = client.loadtest

    @tag('uc_write')
    @task(1)
    def insert_one(self):
        print('upsert one')
        try:
            tic = time.time()
            # 11kb ascii block random worst case scenario for compression
            noise = ''.join(random.choices(string.ascii_uppercase + string.digits + string.ascii_lowercase, k = 1024*11))
            # 16^7 = 268,435,456 possible _id values
            id = ''.join(random.choices(os.environ['KEYSPACE'] , k = int(os.environ['KEYCOUNT']) )) 

            obj = {"value": bson.Binary(pickle.dumps(noise)), "created": datetime.datetime.now(), "location":os.environ['ISOLOC']   }

            output = self.db.queue.update_one({"_id":id}, {"$set": obj}, upsert=True)
            self.environment.events.request_success.fire(request_type="pymongo", name="uc_write", response_time=(time.time()-tic), response_length=0)

        except KeyboardInterrupt:
            print
            sys.exit(0)
        except Exception as e:
            print(f'{datetime.datetime.now()} - DB-CONNECTION-PROBLEM: '
                f'{str(e)}')
            connect_problem = True