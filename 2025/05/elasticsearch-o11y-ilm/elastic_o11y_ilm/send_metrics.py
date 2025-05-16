import argparse
import gzip
import json
import os
import time

import requests

from faker import Faker
from google.protobuf.json_format import ParseDict
from opentelemetry.proto.collector.metrics.v1.metrics_service_pb2 import ExportMetricsServiceRequest

elastic_apm_server_metrics_endpoint = f"http://{os.getenv("APMSERVER_HOST")}:{os.getenv("APMSERVER_PORT")}/v1/metrics"

default_headers = {
    "User-Agent": "OpenTelemetry Collector Contrib/0.123.0 (linux/amd64)",
    "Accept-Encoding": "gzip",
    "Authorization": f"Bearer {os.getenv("ELASTIC_APM_SECRET_TOKEN")}",
    "Content-Type": "application/x-protobuf",
    "Content-Encoding": "gzip",
}


def update_payload(payload, service_name, environment):
    current_time = int(time.time() * 1e9)  # Current time in nanoseconds
    updated_payload = payload.copy()

    # Update resource attributes
    for attr in updated_payload["resourceMetrics"][0]["resource"]["attributes"]:
        if attr["key"] == "service.name":
            attr["value"]["stringValue"] = service_name
        elif attr["key"] == "deployment.environment":
            attr["value"]["stringValue"] = environment

    # Update metric data points
    for metric in updated_payload["resourceMetrics"][0]["scopeMetrics"][0]["metrics"]:
        for data_point in metric["gauge"]["dataPoints"]:
            data_point["timeUnixNano"] = str(current_time)
            data_point["asInt"] = str(fake_value(metric["name"], data_point["attributes"]))
            current_time += int(0.005 * 1e9)  # Increment by 0.005 seconds

    return updated_payload


def fake_value(metric_name, attributes):
    # Generate fake values based on metric name and attributes
    if metric_name == "system.memory.usage":
        state = next(attr["value"]["stringValue"] for attr in attributes if attr["key"] == "state")
        if state == "used":
            return 25000000000  # Example fake value for used memory
        elif state == "free":
            return 800000000  # Example fake value for free memory
        elif state == "cached":
            return 7800000000  # Example fake value for cached memory
    return 0


def handle(services: list[tuple[str, str]]):
    with open("/app/elastic_o11y_ilm/metrics_payload_template.json") as f:
        payload_template = json.load(f)

    count = 0
    for service_name, environment in services:
        time.sleep(0.01)
        payload = update_payload(payload_template, service_name, environment)
        proto_msg = ParseDict(payload, ExportMetricsServiceRequest())
        payload_bytes = proto_msg.SerializeToString()
        compressed = gzip.compress(payload_bytes)
        response = requests.post(
            elastic_apm_server_metrics_endpoint,
            headers=default_headers,
            data=compressed,
            timeout=10,
            verify=False,
        )
        if response.status_code != 200:
            print(f"Status: {response.status_code}, Response: {response.text}")
        count += 1
        if count % 50 == 0:
            print(f"Sent {count} metrics payloads...")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--fake-services-count", type=int, default=10)
    parser.add_argument("--faker-seed", type=int, default=1)
    args = parser.parse_args()

    fake_services_count = args.fake_services_count
    faker_seed = args.faker_seed
    faker = Faker(faker_seed)
    fake_services = []
    print("Faker services count:", fake_services_count)
    print("Creating 3 entries per fake service, one for each K8S namespace")
    for _ in range(fake_services_count):
        fake_service_name = faker.slug(faker.company())
        fake_services += [
            (fake_service_name, "development"),
            (fake_service_name, "qa"),
            (fake_service_name, "production"),
        ]
    print("Number of fake services including their namespace:", len(fake_services))
    handle(fake_services)
    print("Done!")
    print("Checkout the indices in Kibana searching for `metrics-apm.app.`")
    print("https://localhost:5601/app/management/data/index_management/indices")
    print("Checkout the data streams in Kibana searching for the data stream name: `metrics-apm.app.`")
    print("https://localhost:5601/app/management/data/index_management/data_streams")
    print("Know the issue: https://github.com/elastic/apm-server/issues/8182")
