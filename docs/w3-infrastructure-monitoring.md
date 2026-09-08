# W3 — Basic Infrastructure Monitoring: Health-Check + Resource Alerts

**Task:** Basic infra monitoring (health-check script is enough) — extended to full CPU/memory/disk monitoring with alerting
**Status:** Done
**Context:** Chrysoptera DevOps internship, Week 3 (Infrastructure as Code)

---

## Two scripts, two different layers of monitoring

It's worth being precise about what each script actually checks, since "monitoring" can mean different things:

| Script | Layer | Question it answers |
|---|---|---|
| `healthcheck.py` | **Application-level** | "Does my API respond correctly?" (HTTP status + response time) |
| `infra-monitor.py` | **Host + container-level** | "Is the underlying machine or a specific container running out of CPU, memory, or disk?" |

Both matter, and neither substitutes for the other — an API can return `200 OK` in 12ms while the host machine is one bad deploy away from running out of disk space, and vice versa.

## What `infra-monitor.py` does

**Host-level checks** (via the `psutil` library, which reads real OS metrics):
- CPU usage (sampled over 1 second for an accurate reading, not an instantaneous snapshot)
- Memory (RAM) usage
- Disk usage on the C: drive

**Container-level checks** (via Docker's own `docker stats --no-stream` command):
- Per-container CPU usage (`db`, `redis`, `api` containers individually)
- Per-container memory usage

**Alerting logic:**
Each metric is compared against a threshold (CPU 80%, memory 85%, disk 90%, matching the same thresholds applied per-container). Crossing a threshold logs a line prefixed `ALERT` instead of `OK`, and the script exits with code `1` instead of `0` — the same "automation-friendly" exit code pattern used in `healthcheck.py`.

## Why these specific thresholds, and why this approach

This mirrors what production monitoring tools (Prometheus + Grafana + Alertmanager, or Azure Monitor / AWS CloudWatch) do at a larger scale — collect a metric, compare it to a threshold, fire an alert if crossed. Those tools add historical graphing, multi-machine aggregation, and integrations (Slack, email, PagerDuty) that were out of scope for this milestone, but the underlying *mechanism* — threshold-based alerting on real system metrics — is genuinely the same idea, built from scratch here to understand how it actually works under the hood.

## Verification: the alert logic was tested, not just assumed to work

To confirm the alerting actually fires (rather than trusting untested code), the CPU threshold was temporarily lowered to 1% — a value guaranteed to be exceeded — and rerun. This produced a real `ALERT Host CPU usage high: 6.3% (threshold: 1%)` line and flipped the overall status to `ALERT(S) TRIGGERED`, confirming the comparison and logging logic both work correctly. The threshold was then restored to the real value (80%) for actual use.

## How to run it

1. Make sure Docker Desktop and the stack are running (`docker ps` should show 3 containers).
2. Install the dependency: `pip install psutil`
3. Run: `python infra-monitor.py`

Example healthy output:
```
[2026-09-06 21:57:13 UTC] Starting infrastructure monitoring check
[2026-09-06 21:57:14 UTC] OK     Host CPU usage: 6.7%
[2026-09-06 21:57:14 UTC] OK     Host memory usage: 75.8%
[2026-09-06 21:57:14 UTC] OK     Host disk usage (C:\): 72.1%
[2026-09-06 21:57:16 UTC] OK     Container 'chrysoptera-stack-api-1' CPU: 0.17%
[2026-09-06 21:57:16 UTC] Overall infrastructure status: HEALTHY
```

## Known limitations, stated honestly

- Runs on-demand, not continuously — could be scheduled via Windows Task Scheduler to run every few minutes for a real ongoing history (same idea noted for `healthcheck.py`).
- Alerts are logged locally only — no actual notification (email/Slack/etc.) is sent. Adding that would be the natural next step for a production version.
- Disk usage is checked for the host's C: drive only, not per-container disk usage, since Docker doesn't expose that as simply via `docker stats`.

---
*Chrysoptera — Cloud Computing / DevOps Internship — Week 3*

