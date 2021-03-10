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
from faker import Faker

class Mongouser(User):
    client = pymongo.MongoClient(os.environ['MDBCONNSTRING'])
    db = client.Lab
    f = Faker()
    choices = ["Clicked","Called","Other","Something"]

    @tag('uc_insertmany_Lookup')
    @task(0)
    def uc_insertmany_Lookup(self):
        print('lookup')
        try:
            tic = time.time()
            docs = []
            for i in range(50):
                noise = ''.join(random.choices(string.ascii_uppercase + string.digits + string.ascii_lowercase, k = int(1024*int(os.environ['KBPADDING'])/4)))
                docs.append({
                    "Answer":self.f.text(),
                    "QuestionId":''.join(random.choices(os.environ['KEYSPACE'] , k = 5 )),
                    "created": datetime.datetime.now(),
                    "noise": bson.Binary(pickle.dumps(noise)),
                    "QuestionType":"Yes/No",
                    "TopicName":''.join(random.choices(os.environ['KEYSPACE'] , k = 5 ))
                })
            
            output = self.db.SurveyResponse.insert_many(docs)
            self.environment.events.request_success.fire(request_type="uc_insertmany_Lookup", name="uc_insertmany_Lookup", response_time=(time.time()-tic), response_length=0)
        except KeyboardInterrupt:
            print
            sys.exit(0)
        except Exception as e:
            print(f'{datetime.datetime.now()} - DB-CONNECTION-PROBLEM: '
                f'{str(e)}')
            connect_problem = True
    
    @tag('uc_insertmany_Contact')
    @task(2)
    def uc_insertmany_Contact(self):
        print('contact')
        try:
            tic = time.time()
            docs = []
            for i in range(25):
                # 11kb ascii block random worst case scenario for compression
                noise = ''.join(random.choices(string.ascii_uppercase + string.digits + string.ascii_lowercase, k = 1024*int(os.environ['KBPADDING'])))
                consents = []
                for j in range(random.randint(5,25)):
                    consents.append({
                        "TopicName":''.join(random.choices(os.environ['KEYSPACE'] , k = 5 )),
                        "ConsentSetting":self.f.boolean()
                    })
                survey = []
                for j in range(random.randint(5,25)):
                    survey.append({
                        "QuestionId":''.join(random.choices(os.environ['KEYSPACE'] , k = 5 )),
                        "Answer":self.f.text(),
                        "ResponseEventCode":random.choice(self.choices),
                    })
                docs.append({
                    "name": self.f.name(),
                    "address": self.f.address(),
                    "background":self.f.text(),
                    "age":random.randint(18,75),
                    "ContactKey":''.join(random.choices(os.environ['KEYSPACE'] , k = int(os.environ['KEYCOUNT']) )),
                    "Consents":consents,
                    "SurveyResponses":survey,
                    "noise": bson.Binary(pickle.dumps(noise)),
                    "created": datetime.datetime.now(), 
                    "location":os.environ['ISOLOC']
                })
            
            output = self.db.Contact.insert_many(docs)
            self.environment.events.request_success.fire(request_type="uc_insertmany_Contact", name="uc_insertmany_Contact", response_time=(time.time()-tic), response_length=0)


        except KeyboardInterrupt:
            print
            sys.exit(0)
        except Exception as e:
            print(f'{datetime.datetime.now()} - DB-CONNECTION-PROBLEM: '
                f'{str(e)}')
            connect_problem = True