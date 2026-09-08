# W3 — Secrets Management Plan

**Task:** Secrets management plan (written doc)
**Status:** Done
**Context:** Chrysoptera DevOps internship, Week 3 (Infrastructure as Code)

---

## The problem this solves

A "secret" is any value that would cause real harm if it leaked publicly — database passwords, API keys, cloud credentials. The single most common way secrets leak in real projects isn't a sophisticated attack — it's someone accidentally committing them to a public (or even private) Git repo, where they sit in the commit history forever, even if deleted later. This plan defines where each secret in the Chrysoptera stack lives, and specifically, where it must *never* live.

## Current secrets in this project, and how each is handled

| Secret | Where it's used | How it's currently handled |
|---|---|---|
| Postgres DB username/password | `docker-compose.yml` (local), Terraform (`postgres.tf`) | Passed as Terraform variables marked `sensitive = true`, supplied on the command line at apply-time — never typed into the `.tf` file itself |
| Azure account credentials | `az login` / Terraform's Azure provider | Handled by the Azure CLI's own local authentication session (`az login`) — never stored in any project file at all |
| GitHub repo access | Git push/pull | Handled by Git's own credential manager on Windows — not a project secret |

## Rules going forward

1. **Never commit real credentials to Git, ever — not even temporarily.** If a password is typed directly into a `.tf`, `.yml`, or `.env` file "just to test quickly," it's one `git add .` away from being in permanent history. Even deleting it in a later commit doesn't remove it from history — a fresh clone of the repo can still find it.

2. **Use a `.gitignore`'d `.tfvars` file for Terraform secrets**, instead of typing `-var="db_password=..."` on the command line every time (which is fine for quick manual testing, as done in W3, but not for repeated/team use). A `terraform.tfvars` file would hold the real values locally, and `.gitignore` (already used for `.terraform/` and `*.tfstate`) would be extended to also ignore `*.tfvars`.

3. **Use GitHub Actions Secrets for CI/CD credentials.** If a future pipeline step needs to deploy or connect to a real database, credentials would be stored in the repo's **Settings → Secrets and variables → Actions** page (encrypted by GitHub, never visible in logs), and referenced in the workflow YAML as `${{ secrets.DB_PASSWORD }}` rather than typed in plain text.

4. **Use environment variables for local development**, via a `.env` file that is `.gitignore`'d — the FastAPI app would read `DATABASE_URL`, `REDIS_URL`, etc. from environment variables rather than hardcoded values in `main.py`.

5. **Rotate anything that does leak, immediately.** If a secret is ever accidentally committed, the fix isn't just deleting it in a new commit — the credential itself (password, API key) must be changed/rotated at the source, since the old value remains recoverable from Git history regardless.

## Known existing risk (carried over from earlier weeks)

The handoff notes flagged that the very first Git commit accidentally included a 65MB Terraform provider binary — not a secret, but the same category of mistake (something that shouldn't be in Git ending up in history). Worth keeping this plan in mind specifically because that incident already happened once on this repo.

---
*Chrysoptera — Cloud Computing / DevOps Internship — Week 3*
