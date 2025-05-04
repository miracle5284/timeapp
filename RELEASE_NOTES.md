# 🚀 Chrona Backend — v2.0 Release Notes

**Date:** 2025-05-04  
**Version:** v2.0 (Major Production Release)

---

## 📌 Overview

Chrona backend has reached a new milestone with **Version 2.0**, which transforms the architecture for scalability, security, and observability.  
This release introduces modular service design, cloud-native deployment readiness, robust observability, and a new countdown timer API to power seamless frontend and extension integrations.

---

## 🎉 What’s New

### Backend Architecture and APIs
- Migrated to **modular service-oriented architecture**, designed for microservices readiness.
- Introduced **Countdown v2 API (countdown app)**:
  - Session sync and Chrome extension metadata support.
  - New `/v2/countdown/` endpoints for starting, pausing, and resetting timers.
- Added **Extension Info API** to dynamically provide extension config.

### Logging Microservice (FastAPI)
- Deployed dedicated logging microservice using Redis Streams.
- Supports scalable, decoupled log processing.

### Observability Stack
- Integrated **Prometheus + Grafana** for metrics visualization.
- Configured **PushGateway** for ephemeral job metrics.
- Centralized logging via **LogDNA**.

### Security and Encryption
- AES-128 encryption and HMAC SHA-256 hashing for secure and deterministic data handling.
- Password hashing upgraded to **Argon2** with stricter validation policies.
- Deprecated `django-allauth` in favor of lighter **social-auth-app-django**.

### Infrastructure as Code (Terraform + Azure)
- Introduced **Terraform** IaC for backend infrastructure provisioning:
  - Azure Redis
  - Azure Container Apps
  - Vault (secrets)

### Developer Experience
- Migrated to **Poetry** for Python dependency management.
- Implemented API payload standardization: camelCase <-> snake_case transformations.
- Improved reverse proxy handling and CORS for cross-origin integrations.

---

## 🛑 Breaking Changes

- Old project structure deprecated. Use new service-oriented layout.
- App Service deployments deprecated — Container Apps are now default.
- `/set_timer`, `/pause_timer`, `/reset_timer` endpoints are deprecated → use `/v2/countdown/`.

---

## ✅ Validation

- Full local environment testing (Docker Compose, Poetry).
- Countdown APIs manually tested and validated.
- Logging, Prometheus, Grafana, and LogDNA validated.
- Terraform IaC provisioned and tested against Azure.

---

## 📈 What’s Next (Planned for v2.x series)

- GitHub Actions-based CI/CD workflows.
- Finalization of OAuth login flows.
- TimescaleDB integration for timer analytics.
- Full unit test coverage and improved test pipelines.

---

Chrona Backend is now **cloud-native, secure, observable, and scalable** → ready to support advanced timer and extension workloads at production scale.