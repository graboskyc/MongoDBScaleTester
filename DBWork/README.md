# Pre-splitting

To get the highest ingest rate performance, pre-split!

* Deploy an Atlas cluster
* `mongosh` in as an Atlas admin
* run the [split.js](split.js) script and wait for it to complete
* then start the ingest
* Verify chunks with commands like:
  * `sh.status();`
  * and `db.getSiblingDB("loadtest").queue.getShardDistribution();`