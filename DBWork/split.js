// original source: https://github.com/jayrunkel/gmDataLoad/blob/master/sharding/setUpSharding.js
// thanks, Uncle Runkel

////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
// GLOBAL VARS
////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
var numShards = 8;                            // CHANGE ME: how many shards
var dbName = "loadtest";                      // CHANGE ME: what DB we using
var colNames = ["loadtest.queue"];            // CHANGE ME: array of collections we are working with
var shardPrefix = "atlas-14dpeu-shard-";      // CHANGE ME: from atlas portal

var avgDocSizeKb = 11;                        // CHANGE ME: based on your load generator in locustfile.py
var keySpaceSize = 16;                        // CHANGE ME: get this from the key space in worker-variables.env but this will break if not 16
var keyCount = 7;                             // CHANGE ME: get this from the key space in worker-variables.env

////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
// Do the work, do not modify below here
////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
var expectedDocCount = Math.pow(keySpaceSize, keyCount);
var CHUNKSIZEKB = 64*1024;                                                          // don't change this
var numOfChunks = ((expectedDocCount * avgDocSizeKb) / CHUNKSIZEKB) * 2;            // we are doubling because we want the chunks to be half empty
var chunkSplitInterval = Math.floor(expectedDocCount / numOfChunks);
var lbound = 0;
var zoneCardinality = Math.round(expectedDocCount / numShards);
var pad = "";
for (p=0; p < keyCount; p++) {
    pad = pad + "0";
}



var db = db.getSiblingDB(dbName);

db.dropDatabase();
sh.enableSharding(dbName);

print("shard each collection...");
colNames.forEach(collection => {
	sh.shardCollection(collection, {_id : 1}, false);
});

print("starting presplit...");
colNames.forEach(collection => {
    print("starting collection: ", collection);
    var ct =0;
    
    for (x = lbound + Math.floor(chunkSplitInterval / 2); x < expectedDocCount; x = x + chunkSplitInterval) {
        var splitId = (pad + x.toString(16)).slice(-pad.length);
        if(ct%100 == 0) {
            print("Done at least " + ct + " of " + numOfChunks);
        }
        db.adminCommand({split : collection, middle : {_id : splitId}});
        ct++;
   }
});

// double check sh.status(); and db.getSiblingDB("loadtest").queue.getShardDistribution();