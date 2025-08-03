# 📦 Chrona Backend — CHANGELOG

## \[3.0.0] – 2025-08-04

### 🧭 Codename: *Nimbus*

---

## ✨ Major Improvements

* **⏱️ Smarter Timers**

  * Timers now auto-detect when they start, pause, or complete.
  * System automatically schedules and cancels alerts based on timer status.
  * Reduces missed or duplicate notifications.

* **🔔 Real-Time Notifications**

  * Instant browser alerts when timers finish — even if the app is in the background.
  * Works across modern devices and browsers.
  * One-click opt-in for users.

* **🔁 Background Task Processing**

  * Heavy tasks now run behind-the-scenes without slowing down the app.
  * Improved reliability for high-traffic and long-running actions.

* **🧪 Quality Checks & Test Coverage**

  * All features now go through automated testing before deployment.
  * Bugs are caught early — leading to fewer app issues and crashes.
  * Minimum quality threshold enforced on every release.

* **🚀 Faster & Safer Deployments**

  * New deployment system ensures updates are faster and more reliable.
  * Staging environments allow features to be tested before going live.
  * Secrets and configuration are securely injected during builds.

---

## 🔐 Security Upgrades

* **Stronger Data Protection**

  * Timer and notification data are now encrypted end-to-end.
  * Secure sessions for all users, with automatic logout for expired tokens.

* **Access Control**

  * Old sessions are blocked once users log out — preventing unauthorized reuse.

---

## ⚠️ Important Changes

* **Legacy timer APIs are now fully retired.**
* **Old manual alert triggers have been removed.**
* **Previous backend structure is no longer supported — services have been modularized.**

---

## ✅ Why This Matters for You

* ✅ Alerts arrive exactly when you need them — even if the app isn’t open.
* ✅ Performance is faster, even with thousands of users online.
* ✅ Better protection of your session and data.
* ✅ Less downtime and more reliable feature updates.

---

## 🔮 What’s Next

* 🧭 **Realtime Multi-device sync** — start a timer on one device, finish on another.
* 📊 **Analytics dashboard** — see how you use your timers and time blocks.
* 🤝 **Shared timers** — collaborate on countdowns with your team or friends.

---

## [2.0.0] - 2025-05-04

### 🚀 Added

- **Project Restructuring**: Adopted service-oriented architecture for scalability and modularity.
- **Logging Microservice**: Introduced FastAPI-based logging service with Redis Streams.
- **Poetry Package Management**: Migrated to Poetry for dependency handling.
- **Observability Stack**: Integrated Prometheus, Grafana, PushGateway, and LogDNA.
- **Countdown v2 Timer API**: Introduced new Django app (`countdown`) with session sync and extension integration.
- **Extension Info API**: Added `/extension-info` endpoint for extension metadata.
- **Security Hardening**:
  - AES-128 encryption for sensitive data.
  - HMAC-SHA256 hashing for lookups.
  - Argon2 password hashing and password validation policies.
- **Reverse Proxy Compatibility**: Added forwarded header support.
- **CORS and Session Management**: Improved cross-origin handling for frontend and extensions.
- **API Payload Standardization**: Implemented camelCase <-> snake_case transformations.
- **Terraform Infrastructure as Code**: Provisioned Azure Redis, Container Apps, and Vault resources.

### 🔧 Changed

- Deprecated direct App Service deployments.
- Deprecated old timer APIs in favor of `/v2/countdown/`.

### 🛑 Breaking

- Legacy project structure is incompatible.
- Old timer API endpoints will be phased out.

### ✅ Validation

- Local testing via Docker Compose.
- Manual API smoke tests.
- Observability and logging tested.
- Terraform validated on Azure.

### 📌 Upcoming (Next Releases)

- CI/CD GitHub Actions integration.
- OAuth completion.
- TimescaleDB event analytics.
- Unit test coverage for countdown v2.

