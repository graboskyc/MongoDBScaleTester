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

    ranWords = ["aspiring","different","ground","porter","selective","spiders","moldy","structure","crate","decorate","ear","steady","self","nervous","exercise","cherry","notice","empty","title","parcel","blind","cannon","willing","cheese","exotic","spell","talented","land","incompetent","woman","cautious","bat","far","nifty","tight","madly","coach","sort","confuse","youthful","yielding","interesting","delirious","car","nappy","gaping","basketball","hard","animated","hapless","actor","ski","quizzical","reduce","parallel","wet","excite","penitent","servant","jewel","mend","black","hydrant","badge","educated","dust","homely","allow","deadpan","pretend","faulty","growth","verdant","periodic","permit","chivalrous","toothbrush","idea","shop","defective","rejoice","theory","ludicrous","precede","arithmetic","daily","zoo","quartz","toothsome","scare","bottle","calendar","gruesome","flash","belong","quarrelsome","violent","cheer","fumbling","button","bulb","hover","brainy","fluttering","fish","shake","detect","inconclusive","tacit","bushes","glorious","unusual","twig","vacation","soap","mountainous","capricious","heartbreaking","development","abundant","laborer","rabid","hang","drag","obtain","vigorous","buzz","chickens","material","annoy","float","inject","education","disgusting","pickle","muddled","drown","sparkle","next","cut","animal","food","condemned","meal","changeable","charge","dapper","conscious","strange","holistic","cruel","visitor","curtain","ignorant","surround","earsplitting","worthless","mind","reply","one","can","snail","mouth","grape","page","windy","playground","incredible","venomous","null","scrape","telephone","furry","mundane","battle","shelf","rod","possessive","rough","liquid","burly","thing","lewd","hysterical","wide","grin","locket","witty","fly","better","attract","attend","taste","concentrate","rake","strip","irate","treat","half","sisters","calm","vest","regret","boundless","love","neck","include","voice","uppity","ship","unsuitable","dreary","observation","doubtful","bear","skate","plain","panoramic","bikes","draconian","scrawny","hall","voracious","dad","nonstop","pedal","kitty","activity","wonder","eyes","lame","star","pollution","engine","butter","defiant","normal","back","flagrant","colour","impolite","license","concern","rabbit","trousers","upbeat","wind","knee","blush","first","roll","clap","deep","twist","suit","wound","guarantee","peaceful","jump","tour","thumb","puny","cumbersome","damaging","quickest","barbarous","control","yell","zipper","snakes","shape","mask","appreciate","answer","fresh","scarf","distribution","bright","degree","toes","seat","narrow","camera","calculating","society","sordid","embarrassed","insect","club","evasive","noxious","energetic","babies","disastrous","fold","expand","obsequious","ad hoc","kiss","efficient","blood","poor","change","ambiguous","gainful","enormous","charming","potato","aloof","waves","wail","wanting","squeal","remain","stupendous","seal","birth","tasty","camp","curvy","wipe","faint","pack","meek","x-ray","hunt","boy","downtown","honey","remember","romantic","longing","cause","prefer","jelly","white","eatable","aberrant","pipe","smart","experience","addicted","dizzy","voyage","multiply","chase","grotesque","flag","warlike","plastic","sneeze","warm","letter","private","sophisticated","exist","bells","dangerous","sad","squeamish","lamentable","recess","puzzled","frequent","delay","lighten","grieving","side","ill-informed","wrong","glistening","important","girls","enter","childlike","creepy","breakable","staking","radiate","chunky","thaw","day","rice","amusement","rings","dogs","obese","afraid","encouraging","fast","rain","educate","stroke","guess","friendly","lumpy","carriage","pocket","war","shave","apathetic","elated","languid","town","gaudy","cobweb","therapeutic","unequal","caption","mammoth","rustic","call","want","tug","shelter","consist","sincere","oven","tested","save","pigs","obnoxious","mother","front","vengeful","unused","oafish","eight","abrasive","excellent","scared","determined","straw","magic","perpetual","retire","helpful","cry","coal","mitten","powder","icy","spoil","dock","bizarre","flow","pointless","deranged","ossified","dress","cactus","abashed","frightened","handle","present","knowing","vague","adamant","fence","guitar","gratis","ajar","tick","fallacious","flat","rifle","trucks","rhetorical","appear","furniture","print","women","punishment","rude","sugar","share","steadfast","robust","endurable","internal","trees","corn","observant","overflow","screw","admire","clumsy","skip","flood","slave","flavor","fortunate","lavish","lip","promise","grubby","cure","clear","milk","forgetful","abstracted"]
    keySpace = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "a","b","c","d","e" ] # 15
    keySize = 5                                                                   # 15 ^ 5 = 759,375

    minDate = datetime.strptime("2022-01-01", "%Y-%m-%d")
    maxRunTime = 1*60                                                            # 15 mins change it up 
    minHour = 9
    maxHour = 17

    howLongBeenRunningLikeThis = datetime.now()
    currentHour = minHour
    currentMin = 0
    currentDay = 0
    currentDateBase = minDate + timedelta(hours=9)

    f = Faker()

    tic = time.time()

    @tag('uc_write')
    @task(100)
    def insert_one(self):
        try:
            timediff = datetime.now() - self.howLongBeenRunningLikeThis 
            if(timediff.total_seconds() > self.maxRunTime):
                self.howLongBeenRunningLikeThis = datetime.now()
                self.currentHour = self.currentHour + 1
                if(self.currentHour > self.maxHour):
                    self.currentHour = self.minHour
                    self.currentDay = self.currentDay + 1
                
                self.currentDateBase = self.minDate + timedelta(hours=self.currentHour) + timedelta(days=self.currentDay)
                print("changing it up to " + str(self.currentDateBase))

            # thruput tracking
            self.tic = time.time()

            stampToEnter = self.currentDateBase + timedelta(minutes=datetime.now().minute) + timedelta(seconds=datetime.now().second) + timedelta(microseconds=datetime.now().microsecond)
            user = ''.join(self.f.random_choices(elements=self.keySpace , length=self.keySize))

            doc = {}

            doc["ts"] = stampToEnter

            doc["qty"] = random.randint(15,1015)

            doc["meta"] = {}
            doc["meta"]["name"] = user
            doc["meta"]["content"] = "soda"
            doc["meta"]["location"] = "NY"

            output = self.handle.insert_one(doc)

            # thruput tracking
            self.environment.events.request_success.fire(request_type="pymongo", name="uc_write", response_time=(time.time()-self.tic), response_length=0)

        except KeyboardInterrupt:
            print
            sys.exit(0)
        except Exception as e:
            print(f'{datetime.now()} - DB-CONNECTION-PROBLEM: ' f'{str(e)}')
            self.environment.events.request_failure.fire(request_type="pymongo", name="uc_write", response_time=(time.time()-self.tic), response_length=0)
            connect_problem = True

    @tag('uc_window')
    @task(5)
    def uc_agg(self):
        try:
            user = ''.join(self.f.random_choices(elements=self.keySpace , length=self.keySize))

            # thruput tracking
            self.tic = time.time()

            pipeline = [{ "$match": { 'meta.name': user } }, { "$group": { "_id": { "name": '$meta.name', "time": { "$dateTrunc": { "date": '$ts', "unit": 'minute', "binSize": 60 } } }, "high": { "$max": '$qty' }, "low": { "$min": '$qty' }, "open": { "$first": '$qty' }, "close": { "$last": '$qty' } } }, { "$setWindowFields": { "partitionBy": '$_id.name', "sortBy": { '_id.time': 1 }, "output": { "avgWindow": {"$avg": '$close', "window": { "documents": [ -100, 0] } } } } }]

            output = self.handle.aggregate(pipeline)

            # thruput tracking
            self.environment.events.request_success.fire(request_type="pymongo", name="uc_window", response_time=(time.time()-self.tic), response_length=0)

        except KeyboardInterrupt:
            print
            sys.exit(0)
        except Exception as e:
            print(f'{datetime.now()} - DB-CONNECTION-PROBLEM: ' f'{str(e)}')
            self.environment.events.request_failure.fire(request_type="pymongo", name="uc_window", response_time=(time.time()-self.tic), response_length=0)
            connect_problem = True