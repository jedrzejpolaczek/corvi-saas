# Corvi – SaaS HPO (Low‑Code)

**Quick Start**
```bash
cp .env.sample .env
docker compose -f infra/docker-compose.yml up --build
# open http://localhost (frontend) and http://localhost:8000/docs (API)
```
**Demo login**: `docker compose -f infra/docker-compose.yml exec api python -m scripts.cli seed_demo`
