# Chrysoptera — Cloud Computing / DevOps Internship

DevOps track deliverables for an internship with Innovation Ecosystem, built around **Chrysoptera**, an AI-layer platform for renewable energy (solar monitoring + carbon accounting), delivered as a SaaS product.

This repo covers Month 1: local infrastructure, CI/CD, Infrastructure as Code, monitoring, and operational documentation.

## Project structure

```
chrysoptera-devops/
├── chrysoptera-stack/              # The actual application: FastAPI + PostgreSQL + Redis
│   ├── api/
│   │   ├── main.py                 # FastAPI app (/health, /readings)
│   │   ├── test_main.py            # Automated tests (pytest)
│   │   ├── requirements.txt
│   │   └── Dockerfile
│   ├── docker-compose.yml          # Wires api + db + redis together locally
│   ├── healthcheck.py              # Application-level monitoring (endpoint checks)
│   ├── infra-monitor.py            # Host + container-level monitoring (CPU/memory/disk, with alerts)
│   └── backup_database.py          # Automated Postgres backups with retention
│
├── chrysoptera-terraform-tutorial/ # W1-02: Terraform learning exercise (local Docker provider)
│
├── chrysoptera-terraform-postgres/ # W3: Real Infrastructure as Code for a cloud Postgres database
│   └── postgres.tf                 # Deployed and verified on Azure (Postgres Flexible Server)
│
├── .github/workflows/
│   └── lint.yml                    # CI: lints Python + runs tests on every push
│
└── docs/                           # Written deliverables (reports, plans, runbooks — see below)
```

## What's implemented

- **CI/CD**: every push is automatically linted (flake8) and tested (pytest) via GitHub Actions.
- **Infrastructure as Code**: the Postgres database is defined in Terraform and was deployed for real on Azure (Postgres Flexible Server, Switzerland North), then torn down cleanly — proving the full apply/destroy lifecycle works, not just documented.
- **Monitoring**: two layers — application-level (`healthcheck.py`, checks the API itself) and infrastructure-level (`infra-monitor.py`, checks CPU/memory/disk on the host and per Docker container, with threshold-based alerting).
- **Backups**: automated PostgreSQL backups via `pg_dump`, with retention (keeps the last 5), tested including the cleanup logic.

## Documentation

Written deliverables (cost comparisons, architecture, secrets management, disaster recovery, runbooks, GDPR notes, etc.) are collected in `docs/` — see the Month 1 Summary there for a full narrative walkthrough of the internship.

## Running it locally

```
cd chrysoptera-stack
docker compose up -d
python healthcheck.py
```

See `docs/w4-deployment-runbook.md` for the full step-by-step procedures (setup, shipping code changes, provisioning cloud infrastructure).
