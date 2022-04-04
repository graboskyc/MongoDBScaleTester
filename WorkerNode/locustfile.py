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
import uuid
from base64 import b64encode
from random import randint

class Mongouser(User):
    client = pymongo.MongoClient(os.environ['MDBCONNSTRING'])
    f = Faker()

    ranWords = ["aspiring","different","ground","porter","selective","spiders","moldy","structure","crate","decorate","ear","steady","self","nervous","exercise","cherry","notice","empty","title","parcel","blind","cannon","willing","cheese","exotic","spell","talented","land","incompetent","woman","cautious","bat","far","nifty","tight","madly","coach","sort","confuse","youthful","yielding","interesting","delirious","car","nappy","gaping","basketball","hard","animated","hapless","actor","ski","quizzical","reduce","parallel","wet","excite","penitent","servant","jewel","mend","black","hydrant","badge","educated","dust","homely","allow","deadpan","pretend","faulty","growth","verdant","periodic","permit","chivalrous","toothbrush","idea","shop","defective","rejoice","theory","ludicrous","precede","arithmetic","daily","zoo","quartz","toothsome","scare","bottle","calendar","gruesome","flash","belong","quarrelsome","violent","cheer","fumbling","button","bulb","hover","brainy","fluttering","fish","shake","detect","inconclusive","tacit","bushes","glorious","unusual","twig","vacation","soap","mountainous","capricious","heartbreaking","development","abundant","laborer","rabid","hang","drag","obtain","vigorous","buzz","chickens","material","annoy","float","inject","education","disgusting","pickle","muddled","drown","sparkle","next","cut","animal","food","condemned","meal","changeable","charge","dapper","conscious","strange","holistic","cruel","visitor","curtain","ignorant","surround","earsplitting","worthless","mind","reply","one","can","snail","mouth","grape","page","windy","playground","incredible","venomous","null","scrape","telephone","furry","mundane","battle","shelf","rod","possessive","rough","liquid","burly","thing","lewd","hysterical","wide","grin","locket","witty","fly","better","attract","attend","taste","concentrate","rake","strip","irate","treat","half","sisters","calm","vest","regret","boundless","love","neck","include","voice","uppity","ship","unsuitable","dreary","observation","doubtful","bear","skate","plain","panoramic","bikes","draconian","scrawny","hall","voracious","dad","nonstop","pedal","kitty","activity","wonder","eyes","lame","star","pollution","engine","butter","defiant","normal","back","flagrant","colour","impolite","license","concern","rabbit","trousers","upbeat","wind","knee","blush","first","roll","clap","deep","twist","suit","wound","guarantee","peaceful","jump","tour","thumb","puny","cumbersome","damaging","quickest","barbarous","control","yell","zipper","snakes","shape","mask","appreciate","answer","fresh","scarf","distribution","bright","degree","toes","seat","narrow","camera","calculating","society","sordid","embarrassed","insect","club","evasive","noxious","energetic","babies","disastrous","fold","expand","obsequious","ad hoc","kiss","efficient","blood","poor","change","ambiguous","gainful","enormous","charming","potato","aloof","waves","wail","wanting","squeal","remain","stupendous","seal","birth","tasty","camp","curvy","wipe","faint","pack","meek","x-ray","hunt","boy","downtown","honey","remember","romantic","longing","cause","prefer","jelly","white","eatable","aberrant","pipe","smart","experience","addicted","dizzy","voyage","multiply","chase","grotesque","flag","warlike","plastic","sneeze","warm","letter","private","sophisticated","exist","bells","dangerous","sad","squeamish","lamentable","recess","puzzled","frequent","delay","lighten","grieving","side","ill-informed","wrong","glistening","important","girls","enter","childlike","creepy","breakable","staking","radiate","chunky","thaw","day","rice","amusement","rings","dogs","obese","afraid","encouraging","fast","rain","educate","stroke","guess","friendly","lumpy","carriage","pocket","war","shave","apathetic","elated","languid","town","gaudy","cobweb","therapeutic","unequal","caption","mammoth","rustic","call","want","tug","shelter","consist","sincere","oven","tested","save","pigs","obnoxious","mother","front","vengeful","unused","oafish","eight","abrasive","excellent","scared","determined","straw","magic","perpetual","retire","helpful","cry","coal","mitten","powder","icy","spoil","dock","bizarre","flow","pointless","deranged","ossified","dress","cactus","abashed","frightened","handle","present","knowing","vague","adamant","fence","guitar","gratis","ajar","tick","fallacious","flat","rifle","trucks","rhetorical","appear","furniture","print","women","punishment","rude","sugar","share","steadfast","robust","endurable","internal","trees","corn","observant","overflow","screw","admire","clumsy","skip","flood","slave","flavor","fortunate","lavish","lip","promise","grubby","cure","clear","milk","forgetful","abstracted"]
    actions = ["update","set"]
    state = ["update","pending"]
    keySpace = ["a","b","c","d","e","f","g","h","k","m"]
    clientIds = ranWords[:5]
    fieldIds = random.choices(ranWords, k=50)
    keySize = 6
    minDate = datetime.datetime.strptime("2021-01-01", "%Y-%m-%d")
    maxDate = datetime.datetime.strptime("2021-01-31", "%Y-%m-%d")

    @tag('uc_table_1')
    @task(7)
    def table1(self):
        print('Table 1')
        try:
            # thruput tracking
            tic = time.time()

            doc = {}
            doc["accountclientid"] = random.choice(self.clientIds)+"ClientAppV2"
            doc["action"] = random.choice(self.actions)
            doc["authorization"] = ""
            doc["callbackurl"] = ""
            doc["capabilityid"] = ""
            doc["createdon"] = datetime.datetime.combine(self.f.date_between(self.minDate, self.maxDate), datetime.datetime.min.time())
            doc["description"] = ""
            doc["deviceid"] = str(uuid.uuid4())
            doc["errmsg"] = ""
            doc["fieldid"] = random.choice(self.fieldIds)
            doc["fieldvalue"] = b64encode(self.f.sentence().encode("ascii"))
            doc["foreignid"] = str(uuid.uuid4())
            doc["id"] = str(uuid.uuid4())
            doc["kind"] = "ts.event."+doc["fieldid"]
            doc["lastupdated"] = doc["createdon"]
            doc["modelid"] = ""
            doc["name"] = ""
            doc["state"] = random.choice(self.state)
            
            doc["tags"] = []
            i = 0
            while i < randint(1, 4):
                doc["tags"].append(str(uuid.uuid4()))
                i = i + 1

            doc["timebucket"] = doc["createdon"].strftime("%Y-%V")
            doc["transactionid"] = str(uuid.uuid4())
            doc["versionid"] = str(uuid.uuid4())
            doc["version"] = 1.0 

            output = self.client.ts.event_by_device_new.insert_one(doc)

            # thruput tracking
            self.environment.events.request_success.fire(request_type="pymongo", name="uc_table_1", response_time=(time.time()-tic), response_length=0)

        except KeyboardInterrupt:
            print
            sys.exit(0)
        except Exception as e:
            print(f'{datetime.datetime.now()} - DB-CONNECTION-PROBLEM: ' f'{str(e)}')
            self.environment.events.request_failure.fire(request_type="pymongo", name="uc_table_1", response_time=(time.time()-tic), response_length=0)
            connect_problem = True

    @tag('uc_table_2')
    @task(1)
    def table2(self):
        print('Table 2')
        try:
            tic = time.time()
            # 11kb ascii block random worst case scenario for compression
            noise = ''.join(random.choices(string.ascii_uppercase + string.digits + string.ascii_lowercase, k = 1024*11))
            # 16^7 = 268,435,456 possible _id values
            id = ''.join(random.choices(os.environ['KEYSPACE'] , k = int(os.environ['KEYCOUNT']) )) 

            doc = {}
            doc["accountclientid"] = ""

            doc["address"] = "http://haproxy.coho.svc.cluster.local:8082/coho/v2/asyncmessages"
            i = 0
            while i < randint(1, 4):
                doc["address"] = doc["address"] + "/" + random.choice(self.fieldIds)
                i = i + 1

            doc["addressscheme"] = "rest"
            doc["billingaccountid"] = "" 
            doc["clientid"] = ""
            doc["createdon"] = datetime.datetime.combine(self.f.date_between(self.minDate, self.maxDate), datetime.datetime.min.time())
            doc["customratelimit"] = 0
            doc["deliveryscheme"] = ""
            doc["description"] = self.f.sentence()

            doc["fields"] = {}
            doc["fields"]["httpheaders"] = b64encode(self.f.sentence().encode("ascii"))

            doc["foreignid"] = str(uuid.uuid4())
            doc["fromaddress"] = ""
            doc["id"] = str(uuid.uuid4())
            doc["isdeleted"] = False
            doc["key1"] = ""
            doc["kind"] = "ts.target"
            doc["lastupdated"] = doc["createdon"]
            doc["name"] = self.f.sentence()
            doc["premiumsubscription"] = False
            doc["repeatcnt"] = 0
            doc["repeatfrequency"] = ""
            doc["subject"] = ""
            doc["tags"] = []
            doc["template"] = ""
            doc["version"] = 1.0
            doc["version"] = str(uuid.uuid4())

            output = self.client.ts.target_new.insert_one(doc)

            # thruput tracking
            self.environment.events.request_success.fire(request_type="pymongo", name="uc_table_2", response_time=(time.time()-tic), response_length=0)

        except KeyboardInterrupt:
            print
            sys.exit(0)
        except Exception as e:
            print(f'{datetime.datetime.now()} - DB-CONNECTION-PROBLEM: ' f'{str(e)}')
            self.environment.events.request_failure.fire(request_type="pymongo", name="uc_table_2", response_time=(time.time()-tic), response_length=0)
            connect_problem = True

    @tag('uc_table_3')
    @task(2)
    def table3(self):
        print('Table 3')
        try:
            # thruput tracking
            tic = time.time()

            doc = {}
            doc["accountclientid"] = ""
            doc["actions"] = None
            doc["billingaccountid"] = ""
            doc["chipset"] = ""
            doc["createdon"] = datetime.datetime.combine(self.f.date_between(self.minDate, self.maxDate), datetime.datetime.min.time())
            
            doc["customdata"] = {}
            i = 0
            while i < randint(1, 10):
                doc["customdata"][random.choice(self.fieldIds)] = b64encode(self.f.sentence().encode("ascii"))
                i = i + 1

            doc["description"] = self.f.sentence()
            doc["esn"] = "0"
            doc["eventretention"] = 90
            doc["extensionservices"] = []
            doc["foreignid"] = str(uuid.uuid4())
            doc["hw_version"] = ""
            doc["iccid"] = ""
            doc["id"] = str(uuid.uuid4())
            doc["imei"] = "0"
            doc["imsi"] = "0"
            doc["isdeleted"] = False
            doc["kind"] = "ts.device"
            doc["lastupdated"] = doc["createdon"]
            doc["licenses"] = []
            doc["mac"] = self.f.hexify(text='^^:^^:^^:^^:^^:^^')
            doc["manufacturer"] = ""
            doc["meid"] = ""
            doc["msisdn"] = ""
            doc["name"] = "virtual-home"
            doc["productmodel"] = ""
            doc["providerid"] = ""
            doc["qrcode"] = ""
            doc["refid"] = str(uuid.uuid4())
            doc["refidtype"] = "uuid"
            doc["serial"] = ""
            doc["sku"] = ""
            doc["state"] = "activated"
            doc["sw_version"] = ""
            doc["tags"] = []
            doc["version"] = 1.0
            doc["versionid"] = str(uuid.uuid4())

            output = self.client.ts.device.insert_one(doc)

            # thruput tracking
            self.environment.events.request_success.fire(request_type="pymongo", name="uc_table_3", response_time=(time.time()-tic), response_length=0)

        except KeyboardInterrupt:
            print
            sys.exit(0)
        except Exception as e:
            print(f'{datetime.datetime.now()} - DB-CONNECTION-PROBLEM: ' f'{str(e)}')
            self.environment.events.request_failure.fire(request_type="pymongo", name="uc_table_3", response_time=(time.time()-tic), response_length=0)
            connect_problem = True