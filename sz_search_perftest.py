#! /usr/bin/env python3

import concurrent.futures

import argparse
import pathlib
import orjson
import itertools

import sys
import os
import time
from timeit import default_timer as timer

import senzing_core
from senzing import SzEngineFlags, SzError

INTERVAL = 1000


def process_line(engine, line):
    try:
        record = orjson.loads(line.encode())
        startTime = timer()
        response = engine.search_by_attributes(
            line, SzEngineFlags.SZ_SEARCH_BY_ATTRIBUTES_MINIMAL_ALL
        )
        # engine.searchByAttributes( line, response, SzEngineFlags.SZ_SEARCH_INCLUDE_FEATURE_SCORES )
        # engine.searchByAttributes( line, response, SzEngineFlags.SZ_ENTITY_INCLUDE_RECORD_DATA )
        # engine.searchByAttributes( line, response, SzEngineFlags.SZ_SEARCH_INCLUDE_FEATURE_SCORES | SzEngineFlags.SZ_ENTITY_INCLUDE_RECORD_DATA )
        # engine.searchByAttributes( line, response, SzEngineFlags.SZ_SEARCH_INCLUDE_FEATURE_SCORES | SzEngineFlags.SZ_ENTITY_INCLUDE_RECORD_DATA | SzEngineFlags.SZ_ENTITY_INCLUDE_RECORD_JSON_DATA)
        # engine.searchByAttributes( line, response, SzEngineFlags.SZ_SEARCH_INCLUDE_FEATURE_SCORES | SzEngineFlags.SZ_ENTITY_INCLUDE_RECORD_DATA | SzEngineFlags.SZ_ENTITY_INCLUDE_REPRESENTATIVE_FEATURES )
        return (timer() - startTime, record["RECORD_ID"], response)
    except Exception as err:
        print(f"{err} [{line}]", file=sys.stderr)
        raise


try:
    parser = argparse.ArgumentParser()
    parser.add_argument("fileToProcess", default=None)
    parser.add_argument(
        "-t",
        "--debugTrace",
        dest="debugTrace",
        action="store_true",
        default=False,
        help="output debug trace information",
    )
    args = parser.parse_args()

    engine_config = os.getenv("SENZING_ENGINE_CONFIGURATION_JSON")
    if not engine_config:
        print(
            "The environment variable SENZING_ENGINE_CONFIGURATION_JSON must be set with a proper JSON configuration.",
            file=sys.stderr,
        )
        print(
            "Please see https://senzing.zendesk.com/hc/en-us/articles/360038774134-SzModule-Configuration-and-the-Senzing-API",
            file=sys.stderr,
        )
        exit(-1)

    # Initialize Senzing
    factory = senzing_core.SzAbstractFactoryCore(
        "sz_search_perftest", engine_config, verbose_logging=args.debugTrace
    )
    g2 = factory.create_engine()
    g2.prime_engine()
    max_workers = int(os.getenv("SENZING_THREADS_PER_PROCESS", 0))
    if not max_workers:  # reset to null for executors
        max_workers = None

    g2Diagnostic = factory.create_diagnostic()
    response = g2Diagnostic.check_datastore_performance(3)
    print(response)

    beginTime = prevTime = time.time()
    timeMin = timeMax = timeTot = count = 0
    timesAll = []

    with open(args.fileToProcess, "r") as fp:
        numLines = 0
        q_multiple = 2
        total_entities_returned = 0

        with concurrent.futures.ThreadPoolExecutor(max_workers) as executor:
            print(f"Searching with {executor._max_workers} threads")
            try:
                futures = {
                    executor.submit(process_line, g2, line): line
                    for line in itertools.islice(fp, q_multiple * executor._max_workers)
                }

                while futures:

                    done, _ = concurrent.futures.wait(
                        futures, return_when=concurrent.futures.FIRST_COMPLETED
                    )
                    for fut in done:
                        result = fut.result()
                        futures.pop(fut)

                        if result:
                            count += 1
                            result_time = result[0]
                            timesAll.append(result)
                            timeTot += result_time
                            if timeMin == 0:
                                timeMin = result_time
                            else:
                                timeMin = min(timeMin, result_time)
                            timeMax = max(timeMax, result_time)
                            response = orjson.loads(result[2])
                            if response:
                                total_entities_returned += len(response["RESOLVED_ENTITIES"])

                        numLines += 1
                        if numLines % INTERVAL == 0:
                            nowTime = time.time()
                            speed = int(INTERVAL / (nowTime - prevTime))
                            print(
                                f"Processed {numLines} searches, {speed} records per second, entities returned {total_entities_returned}: avg[{timeTot/count:.3f}s] tps[{count/(time.time()-beginTime):.3f}/s] min[{timeMin:.3f}s] max[{timeMax:.3f}s]"
                            )
                            prevTime = nowTime
                        if numLines % 100000 == 0:
                            response = g2.get_stats()
                            print(f"\n{response}\n")

                        line = fp.readline()
                        if line:
                            futures[executor.submit(process_line, g2, line)] = line

                print(
                    f"Processed total of {numLines} searches, entities returned {total_entities_returned}: avg[{timeTot/count:.3f}s] tps[{count/(time.time()-beginTime):.3f}/s] min[{timeMin:.3f}s] max[{timeMax:.3f}s]"
                )
                timesAll.sort(key=lambda x: x[0], reverse=True)

                i = 0
                while i < count:
                    if timesAll[i][0] <= 1.0:
                        break
                    i += 1
                print(f"Percent under 1s: {(count-i)/count*100:.1f}%")
                print(f"longest: {timesAll[0][0]:.3f}s record[{timesAll[0][1]}]")

                p99 = int(count * 0.01)
                p95 = int(count * 0.05)
                p90 = int(count * 0.10)

                i = 0
                while i < p90:
                    i += 1
                    if i == p99:
                        print(f"p99: {timesAll[i][0]:.3f}s record[{timesAll[i][1]}]")
                    if i == p95:
                        print(f"p95: {timesAll[i][0]:.3f}s record[{timesAll[i][1]}]")
                    if i == p90:
                        print(f"p90: {timesAll[i][0]:.3f}s record[{timesAll[i][1]}]")

                response = g2.get_stats()
                print(response)

            except Exception as err:
                print(f"Shutting down due to error: {err}", file=sys.stderr)
                executor.shutdown()
                exit(-1)

except Exception as err:
    print(err, file=sys.stderr)
    exit(-1)
