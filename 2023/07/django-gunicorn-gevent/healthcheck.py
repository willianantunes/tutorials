import os

import requests

address = os.getenv("DJANGO_BIND_ADDRESS", "0.0.0.0")
port = os.getenv("DJANGO_BIND_PORT", "8000")

result = requests.get(f"http://{address}:{port}/healthcheck/liveness", timeout=5)

if result.status_code == 200:
    exit(0)
else:
    exit(1)
