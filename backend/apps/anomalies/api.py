from datetime import UTC, datetime

from django.shortcuts import get_object_or_404
from ninja import Router

from apps.authentication.jwt_auth import JWTAuth

from .models import AnomalyIncident
from .schemas import AnomalyIncidentOut, AnomalyResolveIn
from .tasks import analyze_cluster_anomalies

router = Router()
auth_required = JWTAuth()


@router.get("/incidents", response=list[AnomalyIncidentOut], auth=auth_required)
def list_incidents(request, status: str | None = None, severity: str | None = None):
    """Retrieve list of detected telemetry anomalies and incident reports."""
    qs = AnomalyIncident.objects.select_related("node").all()
    if status:
        qs = qs.filter(status=status.upper())
    if severity:
        qs = qs.filter(severity=severity.upper())

    out = []
    for inc in qs:
        out.append(
            AnomalyIncidentOut(
                id=inc.id,
                node_id=inc.node.id,
                node_hostname=inc.node.hostname,
                title=inc.title,
                severity=inc.severity,
                status=inc.status,
                metric_type=inc.metric_type,
                detected_value=inc.detected_value,
                expected_baseline=inc.expected_baseline,
                description=inc.description,
                root_cause_summary=inc.root_cause_summary,
                recommended_action=inc.recommended_action,
                detected_at=inc.detected_at,
                resolved_at=inc.resolved_at,
            )
        )
    return out


@router.get("/incidents/{int:incident_id}", response=AnomalyIncidentOut, auth=auth_required)
def get_incident(request, incident_id: int):
    """Get single anomaly incident with full triage recommendations."""
    inc = get_object_or_404(AnomalyIncident.objects.select_related("node"), id=incident_id)
    return AnomalyIncidentOut(
        id=inc.id,
        node_id=inc.node.id,
        node_hostname=inc.node.hostname,
        title=inc.title,
        severity=inc.severity,
        status=inc.status,
        metric_type=inc.metric_type,
        detected_value=inc.detected_value,
        expected_baseline=inc.expected_baseline,
        description=inc.description,
        root_cause_summary=inc.root_cause_summary,
        recommended_action=inc.recommended_action,
        detected_at=inc.detected_at,
        resolved_at=inc.resolved_at,
    )


@router.post("/incidents/{int:incident_id}/resolve", auth=auth_required)
def resolve_incident(request, incident_id: int, payload: AnomalyResolveIn):
    """Mark an active incident as resolved."""
    inc = get_object_or_404(AnomalyIncident, id=incident_id)
    inc.status = AnomalyIncident.Status.RESOLVED
    inc.resolved_at = datetime.now(UTC)
    if payload.resolution_notes:
        inc.description += f"\n[Resolution]: {payload.resolution_notes}"
    inc.save()
    return {"status": "success", "message": f"Incident {inc.id} marked as RESOLVED."}


@router.post("/trigger-analysis", auth=auth_required)
def trigger_analysis(request):
    """Manually dispatch background anomaly evaluation across cluster nodes."""
    result = analyze_cluster_anomalies()
    return {"status": "dispatched", "result": result}
