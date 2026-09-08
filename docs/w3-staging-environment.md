# W3 — Staging Environment Plan

**Task:** Staging environment doc (written doc)
**Status:** Done
**Context:** Chrysoptera DevOps internship, Week 3 (Infrastructure as Code)

---

## What "staging" means here

A staging environment is a copy of the production setup used to test changes safely before they reach real users — same stack, same configuration shape, but isolated data and no real consequences if something breaks. Right now, Chrysoptera effectively has one environment: local development on one laptop. This doc defines what a proper local → staging → production progression would look like.

## The three environments

| Environment | Where it runs | Purpose | Status |
|---|---|---|---|
| **Local** | Docker Compose on a developer's own machine | Day-to-day development and quick testing | ✅ Exists (W1-03) |
| **Staging** | Cloud-hosted, isolated from production | Test changes against something closer to real infrastructure before it matters | 📝 Planned (this doc) |
| **Production** | Cloud-hosted, real users | Actually serving the 100+ solar sites | Not yet applicable — no real users/sites onboarded yet |

## What changes between Local and Staging

| Aspect | Local (current) | Staging (planned) |
|---|---|---|
| Database | Postgres container via Docker Compose | Managed Postgres (e.g. the Azure Flexible Server config from this week, tagged `Environment: staging` — already built this way) |
| Secrets | Plaintext in local `.env`/terminal | GitHub Actions Secrets / Azure Key Vault (see Secrets Management Plan) |
| Access | `localhost` only | Reachable via a real (but non-public/limited) URL, firewalled to known IPs |
| Data | Fake/sample readings | Realistic but non-production sample data — never real customer data |
| Deploy trigger | Manual (`docker compose up`) | Automated, via the GitHub Actions pipeline built in Week 2, triggered on merge to `main` |

## Why staging matters even at this small scale

The CI pipeline from Week 2 already catches style and logic errors before merge (lint + tests). Staging catches a different category of problem: things that only break in something *resembling* real infrastructure — a database connection string that works locally but not against a real managed database, a firewall rule that's too strict, a config value that was hardcoded to `localhost`. Skipping straight from a laptop to production is how those issues get discovered by real users instead of by the developer.

## Practical plan for Chrysoptera going forward

1. The Terraform config from this week already tags its resources `Environment: staging` — this was intentional, not incidental. When (or if) a real production deployment happens later, it would use a *separate* Terraform configuration (or separate variable values — different resource names, `Environment: production` tag) rather than reusing the staging resources directly.
2. The GitHub Actions workflow (`lint.yml`) could later be extended with a `deploy-staging` job that runs `terraform apply` automatically against the staging config whenever code is merged to `main` — turning today's manual `terraform apply` (run by hand this week) into a fully automated step.
3. Staging should always use different credentials than any future production environment, so a staging leak can never expose real production access.

## Current limitation, stated honestly

No actual staging deployment is being kept running continuously (the Postgres server built this week was deployed, verified, and torn down via `terraform destroy` to control cost on a student cloud account) — this doc describes the intended shape of a staging environment rather than a permanently running one, which is a reasonable trade-off given the current lack of a dedicated cloud budget.

---
*Chrysoptera — Cloud Computing / DevOps Internship — Week 3*
