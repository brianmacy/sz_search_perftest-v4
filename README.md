# sz_search_perftest

# Overview
Simple parallel JSON data processor using the Senzing API and is meant to provide developers with a simple starting point for a simple, scalable search.

# API demonstrated
### Core
* searchByAttributes: Searches the JSON search request (assumes a RECORD_ID attribute for tracking)
### Supporting
* init: To initialize the G2Engine and G2Diagnostics objects
* stats: To retrieve internal engine diagnostic information as to what is going on in the engine
* checkDBPerf: To check single threaded/connection DB latency

For more details on the Senzing API go to https://docs.senzing.com

# Details

### Required parameter (environment)
```
SENZING_ENGINE_CONFIGURATION_JSON
```

### Optional parameters (environment)
```
SENZING_THREADS_PER_PROCESS (default: based on whatever concurrent.futures.ThreadPoolExecutor chooses automatically)
```

## Running
```
./sz_search_perftest <search file of JSON lines>
```
## Example output
```
{"numRecordsInserted":24436,"insertTime":3000}
Searching with 20 threads
Processed total of 5407 searches: avg[0.151s] min[0.004s] max[1.037s]
Percent under 1s: 99.9%
longest: 1.037s record[12313]
p99: 0.415s record[24362436]
p95: 0.300s record[345345]
p95: 0.287s record[796876867]
{ "workload": { "apiVersion": "3.6.2.DEVELOPMENT_VERSION",  "loadedRecords": -1,  "addedRecords": 0,  "deletedRecords": 0,  "reevaluations": 0,  "repairedEntities": 0,  "duration": 0,  "retries": 0,  "candidates": 213271,  "actualAmbiguousTest": 0,  "cachedAmbiguousTest": 0,  "libFeatCacheHit": 1042374,  "libFeatCacheMiss": 764836,  "resFeatStatCacheHit": 3402983,  "resFeatStatCacheMiss": 861731,  "resFeatStatUpdate": 51389,  "unresolveTest": 0,  "abortedUnresolve": 0,  "gnrScorersUsed": 1,  "unresolveTriggers": { "normalResolve" : 0,  "update" : 0,  "relLink" : 0,  "extensiveResolve" : 0,  "ambiguousNoResolve" : 0,  "ambiguousMultiResolve" : 0  }, "reresolveTriggers": { "abortRetry" : 0,  "unresolveMovement" : 0,  "multipleResolvableCandidates" : 0,  "resolveNewFeatures" : 0,  "newFeatureFTypes": [ ]  }, "reresolveSkipped" : 0,  "filteredObsFeat" : 8929,  "expressedFeatureCalls": [  { "EFCALL_ID": 1,"EFUNC_CODE": "PHONE_HASHER", "numCalls":7 } ,  { "EFCALL_ID": 7,"EFUNC_CODE": "NAME_HASHER", "numCalls":5413 } ,  { "EFCALL_ID": 9,"EFUNC_CODE": "ADDR_HASHER", "numCalls":10808 } ,  { "EFCALL_ID": 11,"EFUNC_CODE": "EXPRESS_ID", "numCalls":4 } ,  { "EFCALL_ID": 29,"EFUNC_CODE": "EXPRESS_ID", "numCalls":7 } ],  "expressedFeaturesCreated": [  { "ADDR_KEY": 18193 } ,  { "ID_KEY": 11 } ,  { "NAME_KEY": 62425 } ,  { "PHONE_KEY": 7 } ],  "scoredPairs": [  { "ADDRESS": 855440 } ,  { "NAME": 345105 } ,  { "TAX_ID": 15 } ,  { "WEBSITE": 6 } ],  "cacheHit": [  { "ADDRESS": 80082 } ,  { "NAME": 66183 } ],  "cacheMiss": [  { "ADDRESS": 775358 } ,  { "NAME": 278922 } ],  "redoTriggers": [ ],  "latchContention": [ ],  "highContentionFeat": [ ],  "highContentionResEnt": [ ],  "genericDetect": [ ],  "candidateBuilders": [  { "ADDR_KEY": 3794 } ,
{ "ID_KEY": 7 } ,  { "NAME_KEY": 5407 } ,  { "PHONE": 7 } ,  { "PHONE_KEY": 7 } ,  { "TAX_ID": 4 } ,  { "WEBSITE": 5 } ],  "suppressedCandidateBuilders": [ ],  "suppressedScoredFeatureType": [  { "ADDRESS": 4 } ],  "suppressedDisclosedRelationshipDomainCount":  0 ,  "CorruptEntityTestDiagnosis": { },  "threadState": { "active": 0,"idle": 21,"sqlExecuting": 0,"loader": 0,"resolver": 0,"scoring": 0,"dataLatchContention": 0,"obsEntContention": 0,"resEntContention": 0},  "systemResources": {  "initResources": [ { "physicalCores": 16 },{ "logicalCores": 16 },{ "totalMemory": "125.6GB" },{ "availableMemory": "123.4GB" }],  "currResources": [ { "availableMemory": "120.2GB" },{ "activeThreads": 0 },{ "workerThreads": 21 }, {  "systemLoad": [ ] } ] } } }

```

## Additional items to note

