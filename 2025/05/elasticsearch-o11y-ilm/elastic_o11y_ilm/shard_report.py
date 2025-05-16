import csv
import os
import re

from collections import Counter
from collections import defaultdict

import requests

ES_HOST = f"https://{os.getenv("ELASTICSEARCH_HOST")}:{os.getenv("ELASTICSEARCH_PORT")}"
ES_USERNAME_PASSWORD = "elastic:elastic"
CAT_SHARDS_ENDPOINT = f"{ES_HOST}/_cat/shards?format=json"


def fetch_shards():
    credentials = tuple(ES_USERNAME_PASSWORD.split(":"))
    resp = requests.get(CAT_SHARDS_ENDPOINT, auth=credentials, verify=False)
    resp.raise_for_status()
    return resp.json()


def parse_size_gb(size_str):
    if not size_str:
        return 0.0
    size_str = size_str.strip().lower()
    match = re.match(r"([\d.]+)([a-z]+)", size_str)
    if not match:
        return 0.0
    size, unit = match.groups()
    size = float(size)
    unit_multipliers = {"b": 1 / 1_073_741_824, "kb": 1 / 1_048_576, "mb": 1 / 1024, "gb": 1, "tb": 1024}
    return size * unit_multipliers.get(unit, 0.0)


def aggregate_index_data(shards):
    shard_count = Counter()
    storage_usage = defaultdict(float)
    for shard in shards:
        index = shard["index"]
        size_str = shard.get("store", "0")
        size_gb = parse_size_gb(size_str)
        shard_count[index] += 1
        storage_usage[index] += size_gb
    return shard_count, storage_usage


def print_report(shard_count, storage_usage):
    print(f"{'Index':<40} | {'Shards':<6} | {'Storage (GB)':<12}")
    print("-" * 65)
    for index in sorted(shard_count, key=lambda i: shard_count[i], reverse=True):
        print(f"{index:<40} | {shard_count[index]:<6} | {storage_usage[index]:<12.2f}")


def save_report_csv(shard_count, storage_usage, filename="shard_report.csv"):
    with open(filename, mode="w", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Index", "Shards", "Storage (GB)"])
        for index in sorted(shard_count, key=lambda i: shard_count[i], reverse=True):
            writer.writerow([index, shard_count[index], f"{storage_usage[index]:.2f}"])
        total_shards = sum(shard_count.values())
        total_storage = sum(storage_usage.values())
        writer.writerow(["Total", total_shards, f"{total_storage:.2f}"])


if __name__ == "__main__":
    shards = fetch_shards()
    shard_count, storage_usage = aggregate_index_data(shards)
    save_report_csv(shard_count, storage_usage)
