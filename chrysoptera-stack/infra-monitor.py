"""
Chrysoptera — Infrastructure Monitoring Script (CPU / Memory / Disk)

This checks resource usage at two levels:
  1. HOST level  — the actual machine's overall CPU, RAM, and disk usage
                   (using psutil, which reads real OS-level metrics)
  2. CONTAINER level — per-container CPU and memory usage
                        (using Docker's own `docker stats` command)

Any metric that crosses its threshold gets logged as an ALERT.
This is a simplified, from-scratch version of what tools like
Prometheus + Grafana, or Azure Monitor / AWS CloudWatch, automate
at a much larger scale in real production systems.
"""

import subprocess
import sys
from datetime import datetime, timezone

import psutil

# --- Thresholds: cross these and it counts as an alert ---
CPU_THRESHOLD_PERCENT = 80
MEMORY_THRESHOLD_PERCENT = 85
DISK_THRESHOLD_PERCENT = 90
CONTAINER_CPU_THRESHOLD_PERCENT = 80
CONTAINER_MEM_THRESHOLD_PERCENT = 85

DISK_PATH_TO_CHECK = "C:\\"  # change if monitoring a different drive
LOG_FILE = "infra-monitor.log"


def log(message: str) -> None:
    """Print to console and append to a log file with a timestamp."""
    timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")
    line = f"[{timestamp}] {message}"
    print(line)
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(line + "\n")


def check_host_resources() -> bool:
    """
    Check the actual machine's CPU, memory, and disk usage.
    Returns True if everything is within thresholds, False if any alert fired.
    """
    healthy = True

    # cpu_percent(interval=1) takes a real 1-second sample for an accurate reading,
    # rather than an instantaneous (and often misleading) snapshot.
    cpu_percent = psutil.cpu_percent(interval=1)
    memory_percent = psutil.virtual_memory().percent
    disk_percent = psutil.disk_usage(DISK_PATH_TO_CHECK).percent

    if cpu_percent >= CPU_THRESHOLD_PERCENT:
        log(f"ALERT  Host CPU usage high: {cpu_percent}% (threshold: {CPU_THRESHOLD_PERCENT}%)")
        healthy = False
    else:
        log(f"OK     Host CPU usage: {cpu_percent}%")

    if memory_percent >= MEMORY_THRESHOLD_PERCENT:
        log(f"ALERT  Host memory usage high: {memory_percent}% (threshold: {MEMORY_THRESHOLD_PERCENT}%)")
        healthy = False
    else:
        log(f"OK     Host memory usage: {memory_percent}%")

    if disk_percent >= DISK_THRESHOLD_PERCENT:
        log(f"ALERT  Host disk usage high: {disk_percent}% (threshold: {DISK_THRESHOLD_PERCENT}%)")
        healthy = False
    else:
        log(f"OK     Host disk usage ({DISK_PATH_TO_CHECK}): {disk_percent}%")

    return healthy


def check_container_resources() -> bool:
    """
    Check per-container CPU and memory usage using `docker stats`.
    Returns True if everything is within thresholds, False if any alert fired.
    """
    healthy = True

    try:
        # --no-stream: take one snapshot and exit, instead of streaming forever
        # --format: ask Docker to output plain comma-separated fields we can parse
        result = subprocess.run(
            [
                "docker", "stats", "--no-stream",
                "--format", "{{.Name}},{{.CPUPerc}},{{.MemPerc}}",
            ],
            capture_output=True,
            text=True,
            timeout=10,
            check=True,
        )
    except FileNotFoundError:
        log("ALERT  Docker command not found — is Docker Desktop running?")
        return False
    except subprocess.CalledProcessError as e:
        log(f"ALERT  'docker stats' failed: {e}")
        return False
    except subprocess.TimeoutExpired:
        log("ALERT  'docker stats' timed out")
        return False

    lines = [line for line in result.stdout.strip().splitlines() if line]

    if not lines:
        log("ALERT  No running containers found")
        return False

    for line in lines:
        name, cpu_str, mem_str = line.split(",")
        cpu_value = float(cpu_str.strip("%"))
        mem_value = float(mem_str.strip("%"))

        if cpu_value >= CONTAINER_CPU_THRESHOLD_PERCENT:
            log(f"ALERT  Container '{name}' CPU high: {cpu_value}% (threshold: {CONTAINER_CPU_THRESHOLD_PERCENT}%)")
            healthy = False
        else:
            log(f"OK     Container '{name}' CPU: {cpu_value}%")

        if mem_value >= CONTAINER_MEM_THRESHOLD_PERCENT:
            log(f"ALERT  Container '{name}' memory high: {mem_value}% (threshold: {CONTAINER_MEM_THRESHOLD_PERCENT}%)")
            healthy = False
        else:
            log(f"OK     Container '{name}' memory: {mem_value}%")

    return healthy


def main() -> int:
    log("Starting infrastructure monitoring check")

    host_healthy = check_host_resources()
    containers_healthy = check_container_resources()

    if host_healthy and containers_healthy:
        log("Overall infrastructure status: HEALTHY")
        return 0
    else:
        log("Overall infrastructure status: ALERT(S) TRIGGERED")
        return 1


if __name__ == "__main__":
    sys.exit(main())
