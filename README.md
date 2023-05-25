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

## Additional items to note

