// original source: https://github.com/jayrunkel/gmDataLoad/blob/master/sharding/setUpSharding.js
// thanks, Uncle Runkel

////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
// GLOBAL VARS
////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
var numShards = 8;                            // CHANGE ME: how many shards
var dbName = "loadtest";                      // CHANGE ME: what DB we using
var colNames = ["loadtest.queue"];            // CHANGE ME: array of collections we are working with

var avgDocSizeKb = 11;                        // CHANGE ME: based on your load generator in locustfile.py
var keySpaceSize = 16;                        // CHANGE ME: get this from the key space in worker-variables.env but this will break if not 16
var keyCount = 7;                             // CHANGE ME: get this from the key space in worker-variables.env

////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
// Do the work, do not modify below here
////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
var expectedDocCount = Math.pow(keySpaceSize, keyCount);
var CHUNKSIZEKB = 64*1024;                                                          // don't change this
var chunkSplitInterval = Math.floor(expectedDocCount / numShards);
var pad = "";
for (p=0; p < keyCount; p++) {
    pad = pad + "0";
}

var db = db.getSiblingDB(dbName);
sh.stopBalancer();

db.dropDatabase();
sh.enableSharding(dbName);

print("shard each collection...");
colNames.forEach(collection => {
    print("enabling sharding for collection" + collection)
	sh.shardCollection(collection, {_id : 1}, false);
});

print("starting presplit...");
colNames.forEach(collection => {
    print("starting collection: ", collection);
    var ct =0;

    for(x = 1; x < numShards; x++) {
        var splitPoint_dec = x * chunkSplitInterval;
        var splitPoint_hex = (pad + (splitPoint_dec-1).toString(16)).slice(-pad.length);
        var insidePoint_hex = (pad + (splitPoint_dec-10).toString(16)).slice(-pad.length);
        print(splitPoint_dec + " " + splitPoint_hex + " " + insidePoint_hex);
        if(x == 1) {

        }
        db.adminCommand({split : collection, middle : {_id : splitPoint_hex}});
        //sh.moveChunk(dbName + "." + collection, { "_id" : insidePoint_hex }, "atlas-14dpeu-shard-"+(x-1))
    }
});
sh.stopBalancer();

// double check sh.status(); and db.getSiblingDB("loadtest").queue.getShardDistribution();