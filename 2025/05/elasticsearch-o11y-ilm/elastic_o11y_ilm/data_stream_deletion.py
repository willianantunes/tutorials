import argparse
import os
import warnings

from elasticsearch import Elasticsearch

warnings.filterwarnings("ignore")
ES_HOST = f"https://{os.getenv('ELASTICSEARCH_HOST')}:{os.getenv('ELASTICSEARCH_PORT')}"
ES_USERNAME_PASSWORD = "elastic:elastic"


def delete_data_streams(es_client, pattern):
    try:
        # Retrieve all data streams matching the pattern
        response = es_client.indices.get_data_stream(name=pattern)
        data_streams = response["data_streams"]

        if not data_streams:
            print(f"No data streams found matching pattern: {pattern}")
            return

        # Extract data stream names
        data_stream_names = [ds["name"] for ds in data_streams]
        print(f"Found {len(data_stream_names)} data streams to delete")

        # Bulk delete data streams
        restricted_indices = [
            ".fleet-actions-results",
        ]
        count = 0
        for data_stream in data_stream_names:
            if data_stream not in restricted_indices:
                es_client.indices.delete_data_stream(name=data_stream)
                count += 1
                if count % 25 == 0:
                    print(f"Deleted {count} data streams...")
    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--pattern", type=str, default="metrics-apm.app.*")
    args = parser.parse_args()
    pattern = args.pattern

    es_client = Elasticsearch(hosts=ES_HOST, basic_auth=tuple(ES_USERNAME_PASSWORD.split(":")), verify_certs=False)

    print(f"Deleting data streams matching pattern: {pattern}")
    delete_data_streams(es_client, pattern)
    print("Done!")
