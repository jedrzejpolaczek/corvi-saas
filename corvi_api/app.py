from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from prometheus_client import make_asgi_app
from starlette.middleware.sessions import SessionMiddleware

# Complete the absolute imports:
from config import settings
from metrics_exporter import REQUEST_COUNT, REQUEST_LATENCY
from routers import auth, users, orgs, projects, datasets, experiments, algorithms, jobs, metrics, artifacts, roi, exports, billing, features, usage, admin, health

app = FastAPI(title="Corvi API", version="1.0.0", root_path=settings.API_ROOT_PATH)

@app.get("/")
async def root():
    return {"message": "Corvi API is running", "environment": settings.ENVIRONMENT if hasattr(settings, 'ENVIRONMENT') else "unknown"}

@app.get("/health")
async def health():
    return {"status": "healthy"}

app.add_middleware(CORSMiddleware, allow_origins=settings.CORS_ORIGINS, allow_credentials=True, allow_methods=["*"], allow_headers=["*"])
app.add_middleware(SessionMiddleware, secret_key=settings.SESSION_SECRET)

# Include all routers
app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(users.router, prefix="/users", tags=["users"])
app.include_router(orgs.router, prefix="/orgs", tags=["orgs"])
app.include_router(projects.router, prefix="/projects", tags=["projects"])
app.include_router(datasets.router, prefix="/datasets", tags=["datasets"])
app.include_router(experiments.router, prefix="/experiments", tags=["experiments"])
app.include_router(algorithms.router, prefix="/algorithms", tags=["algorithms"])
app.include_router(jobs.router, prefix="/jobs", tags=["jobs"])
app.include_router(metrics.router, prefix="/metrics", tags=["metrics"])
app.include_router(artifacts.router, prefix="/artifacts", tags=["artifacts"])
app.include_router(roi.router, prefix="/roi", tags=["roi"])
app.include_router(exports.router, prefix="/exports", tags=["exports"])
app.include_router(billing.router, prefix="/billing", tags=["billing"])
app.include_router(features.router, prefix="/features", tags=["features"])
app.include_router(usage.router, prefix="/usage", tags=["usage"])
app.include_router(admin.router, prefix="/admin", tags=["admin"])
app.include_router(health.router, prefix="/health", tags=["health"])

# Add Prometheus metrics
metrics_app = make_asgi_app()
app.mount("/metrics", metrics_app)

@app.middleware("http")
async def add_process_time_header(request, call_next):
    import time
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    REQUEST_COUNT.inc()
    REQUEST_LATENCY.observe(process_time)
    return response