<!-- PROJECT SHIELDS -->
[![CI status][ci-status-shield]](https://github.com/ORGANIZATION/REPO/actions)

# Project data

Project name: Corvi

Application name: Corvi SaaS

Additional names: Corvi

Software version: 0.0.1

Repository Purpose: AI-driven experiment management and optimization platform.

# Table of Contents
1. [Project Data](#project-data)
2. [Project Task Board](#project-task-board)
3. [Technical Details](#technical-details)
   - [Environment](#environment)
   - [File Structure](#file-structure)
   - [Required Tools](#required-tools)
   - [Build Procedure](#build-procedure)
4. [Usage](#usage)
5. [Testing Information](#testing-information)
6. [Other Important Information](#other-important-information)
   - [Coding standards](#coding-standards)
   - [Knowledge base](#knowledge-base)
   - [Contribution Guidelines](#contribution-guidelines)
   - [Versioning Convention](#versioning-convention)
   - [FAQs/Troubleshooting](#faqstroubleshooting)
   - [License](#license)
7. [Contact Information](#contact-information)
8. [Acknowledgments](#acknowledgments)
9. [Screenshots/Media](#screenshotmedia)
10. [Release History](#release-history)

# Project task board

Project task board: WIP

# Technical details

Corvi is built using Python (FastAPI, SQLAlchemy), React (Vite), Docker, and PostgreSQL.

## Environment

- Dockerized microservices
- Recommended OS: Windows 10/11, Linux, macOS
- Database: PostgreSQL
- Other services: Redis, RabbitMQ, MinIO, Grafana, Prometheus

## File structure

```
├── corvi_api/                              # Backend API (FastAPI)
│   ├── alembic/                            # Database migrations (Alembic)
│   │   ├── env.py                          # Alembic environment config
│   │   └── versions/                       # Migration scripts
│   ├── app/                                # DB logic
│   │   └── db.py                           # Database session and engine
│   ├── models/                             # SQLAlchemy models
│   │   ├── apikey.py                       # API key model
│   │   ├── artifact.py                     # Artifact model
│   │   ├── audit.py                        # Audit log model
│   │   ├── base.py                         # Base model
│   │   ├── dataset.py                      # Dataset model
│   │   ├── experiment.py                   # Experiment model
│   │   ├── job.py                          # Job model
│   │   ├── metric.py                       # Metric model
│   │   ├── project.py                      # Project model
│   │   ├── roi.py                          # ROI model
│   │   ├── subscription.py                 # Subscription and quota models
│   │   └── user.py                         # User, Org, Membership models
│   ├── routers/                            # FastAPI routers
│   │   ├── admin.py                        # Admin endpoints
│   │   ├── algorithms.py                   # Algorithms endpoints
│   │   ├── artifacts.py                    # Artifacts endpoints
│   │   ├── auth.py                         # Authentication endpoints
│   │   ├── billing.py                      # Billing endpoints
│   │   ├── datasets.py                     # Dataset endpoints
│   │   ├── experiments.py                  # Experiment endpoints
│   │   ├── exports.py                      # Export endpoints
│   │   ├── features.py                     # Feature gating endpoints
│   │   ├── health.py                       # Health check endpoint
│   │   ├── jobs.py                         # Job endpoints
│   │   ├── metrics.py                      # Metrics endpoints
│   │   ├── orgs.py                         # Organization endpoints
│   │   ├── projects.py                     # Project endpoints
│   │   ├── roi.py                          # ROI endpoints
│   │   ├── usage.py                        # Usage endpoints
│   │   └── users.py                        # User endpoints
│   ├── schemas/                            # Pydantic schemas
│   │   ├── admin.py                        # Admin schemas
│   │   ├── artifact.py                     # Artifact schemas
│   │   ├── auth.py                         # Auth schemas
│   │   ├── common.py                       # Common schemas
│   │   ├── dataset.py                      # Dataset schemas
│   │   ├── experiment.py                   # Experiment schemas
│   │   ├── metric.py                       # Metric schemas
│   │   ├── org.py                          # Organization schemas
│   │   ├── project.py                      # Project schemas
│   │   ├── roi.py                          # ROI schemas
│   │   └── user.py                         # User schemas
│   ├── alembic.ini                         # Alembic config file
│   ├── app.py                              # FastAPI app entrypoint
│   ├── config.py                           # App configuration
│   ├── db.py                               # Database session and engine
│   ├── Dockerfile                          # Backend Dockerfile
│   ├── feature_gating.py                   # Feature gating logic
│   ├── metrics_exporter.py                 # Prometheus metrics exporter
│   ├── mlflow_sync.py                      # MLflow sync logic
│   ├── openapi_client_gen.sh               # OpenAPI client generator
│   ├── poetry.lock                         # Poetry lock file
│   ├── pyproject.toml                      # Poetry project file
│   ├── rbac.py                             # Role-based access control
│   ├── requirements.txt                    # Python dependencies
│   ├── s3.py                               # S3 storage logic
│   ├── security.py                         # Security helpers
│   └── websocket_manager.py                # WebSocket manager
│
├── corvi_frontend/                         # Frontend (React + Vite)
│   ├── src/                                # Frontend source code
│   │   ├── App.tsx                         # Main React component
│   │   ├── main.tsx                        # Entry point
│   │   ├── api/
│   │   │   └── client.ts                   # API client
│   │   ├── components/
│   │   │   ├── DataUpload.tsx              # Data upload component
│   │   │   └── JobStatus.tsx               # Job status component
│   │   └── pages/
│   │       └── Experiments.tsx             # Experiments page
│   ├── index.html                          # Main HTML file
│   ├── package.json                        # Frontend dependencies
│   ├── postcss.config.cjs                  # PostCSS config
│   ├── README.md                           # Frontend README
│   ├── tailwind.config.cjs                 # Tailwind CSS config
│   ├── tsconfig.json                       # TypeScript config
│   ├── vite.config.ts                      # Vite config
│   └── dist/                               # Production build output
│       ├── index.html                      # Built HTML file
│       └── assets/                         # Static assets
│
├── corvi_worker/                           # Worker service
│   ├── algorithms/                         # Optimization algorithms
│   │   ├── grid_search.py                  # Grid search algorithm
│   │   ├── random_search.py                # Random search algorithm
│   │   └── corvi_opt/
│   │       ├── bo.py                       # Bayesian optimization
│   │       └── pruning.py                  # Pruning logic
│   ├── __init__.py                         # Worker package init
│   ├── config.py                           # Worker config
│   ├── Dockerfile                          # Worker Dockerfile
│   ├── poetry.lock                         # Poetry lock file
│   ├── pyproject.toml                      # Poetry project file
│   ├── queue.py                            # Task queue logic
│   └── runner.py                           # Worker runner
│
├── corvi_dashboard/                        # Dashboard service
│   ├── app.py                              # Dashboard entrypoint
│   ├── requirements.txt                    # Dashboard dependencies
│   └── templates/
│       ├── base.html                       # Base template
│       └── export_pdf.html                 # PDF export template
│
├── corvi_sdk/                              # Python Software Development Kit (SDK)
│   ├── adapters/
│   │   ├── sklearn_adapter.py              # Scikit-learn adapter
│   │   ├── tf_adapter.py                   # TensorFlow adapter
│   │   └── torch_adapter.py                # PyTorch adapter
│   ├── __init__.py                         # SDK package init
│   ├── client.py                           # SDK client
│   ├── pyproject.toml                      # Poetry project file
│   └── study.py                            # Study logic
│
├── infra/                                  # Infrastructure (Docker, Nginx, configs)
│   ├── docker-compose.yml                  # Main compose file
│   ├── Dockerfile.api                      # Backend Dockerfile
│   ├── Dockerfile.dashboard                # Dashboard Dockerfile
│   ├── Dockerfile.frontend                 # Frontend Dockerfile
│   ├── Dockerfile.worker                   # Worker Dockerfile
│   ├── nginx.conf                          # Nginx config
│   ├── prometheus.yml                      # Prometheus config
│   ├── docker/
│   │   └── entrypoint.sh                   # Entrypoint script
│   └── grafana/
│       └── dashboards/
│           └── corvi_dashboard.json        # Grafana dashboard
│
├── docs/                                   # Documentation
│   ├── manual_admin.md                     # Admin manual
│   ├── manual_user.md                      # User manual
│   ├── README.md                           # Docs README
│   └── help_center/
│       ├── custom_models.md                # Custom models help
│       ├── importing_data.md               # Data import help
│       ├── interpreting_kpi_roi.md         # KPI/ROI interpretation
│       ├── plan_limitations.md             # Plan limitations
│       └── upload_errors.md                # Upload errors help
│
├── scripts/                                # CLI scripts
│   └── cli.py                              # Command-line interface
│
├── tests/                                  # Automated tests
│   ├── algorithms/
│   │   ├── test_corvi_opt.py               # Tests for corvi_opt
│   │   └── test_grid_random.py             # Tests for grid/random search
│   └── backend/
│       ├── conftest.py                     # Pytest config
│       ├── test_auth.py                    # Auth tests
│       ├── test_feature_gating.py          # Feature gating tests
│       └── test_upload_and_experiment.py   # Upload/experiment tests
│
├── .env.sample                             # Sample environment variables
├── README.md                               # Main project README
└── README-template.md                      # Project README template
```

## Required tools

- Docker & Docker Compose
- Node.js (v18+ for frontend development)
- Python (v3.11+ for backend/worker/sdk)
- Git

## Build procedure

1. Copy environment file:
   ```powershell
   Copy-Item .env.sample .env
   ```
2. Start all services:
   ```powershell
   docker compose -f infra/docker-compose.yml up -d --build
   ```
3. Open the application in your browser:  
   [http://localhost](http://localhost)

# Usage

After starting the application:
- Register a user.
- Upload data, select a model, run experiments, analyze results, export reports.

# Testing Information

Run tests with:
```powershell
docker compose -f infra/docker-compose.yml exec api pytest
```
or locally in the `tests/` directory.

# Other important informations

## Coding standards
Coding standard: [Google Python Style Guide](https://google.github.io/styleguide/pyguide.html)

## Knowledge base
- All API keys and sensitive data are stored in environment variables.
- User documentation is in the `docs/` directory.

## Contribution Guidelines
WIP

## Versioning convention
We use [semver.org](https://semver.org/) for versioning.

## FAQs/Troubleshooting
- If the frontend does not work: check nginx and frontend logs.
- If you cannot log in: register a user via `/api/auth/register`.
- If the database does not work: check if the postgres container is running.

## License
WIP

## Contact Information
WIP

## Acknowledgments
WIP

## Screenshots/Media
WIP

# Release history
- v0.0.1: Initial launch

<!-- MARKDOWN LINKS & IMAGES -->
[ci-status-shield]: https://github.com/ORGANIZATION/REPO/actions/workflows/main.yml/badge.svg?branch=main