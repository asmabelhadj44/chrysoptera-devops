# W4 — GDPR Data Residency Note

**Task:** GDPR data residency note (written doc)
**Status:** Done
**Context:** Chrysoptera DevOps internship, Week 4 (Security, Docs & Demo)

---

## Why this matters for Chrysoptera specifically

GDPR (General Data Protection Regulation) is EU law governing how personal data is collected, stored, and processed. It applies based on **whose data it is**, not where the company is based — so if any future Chrysoptera solar site belongs to an individual or organization in the EU, GDPR applies regardless of where Chrysoptera itself operates.

## What data Chrysoptera actually handles, and whether GDPR applies

Looking at the current `/readings` data shape (`site_id`, `solar_output_kw`):

| Data currently collected | Personal data under GDPR? |
|---|---|
| `site_id` (a number) | Not personal on its own — but could become personal data if it's ever linkable to an identifiable person (e.g. a homeowner's name in a separate table) |
| `solar_output_kw` (a number) | Not personal data by itself |

**Current honest assessment:** the data shape built so far is **not clearly personal data** in isolation. However, a real solar monitoring product almost certainly *will* eventually store data that identifies real people or households (site owner names, addresses, billing/account info for carbon accounting) — at which point GDPR obligations become directly relevant. This note exists to plan for that point in advance, not because the current MVP already processes personal data.

## Core GDPR principles relevant to this project's future design

1. **Data residency**: Personal data of EU residents should ideally be stored within the EU, or in a location covered by an adequate legal transfer mechanism (e.g. EU-US Data Privacy Framework). This directly affects cloud region choice — the Azure Postgres instance provisioned this week was deployed to **Switzerland North**, which is relevant here: Switzerland has its own adequacy status recognized by the EU, but it is worth explicitly deciding on an EU region (e.g. France Central, Germany West Central where available) once real EU customer data is involved, rather than defaulting to whichever region a student subscription happened to allow.

2. **Data minimization**: Only collect what's actually needed. The current schema (site ID + power output) already follows this principle well — no unnecessary personal fields exist yet, and any future addition (owner name, address) should be evaluated against whether it's truly required.

3. **Right to erasure ("right to be forgotten")**: If personal data is added later, there must be a real technical way to delete a specific person's data on request — not just archive it. This has direct implications for backup design: backups (see this week's backup script) need a retention/deletion policy too, not just the live database.

4. **Encryption in transit and at rest**: Any future production database storing personal data should use TLS for connections and encryption at rest — both of which managed cloud database services (Azure Database for PostgreSQL, AWS RDS) provide by default, which is one more argument for using managed services over a self-hosted database once real data is involved.

## Practical recommendations for Chrysoptera going forward

- When personal data (owner names, contact info, billing details for carbon accounting) is added to the schema, explicitly choose an EU cloud region for any EU customers' data, and document that decision.
- Add a data retention policy alongside the backup strategy — e.g., "raw sensor readings kept for N years, personal account data deleted M days after account closure."
- If Chrysoptera ever processes data for EU users at meaningful scale, a real legal/compliance review is warranted — this document is a technical/architectural starting point, not a substitute for legal advice.

---
*Chrysoptera — Cloud Computing / DevOps Internship — Week 4*
*Note: this document reflects a technical/DevOps perspective on data residency and is not legal advice.*
