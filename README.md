# ⚡ OpsPulse

<p align="center">
  <strong>Modern Full-Stack Cloud Observability & AIOps Telemetry Dashboard</strong>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Django-5.x-092E20?style=for-the-badge&logo=django&logoColor=white" alt="Django" />
  <img src="https://img.shields.io/badge/Django_Ninja-FastAPI_Speed-blue?style=for-the-badge" alt="Django Ninja" />
  <img src="https://img.shields.io/badge/Next.js-15_App_Router-black?style=for-the-badge&logo=next.js&logoColor=white" alt="Next.js" />
  <img src="https://img.shields.io/badge/Tailwind_CSS-v4-38B2AC?style=for-the-badge&logo=tailwind-css&logoColor=white" alt="Tailwind CSS" />
  <img src="https://img.shields.io/badge/shadcn%2Fui-Components-000000?style=for-the-badge" alt="shadcn/ui" />
  <img src="https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge" alt="License" />
</p>

---

## 📖 Overview

**OpsPulse** is a production-grade, open-source cloud telemetry and AIOps platform. It bridges the enterprise-level robustness of **Django 5** with the high performance and ergonomic user experience of **Next.js 15 (React 19 App Router)** and **shadcn/ui**.

Designed for DevOps engineers and modern software teams, OpsPulse ingests real-time metrics, monitors host clusters, runs statistical anomaly detection on background Celery queues, and provides instant, LLM-powered incident diagnostics.

---

## 🏗️ Architecture

```
[ Host Nodes & Cloud Agents ]
              │ (HTTP Telemetry / Logs)
              ▼
+───────────────────────────────────────────────────────────+
|                  OpsPulse Backend (Django 5)              |
|  - Django Ninja (High-speed Async API & OpenAPI Schemas)  |
|  - JWT Authentication & RBAC (Admin / Engineer / Viewer)  |
|  - Celery Worker (Statistical Log & Metric Anomaly Engine)|
|  - PostgreSQL (Primary Storage) + Redis (Cache & Broker)  |
+───────────────────────────────────────────────────────────+
              ▲
              │ REST API & Server-Sent Events (SSE)
              ▼
+───────────────────────────────────────────────────────────+
|                 OpsPulse Frontend (Next.js 15)            |
|  - App Router with React 19 Server Components             |
|  - Tailwind CSS v4 + Semantic shadcn/ui Component Library |
|  - Type-Safe API Client auto-generated from OpenAPI       |
|  - Real-time Telemetry Charts & Log Filtering Engine      |
+───────────────────────────────────────────────────────────+
```

---

## ✨ Key Features

- **⚡ Blazing Fast API with Django Ninja**: Sub-millisecond serialization with automatic OpenAPI 3.0 schema generation.
- **🛡️ Enterprise Authentication**: Custom User model, JWT token rotation, and Role-Based Access Control (RBAC).
- **📊 Real-time Cloud Telemetry**: Ingest host metrics (CPU, Memory, Disk, Network I/O) and structured logs.
- **🤖 AIOps Anomaly Detection**: Statistical Z-score & spike detection computed asynchronously on Celery workers.
- **🎨 Modern Silicon Valley UI**: Fully responsive, accessible, dark/light mode dashboard powered by Tailwind CSS v4 and shadcn/ui.
- **🐳 One-Command Setup**: Entire environment (Backend, Frontend, PostgreSQL, Redis, Celery) launches with a single `docker compose up`.

---

## 🚀 Quickstart Guide

### Option 1: Docker Compose (Recommended)

Run the full stack with zero local dependency headaches:

```bash
# Clone the repository
git clone https://github.com/saha96/OpsPulse.git
cd OpsPulse

# Copy environment template
cp .env.example .env

# Launch all services
docker compose up --build
```

- **Frontend Dashboard**: [http://localhost:3000](http://localhost:3000)
- **Django Ninja API & Swagger Docs**: [http://localhost:8000/api/v1/docs](http://localhost:8000/api/v1/docs)

---

### Option 2: Local Development Setup

#### 1. Backend (Django)
```bash
cd backend
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install -r requirements.txt

# Run migrations (defaults to SQLite if PostgreSQL is not specified)
python manage.py migrate

# Seed dummy telemetry data
python manage.py seed_telemetry

# Start Django development server
python manage.py runserver 0.0.0.0:8000
```

#### 2. Frontend (Next.js)
```bash
cd frontend
npm install
npm run dev
```

---

## 📂 Project Structure

```text
OpsPulse/
├── docker-compose.yml       # Multi-service local deployment
├── .env.example             # Standard environment configuration
├── backend/                 # Django 5 Backend
│   ├── core/                # Settings, ASGI/WSGI, Ninja API Router
│   ├── apps/
│   │   ├── authentication/  # Custom User, JWT tokens, RBAC schemas
│   │   ├── telemetry/       # Node metrics, logs ingestion, live streams
│   │   └── anomalies/       # Detection algorithms, triage tasks
│   ├── Dockerfile
│   └── requirements.txt
└── frontend/                # Next.js 15 Frontend
    ├── src/
    │   ├── app/             # App Router pages and layouts
    │   ├── components/      # shadcn/ui and custom dashboard widgets
    │   ├── lib/             # API clients and utilities
    │   └── types/           # Generated TypeScript definitions
    ├── Dockerfile
    └── package.json
```

---

## 🤝 Contributing

We welcome open-source contributions! Please check out [CONTRIBUTING.md](CONTRIBUTING.md) for coding guidelines, Conventional Commits standards, and pull request procedures.

---

## 📜 License

Distributed under the MIT License. See [LICENSE](LICENSE) for more information.

Maintained with ❤️ by **[Amir Hossein Ahmadi](https://github.com/saha96)**.
