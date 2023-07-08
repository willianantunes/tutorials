#!/bin/sh

# -n  Number of requests to run.
# -c  Number of requests to run concurrently. Total number of requests cannot be smaller than the concurrency level.
# -t  Timeout for each request in seconds. Default is 20, use 0 for infinite.
/hey -n 10 -c 10 -t 60 http://app:8000/only-database-call/
