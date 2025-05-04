# 📦 Chrona Backend — CHANGELOG

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

