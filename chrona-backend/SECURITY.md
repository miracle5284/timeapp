---

# Chrona Privacy & Data Protection Policy

**Effective Date:** [April 25, 2025]  
**Maintainer:** BluePrime  
**Project:** Chrona – AI Time Companion Assistant (Backend)  
**License:** [Chrona Source-Available License](./LICENSE.md)

---

## 1. Introduction

Chrona is a secure, source-available backend system developed to demonstrate privacy-first architecture, real-time observability, and scalable encrypted user models.

This policy outlines how Chrona processes, protects, and structures user data within its system architecture. This document serves as a formal statement of privacy intent and compliance within the scope of a publicly viewable—but non-usable—codebase.

---

## 2. Data Principles

Chrona is governed by the following **core principles**:

- **Data Minimization**: Only required data fields are modeled (e.g., email, name, timestamps).
- **Encryption by Default**: All personally identifiable information (PII) is encrypted at rest.
- **Searchable Security**: Secure field lookups are enabled using deterministic HMAC.
- **Auditability**: Logging and metrics systems track access and events for review.

---

## 3. What Data Is Handled?

> Chrona is a **codebase only**. It does not collect or transmit real user data unless instantiated.

If deployed, the following fields may be used in the system:
- `email`, `first_name`, `last_name` — all encrypted at rest
- Timestamps (e.g., login, creation)
- OAuth identity tokens (read-only and ephemeral during login)

All sensitive data is encrypted using **AES-256 symmetric encryption** and protected using **SHA-256 HMAC** for lookup support.

---

## 4. Data Protection Methods

Chrona enforces a strict **data protection-by-design** approach:

| Category            | Protection Mechanism                                      |
|---------------------|------------------------------------------------------------|
| **At-Rest Encryption**  | `cryptography.Fernet` (AES-256) per field                 |
| **Field Lookup**        | SHA-256 HMAC with private app key                        |
| **OAuth Tokens**        | Temporarily held in memory only                          |
| **Logs**                | Sent to Redis, then consumed and forwarded securely       |
| **Error Reporting**     | Errors (if enabled) sent to Sentry via authenticated SDK |
| **Metrics**             | Scraped by Prometheus, anonymous by default              |

---

## 5. GDPR, HIPAA & Global Compliance

Chrona aligns with best practices defined by:

- **GDPR** – Encrypted PII, pseudonymized search, minimal data retention
- **HIPAA** – Encrypted identifiers, secure access control principles
- **CCPA** – Right-to-forget and minimal personal traceability
- **NIST 800-63B** – HMAC for safe identity lookups without disclosure

Chrona never stores plaintext sensitive data, and all access patterns are designed to be **constant-time and tamper-evident**.

---

## 6. Logs and Monitoring

Chrona uses a dedicated **FastAPI Logging Service** to:

- Consume logs from a Redis stream
- Forward logs to **LogDNA** (aggregated storage)
- Send error-level records to **Sentry** for diagnostics (optional)

No PII is logged unless explicitly anonymized or whitelisted. Logs are filtered for sensitive values before transmission.

Metrics are exposed via `/metrics` endpoints and include operational stats only — never personal data.

---

## 7. Contribution and User Data

This project does **not accept contributions** at this time.  
No third-party submissions, uploads, or data entries are supported.  
This ensures full control of the codebase and eliminates unintended data risk.

---

## 8. Deployment Warning

While Chrona is made public under a source-available license, it is not production-deployable.  
Any unauthorized deployment violates the license and this privacy agreement.

---

## 9. Future Policy Updates

This policy may be revised in the future as Chrona evolves.  
No backward commitments are made to prior reviewers or forks.

---

## 10. Contact

For privacy-related inquiries or questions about this document:  
**Email:** [Insert Contact]  
**Project Maintainer:** BluePrime

---
