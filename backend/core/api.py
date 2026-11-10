"""
Main Django Ninja API Router for OpsPulse.
"""

from ninja import NinjaAPI

from apps.anomalies.api import router as anomalies_router
from apps.authentication.api import router as auth_router
from apps.telemetry.api import router as telemetry_router

api = NinjaAPI(
    title="OpsPulse Telemetry & AIOps API",
    version="1.0.0",
    description="High-performance cloud observability and AIOps anomaly detection API.",
    docs_url="/docs",
    openapi_url="/openapi.json",
)

# Mount sub-routers
api.add_router("/auth", auth_router, tags=["Authentication & Users"])
api.add_router("/telemetry", telemetry_router, tags=["Telemetry & Monitoring"])
api.add_router("/anomalies", anomalies_router, tags=["AIOps & Anomaly Detection"])


@api.get("/health", tags=["System"])
def health_check(request):
    """Basic healthcheck endpoint for orchestration probes."""
    return {
        "status": "healthy",
        "service": "OpsPulse Backend",
        "version": "1.0.0",
    }
