"""
Chrysoptera — Automated Database Backup Script

Creates a timestamped SQL dump of the Postgres database running
inside Docker, using pg_dump (run inside the db container via
`docker exec`, so no local Postgres client installation is needed).

Old backups beyond a retention count are automatically cleaned up.
"""

import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

CONTAINER_NAME = "chrysoptera-stack-db-1"
DB_NAME = "chrysoptera_dev"   # matches POSTGRES_DB in docker-compose.yml
DB_USER = "chrysoptera"       # matches POSTGRES_USER in docker-compose.yml
BACKUP_DIR = Path("backups")
KEEP_LAST_N_BACKUPS = 5


def log(message: str) -> None:
    timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")
    print(f"[{timestamp}] {message}")


def create_backup() -> Path:
    """Run pg_dump inside the db container and save the output locally."""
    BACKUP_DIR.mkdir(exist_ok=True)

    timestamp = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
    backup_file = BACKUP_DIR / f"chrysoptera_backup_{timestamp}.sql"

    log(f"Starting backup of database '{DB_NAME}' from container '{CONTAINER_NAME}'...")

    try:
        result = subprocess.run(
            ["docker", "exec", CONTAINER_NAME, "pg_dump", "-U", DB_USER, DB_NAME],
            capture_output=True,
            text=True,
            timeout=60,
            check=True,
        )
    except FileNotFoundError:
        log("ERROR: Docker command not found — is Docker Desktop running?")
        sys.exit(1)
    except subprocess.CalledProcessError as e:
        log(f"ERROR: pg_dump failed: {e.stderr}")
        sys.exit(1)
    except subprocess.TimeoutExpired:
        log("ERROR: pg_dump timed out after 60 seconds")
        sys.exit(1)

    backup_file.write_text(result.stdout, encoding="utf-8")
    size_kb = backup_file.stat().st_size / 1024
    log(f"Backup saved: {backup_file}  ({size_kb:.1f} KB)")

    return backup_file


def cleanup_old_backups() -> None:
    """Keep only the most recent KEEP_LAST_N_BACKUPS backup files."""
    backups = sorted(BACKUP_DIR.glob("chrysoptera_backup_*.sql"), key=lambda p: p.stat().st_mtime)

    if len(backups) <= KEEP_LAST_N_BACKUPS:
        return

    to_delete = backups[:-KEEP_LAST_N_BACKUPS]
    for old_backup in to_delete:
        old_backup.unlink()
        log(f"Deleted old backup (retention policy): {old_backup.name}")


def main() -> int:
    backup_file = create_backup()
    cleanup_old_backups()
    log("Backup process complete.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
