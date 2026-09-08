# W4 — Deployment Runbook

**Task:** Deployment runbook (written doc)
**Status:** Done
**Context:** Chrysoptera DevOps internship, Week 4 (Security, Docs & Demo)

---

## Purpose

A runbook is a step-by-step procedure written so that **anyone** (not just the person who built the system) can follow it under pressure or time constraints and get a correct result. The test for a good runbook: could someone unfamiliar with this project follow it literally, top to bottom, without needing to ask a question?

## Runbook 1: Deploying the local development stack (from scratch)

**When to use:** Setting up the project on a new machine, or after Scenario 2 from the DR plan (lost machine).

1. Install Docker Desktop, Git, and Python (3.11+) if not already present.
2. Clone the repo: `git clone https://github.com/asmabelhadj44/chrysoptera-devops.git`
3. Navigate into the stack folder: `cd chrysoptera-devops/chrysoptera-stack`
4. Start all services: `docker compose up -d`
5. Verify: open `http://localhost:8000/health` in a browser — should return `{"status": "ok"}`
6. Run the health-check script to confirm end-to-end: `python healthcheck.py` — should print `Overall status: HEALTHY`

**Rollback:** `docker compose down` stops and removes the containers cleanly; no persistent state is lost outside the Docker volumes.

## Runbook 2: Shipping a code change through CI

**When to use:** Any change to the FastAPI application code.

1. Create a feature branch: `git checkout -b feature/short-description` (per the Week 2 branching strategy)
2. Make the change, then run tests locally before pushing: `pytest -v` (from `chrysoptera-stack/api`)
3. Commit and push: `git add .` → `git commit -m "..."` → `git push -u origin feature/short-description`
4. Open a Pull Request on GitHub into `main`.
5. Wait for the GitHub Actions checks (lint + tests) to show green on the PR — **do not merge if either check is red.**
6. Merge the PR, then delete the feature branch.
7. Pull `main` locally and redeploy the local stack if testing the merged result: `git pull` → `docker compose up -d --build` (the `--build` flag rebuilds the image with the new code, rather than reusing the old cached image).

**Rollback:** `git revert <commit-hash>` on `main`, push, and let CI re-verify the reverted state — safer than manually editing files back, since it preserves a clear history of what happened.

## Runbook 3: Provisioning the cloud database (Terraform)

**When to use:** Setting up the Postgres database in a real cloud environment (as demonstrated this week on Azure).

1. Ensure Azure CLI is installed and authenticated: `az login`
2. Navigate to the Terraform config: `cd chrysoptera-terraform-postgres`
3. Initialize: `terraform init`
4. Preview changes: `terraform plan -var="db_username=..." -var="db_password=..." -var="my_ip=..."`
5. **Review the plan output carefully** — confirm the resource count and names match expectations before proceeding.
6. Apply: `terraform apply` with the same variables, then type `yes` when prompted.
7. Confirm the deployment succeeded by checking the `db_host` output and verifying the resource in the Azure Portal.

**Rollback:** `terraform destroy` with the same variables removes exactly what was created — this was demonstrated for real this week (4 resources created, 4 destroyed cleanly).

## General rules that apply across all three runbooks

- **Never run destructive commands (`terraform destroy`, `docker compose down -v`, force-pushes) without first confirming which environment/folder you're actually in.**
- **Always check CI status before merging** — a red check exists specifically to be looked at, not clicked past.
- **Screenshot or log the output of major steps** — as demonstrated throughout this internship's documentation, having evidence of what actually happened (not just what was supposed to happen) makes debugging and reporting far easier later.

---
*Chrysoptera — Cloud Computing / DevOps Internship — Week 4*
