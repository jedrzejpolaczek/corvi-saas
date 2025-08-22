from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from prometheus_client import make_asgi_app
from starlette.middleware.sessions import SessionMiddleware
from .config import settings
from .metrics_exporter import REQUEST_COUNT, REQUEST_LATENCY
from .routers import auth, users, orgs, projects, datasets, experiments, algorithms, jobs, metrics, artifacts, roi, exports, billing, features, usage, admin, health

app = FastAPI(title="Corvi API", version="1.0.0", root_path=settings.API_ROOT_PATH)

app.add_middleware(CORSMiddleware, allow_origins=settings.CORS_ORIGINS, allow_credentials=True, allow_methods=["*"], allow_headers=["*"])
app.add_middleware(SessionMiddleware, secret_key=settings.SESSION_SECRET)

# Routers
app.include_router(auth.router, prefix="/api")
app.include_router(users.router, prefix="/api")
app.include_router(orgs.router, prefix="/api")
app.include_router(projects.router, prefix="/api")
app.include_router(datasets.router, prefix="/api")
app.include_router(experiments.router, prefix="/api")
app.include_router(algorithms.router, prefix="/api")
app.include_router(jobs.router, prefix="/api")
app.include_router(metrics.router, prefix="/api")
app.include_router(artifacts.router, prefix="/api")
app.include_router(roi.router, prefix="/api")
app.include_router(exports.router, prefix="/api")
app.include_router(billing.router, prefix="/api")
app.include_router(features.router, prefix="/api")
app.include_router(usage.router, prefix="/api")
app.include_router(admin.router, prefix="/api")
app.include_router(health.router, prefix="/api")

# Prometheus
metrics_app = make_asgi_app()
app.mount("/metrics", metrics_app)

@app.get("/")
def root():
    return {"name": "corvi", "status": "ok"}
