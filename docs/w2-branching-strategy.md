# Week 2 — Branching Strategy

**Task:** Branching strategy doc
**Status:** Done
**Context:** Chrysoptera DevOps internship, Week 2 (CI/CD & Containerization)

---

## Chosen strategy: GitHub Flow (simplified trunk-based)

For a project this size — one developer, one repo, a small FastAPI service — a heavyweight strategy like Git Flow (with `develop`, `release`, `hotfix` branches) adds process overhead without adding value. **GitHub Flow** is a better fit: one long-lived branch (`main`) plus short-lived feature branches.

### The rule
`main` is always deployable. Nothing gets pushed to `main` directly except small, low-risk fixes — everything else goes through a feature branch.

## Workflow

1. **Create a branch off `main`** for any new piece of work, named after what it does:
   ```
   git checkout -b feature/w3-terraform-postgres
   ```
   Naming convention: `feature/<short-description>` for new work, `fix/<short-description>` for bug fixes.

2. **Commit as you go** on that branch, with clear messages (as already being done — e.g. "Fix PEP8 spacing issues flagged by flake8").

3. **Push the branch and open a Pull Request** into `main`:
   ```
   git push -u origin feature/w3-terraform-postgres
   ```
   Even solo, opening a PR is useful — it's where the GitHub Actions lint + test workflow runs automatically *before* the code reaches `main`, catching issues early instead of after they've already landed.

4. **Merge once checks pass.** With the CI pipeline from Week 2 in place, a PR can't look "safe" until the lint and test checks both show green.

5. **Delete the branch** after merging to keep the repo tidy.

## Why this fits Chrysoptera specifically

- **Solo/small-team friendly**: no `develop` branch to keep in sync, no release-branch ceremony — appropriate for a 1-person internship project.
- **CI-native**: pairs directly with the GitHub Actions workflow built this week — every PR triggers lint + tests automatically, which is the actual point of having CI.
- **Low overhead, real practice**: still teaches the core professional habit (isolate work, review before merging) without the process cost of Git Flow, which is really meant for projects with scheduled releases and multiple environments.

## Applying it going forward

Not retroactively enforced on the commits already made directly to `main` during Week 1–2 — but from Week 3 onward, new work can optionally start using a feature branch + PR to demonstrate the practice, e.g.:

```
git checkout -b feature/w3-secrets-doc
# ...make changes...
git add .
git commit -m "Add secrets management plan"
git push -u origin feature/w3-secrets-doc
# open PR on GitHub, confirm checks pass, merge
```

---
*Chrysoptera — Cloud Computing / DevOps Internship — Week 2*
