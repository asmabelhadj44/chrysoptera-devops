# W4 — Disaster Recovery Plan

**Task:** Disaster recovery plan (written doc)
**Status:** Done
**Context:** Chrysoptera DevOps internship, Week 4 (Security, Docs & Demo)

---

## Purpose

A disaster recovery (DR) plan answers one question in advance, calmly, before anything is actually on fire: **"If we lose X, what exactly do we do?"** Writing this now — while nothing is broken — means a real incident later is a checklist to follow, not a panic to improvise through.

## Scope: what "disaster" means for Chrysoptera at this stage

At Month 1, with no real users/sites onboarded yet, realistic disaster scenarios are narrower than they'd be in full production. This plan covers the three that actually apply to the current stack:

1. **Database loss or corruption** (the Postgres container/instance becomes unavailable or its data is corrupted)
2. **Complete loss of the developer's machine** (laptop failure, since local development is currently the only environment)
3. **Accidental deletion of cloud resources** (e.g. someone runs `terraform destroy` against the wrong environment)

Full-scale scenarios (region-wide cloud outage, DDoS attack, coordinated data breach) are **out of scope at this stage** — they matter once there's real production traffic and users, and would be revisited then.

## Scenario 1: Database loss or corruption

**Impact:** All stored solar readings and carbon-accounting data lost or unreadable.

**Recovery steps:**
1. If running locally: stop the affected container (`docker compose stop db`), remove its volume, and restore from the most recent backup (see the automated backups doc/script from this week).
2. If running on managed cloud Postgres (as provisioned conceptually via Terraform this week): Azure/AWS managed Postgres services support point-in-time restore from automatic backups — this would be the primary recovery path in a real deployment, rather than relying solely on the manual backup script.
3. Verify recovery by re-running the health-check script (`healthcheck.py`) against the restored database to confirm the API can read/write again.

**Recovery Time Objective (RTO):** Under 30 minutes for a local restore from a recent backup file; managed cloud point-in-time restore is typically faster and more reliable once that infrastructure actually exists.

**Recovery Point Objective (RPO):** Depends on backup frequency — see the automated backups doc for the actual interval chosen this week.

## Scenario 2: Complete loss of the developer's machine

**Impact:** Local code, local Docker state, and any un-pushed work would be lost.

**Recovery steps:**
1. All source code is already safe by design: the entire project is a Git repo pushed to GitHub (`github.com/asmabelhadj44/chrysoptera-devops`), so cloning it onto a new machine recovers 100% of committed code, Terraform configs, and documentation instantly.
2. Reinstall the local toolchain (Docker Desktop, Terraform, Python) — the environment setup section from the Week 1 log already documents the exact steps taken, functioning as an unintentional but genuinely useful recovery runbook for this exact scenario.
3. Run `docker compose up` to rebuild the local stack from the checked-in `docker-compose.yml` and `Dockerfile`.

**The actual risk here isn't code loss — it's uncommitted work.** The one mitigation that matters: commit and push frequently, rather than accumulating large uncommitted changes locally.

## Scenario 3: Accidental deletion of cloud resources

**Impact:** A real Azure/AWS resource (like the Postgres server provisioned this week) gets destroyed unintentionally — e.g. running `terraform destroy` in the wrong folder, or against the wrong `.tfvars`.

**Recovery steps:**
1. Because this is Infrastructure as Code, recovery is straightforward *by design*: re-run `terraform apply` with the same configuration and variables to recreate an identical resource.
2. The one thing Terraform **cannot** recover on its own is the *data* that lived inside a destroyed database — this is why Scenario 1's backup strategy is a separate, necessary safeguard, not something IaC replaces.
3. Prevention: naming environments clearly (already done via the `Environment: staging` tag), and treating `terraform destroy` as a command that always requires a manual pause to confirm the correct folder/environment before typing `yes`.

## What this plan deliberately does not cover yet

- Multi-region failover (not applicable — no multi-region deployment exists)
- Formal incident communication plan to end users (no end users yet)
- Automated failover/self-healing (would come with future infrastructure maturity, e.g. Kubernetes health checks from the W1-04 research)

This plan will need a revision once real production infrastructure and real users exist — it currently reflects the actual, honest scale of the project at Month 1.

---
*Chrysoptera — Cloud Computing / DevOps Internship — Week 4*
