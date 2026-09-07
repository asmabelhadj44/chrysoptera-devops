"""
Chrysoptera — Basic Infrastructure Health-Check Script
Checks the FastAPI service's /health and /readings endpoints,
logs the result with a timestamp, and exits with a status code
suitable for automation (0 = healthy, 1 = unhealthy).
"""

import sys
import time
from datetime import datetime, timezone

import requests

BASE_URL = "http://localhost:8000"
ENDPOINTS_TO_CHECK = ["/health", "/readings"]
TIMEOUT_SECONDS = 5
LOG_FILE = "healthcheck.log"


def log(message: str) -> None:
    """Print to console and append to a log file with a timestamp."""
    timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")
    line = f"[{timestamp}] {message}"
    print(line)
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(line + "\n")


def check_endpoint(path: str) -> bool:
    """Check a single endpoint. Returns True if healthy, False otherwise."""
    url = f"{BASE_URL}{path}"
    start = time.time()
    try:
        response = requests.get(url, timeout=TIMEOUT_SECONDS)
        elapsed_ms = round((time.time() - start) * 1000)

        if response.status_code == 200:
            log(f"OK   {path}  status={response.status_code}  {elapsed_ms}ms")
            return True
        else:
            log(f"FAIL {path}  status={response.status_code}  {elapsed_ms}ms")
            return False

    except requests.exceptions.ConnectionError:
        log(f"FAIL {path}  error=connection refused (is the stack running?)")
        return False
    except requests.exceptions.Timeout:
        log(f"FAIL {path}  error=timed out after {TIMEOUT_SECONDS}s")
        return False
    except requests.exceptions.RequestException as e:
        log(f"FAIL {path}  error={e}")
        return False


def main() -> int:
    log(f"Starting health check against {BASE_URL}")
    results = [check_endpoint(path) for path in ENDPOINTS_TO_CHECK]

    if all(results):
        log("Overall status: HEALTHY")
        return 0
    else:
        log("Overall status: UNHEALTHY")
        return 1


if __name__ == "__main__":
    sys.exit(main())
