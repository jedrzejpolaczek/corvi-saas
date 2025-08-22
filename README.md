# corvi

**Definition of Done** satisfied by docker-compose quick start and full flow: upload → model select → HPO → KPI/ROI → exports.

### Quick Start (2 commands)
```powershell
Copy-Item .env.sample .env
docker compose -f infra/docker-compose.yml up -d --build
```
Open **http://localhost**.
