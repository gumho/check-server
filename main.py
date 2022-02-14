#!/usr/bin/env python3
import time
import requests

import prometheus_client as prometheus

LISTEN_PORT = 8000

# Servers to check
SERVERS = ['https://httpstat.us/503', 'https://httpstat.us/200']

# How much time in between checks (in seconds)
CHECK_DELAY = 5

# Metric types
RESPONSE_TIME = prometheus.Gauge('sample_external_url_response_ms', "Server response time (in milliseconds)", labelnames=['url'])
STATUS = prometheus.Gauge('sample_external_url_up', "Server status (1 for HTTP 200, otherwise 0)", labelnames=['url'])


def get_metrics_for_url(url):
    # Determine server status (1 for HTTP 200, otherwise 0)
    status = 1
    try:
        resp = requests.get(url)
        if resp.status_code != 200:
            raise requests.exceptions.HTTPError()
    except requests.exceptions.RequestException:
        status = 0

    STATUS.labels(url=url).set(status)

    # Determine server response time (in milliseconds)
    elapsed = 0
    if status == 1:
        elapsed = int(resp.elapsed.total_seconds() * 1000)

    RESPONSE_TIME.labels(url=url).set(elapsed)


if __name__ == '__main__':
    # Unregister unneeded Python client metrics
    prometheus.REGISTRY.unregister(prometheus.PROCESS_COLLECTOR)
    prometheus.REGISTRY.unregister(prometheus.PLATFORM_COLLECTOR)
    prometheus.REGISTRY.unregister(prometheus.REGISTRY._names_to_collectors['python_gc_objects_collected_total'])

    # Start metrics server
    prometheus.start_http_server(LISTEN_PORT)
    while True:
        for server in SERVERS:
            get_metrics_for_url(server)

        time.sleep(CHECK_DELAY)
