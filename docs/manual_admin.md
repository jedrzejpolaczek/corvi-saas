# Corvi – Instrukcja administratora

**Instalacja**
```bash
docker compose -f infra/docker-compose.yml up --build
```

**Konfiguracja .env**
- Klucze JWT, adresy S3/MinIO, MLflow, kolejka (RabbitMQ/Redis), tryb Enterprise.

**Tiers & Feature Flags**
- Endpointy `/admin/*` umożliwiają ustawianie planów (Premium/Enterprise), flag, limitów i reset użyć.

**Monitoring**
- Prometheus i Grafana w `infra/`. Podstawowy dashboard JSON w repo.

**Tryb Enterprise**
- `ENTERPRISE_MODE=true`: wyłącza public signup (w UI), SSO (stub), VPC/on‑prem placeholdery.
