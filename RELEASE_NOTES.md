# 🚀 Chrona Backend — v3.0 Release Notes

**Date:** 2025-08-04
**Version:** v3.0 (Major Production Release)
**Codename:** *Nimbus*

---

## 📌 Overview

Chrona v3.0 marks a pivotal step forward in performance, responsiveness, and reliability.
With **real-time notifications**, **automated alert handling**, and **bulletproof deployment workflows**, Nimbus brings Chrona closer to a seamless, responsive experience across platforms — while maintaining secure, scalable infrastructure under the hood.

---

## 🎉 What’s New

### Timer Automation & Signal System

* Timers now automatically:

  * Trigger notifications when started or completed.
  * Cancel alerts when paused or reset.
* Built-in **grace period** reduces false or premature alerts.
* Added support for **multi-event scheduling logic**.

### Real-Time Notifications (Web Push)

* Users receive browser alerts instantly when timers complete.
* Notifications work even if the app is closed or in the background.
* Subscriptions are securely stored and cleaned up when expired.

### Background Task Engine

* Long-running tasks (like notification sending) now run asynchronously.
* System performance is improved during high load or multiple concurrent actions.

### Testing & Quality Gates

* All changes now run through automated testing pipelines before release.
* Introduced **test coverage threshold** enforcement (minimum 69%).
* Added tests for key apps: `countdown`, `notifications`, `users`, and `utils`.

### CI/CD Pipeline Upgrades

* **Secrets now injected securely** during build via Azure Key Vault.
* Deployments gated by test success — safer releases.
* Artifacts and coverage reports are uploaded automatically.
* Production and staging flows are clearly separated.

### Infrastructure & DevOps Enhancements

* Full infrastructure managed via **Terraform**:

  * Timer workers can now scale automatically based on queue load.
  * Environment-specific variables are cleanly injected via Azure bindings.
* Refined `celery-worker` module for better task orchestration.
* Continued use of **Poetry** for reliable dependency management.

---

## 🔐 Security & Resilience

* Redis connections now use **TLS (rediss\://)** for secure communication.
* User logout now blacklists access tokens immediately.
* Improved OAuth and session handling for multi-device safety.

---

## 🛑 Breaking Changes

* Manual task triggers and old alert logic have been retired.
* Legacy APIs for notifications are no longer supported.
* Workers now require updated config values for queues and tasks.

---

## ✅ Validation

* All tests passed with enforced thresholds.
* Full backend deployed in staging, load-tested under typical production traffic.
* Observability tested: Prometheus, Grafana, Sentry, and LogDNA all functional.
* Terraform deployment validated on Azure for both backend and task worker services.

---

## 📈 What’s Next (v3.x Series Roadmap)

* **Cross-device sync** for timer state.
* **Analytics dashboards** for usage insights.
* **Shared timers** — create, assign, and collaborate with others.
* **OAuth + Magic Link** login experience.
* **TimescaleDB** event stream for granular timer analytics.

---

Chrona Backend v3.0 *Nimbus* is now **real-time capable, secure by default, and deployable at scale** — laying the foundation for rich user experiences across all platforms.
---
---

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
