# 🚀 Chrona Backend — v2.0 Release Notes

**Date:** 2025-05-12
**Version:** v2.0 (Major Production Release)

---

## 📌 Overview

Chrona backend has reached a new milestone with **Version 2.0**, transforming the architecture for scalability, security, and observability.
This release introduces modular service design, cloud-native deployment readiness, robust observability, and a new countdown timer API to power seamless frontend and extension integrations.

Recent enhancements also stabilize Google OAuth login flows, improve environment handling in CI/CD, and bring further infrastructure flexibility.

---

## 🎉 What’s New

### Backend Architecture and APIs

* Migrated to **modular service-oriented architecture**, designed for microservices readiness.
* Introduced **Countdown v2 API (countdown app)**:

  * Session sync and Chrome extension metadata support.
  * New `/v2/countdown/` endpoints for starting, pausing, and resetting timers.
* Added **Extension Info API** to dynamically provide extension config.

### Logging Microservice (FastAPI)

* Deployed dedicated logging microservice using Redis Streams.
* Supports scalable, decoupled log processing.

### Observability Stack

* Integrated **Prometheus + Grafana** for metrics visualization.
* Configured **PushGateway** for ephemeral job metrics.
* Centralized logging via **LogDNA**.

### Security and Authentication

* AES-128 encryption and HMAC SHA-256 hashing for secure, deterministic data handling.
* Password hashing upgraded to **Argon2** with stricter validation policies.
* Deprecated `django-allauth` in favor of lighter **social-auth-app-django**.
* 🆕 **OAuth flow stabilized** with isolated session handling for secure popup-based Google login.

### CI/CD and Infrastructure

* Introduced **Terraform** IaC for provisioning:

  * Azure Redis
  * Azure Container Apps
  * Vault (secrets)
* 🆕 Enhanced **CI/CD GitHub Actions** workflows to dynamically detect environments from branches/tags.
* 🆕 Added support for **minimum replica scaling** in Terraform deployments.

### Developer Experience

* Migrated to **Poetry** for Python dependency management.
* Implemented camelCase ↔ snake\_case API transformations.
* Improved reverse proxy handling and CORS for cross-origin integrations.
* 🆕 Added reusable PR and release templates to standardize contributions.

---

## 🛑 Breaking Changes

* Legacy project structure deprecated. Use the new modular layout.
* App Service deployment removed — **Azure Container Apps** are now default.
* Legacy timer endpoints deprecated → use `/v2/countdown/`.

---

## ✅ Validation

* Docker-based local environment and API testing completed.
* OAuth login tested in Chrome popup flow with cross-origin sessions.
* Terraform changes deployed to staging and validated.
* Prometheus, Grafana, and logging stack confirmed functional.

---

## 📈 What’s Next (Planned for v2.x Series)

* Complete rollout of GitHub Actions-based CI/CD pipelines.
* OAuth token refresh handling and expanded provider support.
* TimescaleDB integration for historical timer analytics.
* Full unit test coverage and test pipeline integration.

---

Chrona Backend is now **secure, modular, cloud-native, and OAuth-ready** — engineered to support modern productivity workflows and real-time analytics at scale.
