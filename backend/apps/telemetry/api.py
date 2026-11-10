from datetime import datetime, timezone, timedelta
from typing import List, Optional
from django.shortcuts import get_object_or_404
from django.db.models import Avg, Count
from ninja import Router, Query
from ninja.errors import HttpError
from apps.authentication.jwt_auth import JWTAuth
from .models import HostNode, MetricPoint, StructuredLog
from .schemas import (
    HostNodeOut,
    MetricPointOut,
    MetricIngestIn,
    LogEntryOut,
    LogIngestIn,
    ClusterOverviewOut,
)

router = Router()
auth_required = JWTAuth()

@router.get("/nodes", response=List[HostNodeOut], auth=auth_required)
def list_nodes(request, status: Optional[str] = None):
    """List all registered host nodes with optional status filter."""
    qs = HostNode.objects.all()
    if status:
        qs = qs.filter(status=status.upper())
    return list(qs)

@router.get("/nodes/{int:node_id}", response=HostNodeOut, auth=auth_required)
def get_node_details(request, node_id: int):
    """Retrieve detailed metadata for a single host node."""
    return get_object_or_404(HostNode, id=node_id)

@router.get("/nodes/{int:node_id}/metrics", response=List[MetricPointOut], auth=auth_required)
def get_node_metrics(request, node_id: int, limit: int = 50):
    """Fetch time-series metric data points for a specific node."""
    node = get_object_or_404(HostNode, id=node_id)
    return list(node.metrics.all()[:min(limit, 200)])

@router.post("/ingest/metrics", auth=None)
def ingest_metrics(request, payload: MetricIngestIn):
    """High-throughput telemetry ingestion endpoint for monitoring agents."""
    node, _ = HostNode.objects.get_or_create(
        hostname=payload.hostname,
        defaults={'ip_address': '127.0.0.1'}
    )
    
    ts = payload.timestamp or datetime.now(timezone.utc)
    point = MetricPoint.objects.create(
        node=node,
        timestamp=ts,
        cpu_usage_percent=payload.cpu_usage_percent,
        memory_usage_percent=payload.memory_usage_percent,
        disk_usage_percent=payload.disk_usage_percent,
        network_rx_mb=payload.network_rx_mb,
        network_tx_mb=payload.network_tx_mb,
    )
    
    # Auto-adjust node status if usage is critically high
    if payload.cpu_usage_percent > 90 or payload.memory_usage_percent > 95:
        node.status = HostNode.Status.DEGRADED
        node.save(update_fields=['status', 'last_heartbeat'])
    else:
        if node.status == HostNode.Status.DEGRADED and payload.cpu_usage_percent < 80:
            node.status = HostNode.Status.ONLINE
            node.save(update_fields=['status', 'last_heartbeat'])
            
    return {"status": "success", "metric_id": point.id}

@router.get("/logs", response=List[LogEntryOut], auth=auth_required)
def list_logs(
    request,
    level: Optional[str] = None,
    service: Optional[str] = None,
    hostname: Optional[str] = None,
    limit: int = 100,
):
    """Search and filter structured system logs."""
    qs = StructuredLog.objects.select_related('node').all()
    if level:
        qs = qs.filter(level=level.upper())
    if service:
        qs = qs.filter(service_name__icontains=service)
    if hostname:
        qs = qs.filter(node__hostname=hostname)
        
    results = []
    for log in qs[:min(limit, 500)]:
        results.append(
            LogEntryOut(
                id=log.id,
                node_hostname=log.node.hostname,
                timestamp=log.timestamp,
                service_name=log.service_name,
                level=log.level,
                message=log.message,
                trace_id=log.trace_id,
                metadata=log.metadata,
            )
        )
    return results

@router.post("/ingest/logs", auth=None)
def ingest_log(request, payload: LogIngestIn):
    """Ingest a structured log event from an application or system daemon."""
    node, _ = HostNode.objects.get_or_create(
        hostname=payload.hostname,
        defaults={'ip_address': '127.0.0.1'}
    )
    ts = payload.timestamp or datetime.now(timezone.utc)
    log = StructuredLog.objects.create(
        node=node,
        timestamp=ts,
        service_name=payload.service_name,
        level=payload.level.upper(),
        message=payload.message,
        trace_id=payload.trace_id,
        metadata=payload.metadata or {},
    )
    return {"status": "success", "log_id": log.id}

@router.get("/overview", response=ClusterOverviewOut, auth=auth_required)
def get_cluster_overview(request):
    """Aggregate high-level health and metric statistics across the cluster."""
    total_nodes = HostNode.objects.count()
    healthy = HostNode.objects.filter(status=HostNode.Status.ONLINE).count()
    degraded = HostNode.objects.filter(status=HostNode.Status.DEGRADED).count()
    offline = HostNode.objects.filter(status=HostNode.Status.OFFLINE).count()
    
    # Calculate average latest metric
    recent_metrics = MetricPoint.objects.filter(
        timestamp__gte=datetime.now(timezone.utc) - timedelta(hours=1)
    ).aggregate(
        avg_cpu=Avg('cpu_usage_percent'),
        avg_mem=Avg('memory_usage_percent')
    )
    
    # Active anomalies
    from apps.anomalies.models import AnomalyIncident
    active_anomalies = AnomalyIncident.objects.filter(status='ACTIVE').count()
    
    logs_count = StructuredLog.objects.filter(
        timestamp__gte=datetime.now(timezone.utc) - timedelta(days=1)
    ).count()

    return ClusterOverviewOut(
        total_nodes=total_nodes,
        healthy_nodes=healthy,
        degraded_nodes=degraded,
        offline_nodes=offline,
        avg_cpu_percent=round(recent_metrics.get('avg_cpu') or 0.0, 1),
        avg_memory_percent=round(recent_metrics.get('avg_mem') or 0.0, 1),
        active_anomalies_count=active_anomalies,
        total_logs_24h=logs_count,
    )
