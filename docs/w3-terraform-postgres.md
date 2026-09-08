# W3 — Terraform Config: PostgreSQL Database

**Task:** Terraform config to provision a PostgreSQL database
**Status:** Done (documented/conceptual — not applied, no paid AWS account)
**Context:** Chrysoptera DevOps internship, Week 3 (Infrastructure as Code)

---

## Why this is documented rather than applied

Unlike the W1-02 Terraform tutorial (which used the free `kreuzwerker/docker` provider to build a real, runnable local example), provisioning an actual AWS RDS instance requires a paid AWS account and billing setup that isn't available for this internship. This config is written to be **immediately usable** if/when real AWS credentials are available — nothing here is a placeholder or pseudocode, it's real, valid Terraform HCL.

## What the config does (`postgres.tf`)

Provisions a single **AWS RDS PostgreSQL** instance sized appropriately for early-stage traffic — matching the "100 solar sites, one reading every 5 minutes" assumption from the W1-01 cost comparison, where volume is small enough not to need anything heavier.

### Key decisions and why

| Setting | Value | Reasoning |
|---|---|---|
| `instance_class` | `db.t3.micro` | Cheapest burstable-performance tier — appropriate for low, steady write volume at this stage; easy to resize later with one line change |
| `allocated_storage` | `20` GB | RDS minimum for Postgres; plenty of headroom for readings + carbon-accounting data early on |
| `multi_az` | `false` | Multi-AZ (automatic failover to a standby in another zone) roughly doubles cost — not justified until this is a production system with uptime guarantees |
| `skip_final_snapshot` | `true` | Appropriate for a staging/dev database that can be recreated; would be set to `false` for a real production database |
| `backup_retention_period` | `7` days | Minimal safety net against accidental data loss, without paying for long retention on a non-critical environment |
| `publicly_accessible` | `false` | Database should only be reachable from inside the app's network (e.g. the same VPC as the FastAPI service), never directly from the internet |

### Credentials handling

`db_username` and `db_password` are declared as `sensitive = true` **variables**, not hardcoded values — Terraform will hide them from console output and plan diffs. In practice these would be supplied via a `terraform.tfvars` file that is **never committed to Git** (see the Secrets Management Plan doc for the full approach), or injected via environment variables (`TF_VAR_db_password`).

## How this fits the existing stack

This replaces the local `postgres` service currently defined in `docker-compose.yml` (from W1-03) with a managed, durable equivalent for a real deployment. The FastAPI app's database connection string would simply point at the `db_endpoint` output instead of `localhost`, once the DB is provisioned — no application code changes needed beyond the connection string.

## To actually apply this (future step, once an AWS account exists)

```
terraform init
terraform plan   -var="db_username=..." -var="db_password=..."
terraform apply  -var="db_username=..." -var="db_password=..."
```
(Never type real credentials directly in the command like this in practice — use a `.tfvars` file or environment variables instead. Shown inline here only to illustrate the two required variables.)

---
*Chrysoptera — Cloud Computing / DevOps Internship — Week 3*
