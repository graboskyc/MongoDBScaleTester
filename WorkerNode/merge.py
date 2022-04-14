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
from faker import Faker
import pickle
from datetime import datetime, timedelta

class Mongouser(User):
    client = pymongo.MongoClient(os.environ['MDBCONNSTRING'])
    handle = client.iot.ts

    howLongBeenRunningLikeThis = datetime.now()
    maxRunTime = 1*60

    f = Faker()

    tic = time.time()

    def wait_time(self):
        timediff = datetime.now() - self.howLongBeenRunningLikeThis 
        if(timediff.total_seconds() > self.maxRunTime):
            self.howLongBeenRunningLikeThis = datetime.now()
            print("changing it up")
            return 0
        else:
            return timediff

    @tag('uc_merge')
    @task(1)
    def uc_merge(self):
        try:
            pipeline = [{"$group": {  "_id": {    "name": '$meta.name',    "time": {  "$dateTrunc": { "date": '$ts',  "unit": 'month'  }  } }, "total": {"$sum": "$qty"}, "ct":{"$sum":1}}}, {"$merge": { "into": 'monthlyRoundup',  "on": "_id"}}]
            print("STARTING Merge")
            # thruput tracking
            self.tic = time.time()

            output = self.handle.aggregate(pipeline, allowDiskUse=True)

            # thruput tracking
            self.environment.events.request_success.fire(request_type="pymongo", name="uc_merge", response_time=(time.time()-self.tic), response_length=0)
            print("ENDING Merge after " + str(time.time()-self.tic))
        except KeyboardInterrupt:
            print
            sys.exit(0)
        except Exception as e:
            print(f'{datetime.now()} - DB-CONNECTION-PROBLEM: ' f'{str(e)}')
            self.environment.events.request_failure.fire(request_type="pymongo", name="uc_merge", response_time=(time.time()-self.tic), response_length=0)
            connect_problem = True
