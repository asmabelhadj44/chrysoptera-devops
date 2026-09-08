# W4 — Automated Database Backups

**Task:** Automated database backups (real or simulated)
**Status:** Done — implemented for real, tested including the retention/cleanup logic
**Context:** Chrysoptera DevOps internship, Week 4 (Security, Docs & Demo)

---

## What it does

`backup_database.py` creates a timestamped SQL dump of the live Postgres database, using `pg_dump` run *inside* the existing `db` container via `docker exec` — meaning no separate Postgres client needs to be installed on the host machine at all, since the tool already exists inside the container image.

Each backup is saved as `backups/chrysoptera_backup_YYYYMMDD_HHMMSS.sql`, and the script automatically deletes the oldest backups once more than 5 exist — a basic retention policy, so backups don't accumulate indefinitely.

## Why this design

- **Runs against the real container name and real credentials** (`chrysoptera-stack-db-1`, database `chrysoptera_dev`, user `chrysoptera`) pulled directly from the actual `docker-compose.yml` — not generic placeholders.
- **`pg_dump` inside the container, not on the host**: avoids needing to install and version-match a Postgres client separately on Windows, since the exact right version already lives inside the `postgres:16` image.
- **Retention policy included from the start**: an unlimited, ever-growing pile of backup files is itself a problem (disk usage, and per the GDPR note this week, a data-retention/erasure concern) — so cleanup isn't an afterthought here.

## Verification performed

This wasn't just written and assumed to work — it was run for real against the live stack:
1. Ran once — produced a real 0.7 KB `.sql` file with actual `pg_dump` output.
2. Ran 5 additional times in a row to simulate a week of daily backups.
3. Confirmed the retention logic actually fired: the script logged `Deleted old backup (retention policy): chrysoptera_backup_20260906_234448.sql` on the 6th run, and a final directory listing showed exactly 5 files remaining, with the oldest correctly removed.

## How to run it

```
python backup_database.py
```
Run from the `chrysoptera-stack` folder, with the Docker stack running (`docker ps` should show the `db` container up).

## Restoring from a backup (the other half of "backup")

A backup that's never been tested for restore isn't a real backup — it's just an unverified file. To restore:
```
docker exec -i chrysoptera-stack-db-1 psql -U chrysoptera -d chrysoptera_dev < backups/chrysoptera_backup_TIMESTAMP.sql
```
This feeds the saved SQL dump back into the running database, recreating its state at backup time — directly supporting Scenario 1 of this week's Disaster Recovery Plan.

## Known limitations, stated honestly

- Runs on-demand, not on a schedule — the natural next step is registering it as a **Windows Task Scheduler** job to run automatically (e.g. daily), which would need no code changes, only a scheduled trigger pointing at this script.
- Backups are stored locally only, in the same folder as the project — a real production setup would also copy backups to a separate location (e.g. cloud blob storage) so a single machine failure can't take out both the database *and* its backups at once.
- Restore was documented but not yet executed — a good next step before fully trusting this system would be to actually run a restore against a test database and confirm the data matches.

---
*Chrysoptera — Cloud Computing / DevOps Internship — Week 4*
