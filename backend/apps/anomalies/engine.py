import math
from datetime import UTC, datetime, timedelta

from apps.telemetry.models import HostNode, MetricPoint

from .models import AnomalyIncident


def compute_z_score(values: list[float], current: float) -> float:
    """Compute standard Z-score for deviation from mean."""
    if not values or len(values) < 3:
        return 0.0
    mean = sum(values) / len(values)
    variance = sum((x - mean) ** 2 for x in values) / len(values)
    std_dev = math.sqrt(variance)
    if std_dev == 0.0:
        return 0.0
    return (current - mean) / std_dev


def evaluate_node_metrics(node: HostNode) -> list[AnomalyIncident]:
    """Analyze recent metrics for a node and generate incident records if abnormal."""
    now = datetime.now(UTC)
    recent_points = list(
        MetricPoint.objects.filter(node=node, timestamp__gte=now - timedelta(hours=2)).order_by("timestamp")
    )

    if len(recent_points) < 5:
        return []

    created_incidents = []
    latest = recent_points[-1]
    history_cpu = [p.cpu_usage_percent for p in recent_points[:-1]]
    history_mem = [p.memory_usage_percent for p in recent_points[:-1]]

    # 1. CPU Spike Analysis
    cpu_z = compute_z_score(history_cpu, latest.cpu_usage_percent)
    avg_cpu = sum(history_cpu) / len(history_cpu)

    if (latest.cpu_usage_percent > 85.0 and cpu_z > 2.0) or latest.cpu_usage_percent > 95.0:
        # Check if already active incident exists
        existing = AnomalyIncident.objects.filter(
            node=node, metric_type="CPU", status=AnomalyIncident.Status.ACTIVE
        ).first()

        if not existing:
            severity = (
                AnomalyIncident.Severity.CRITICAL if latest.cpu_usage_percent > 95.0 else AnomalyIncident.Severity.HIGH
            )
            inc = AnomalyIncident.objects.create(
                node=node,
                title=f"CPU Spike Detected ({latest.cpu_usage_percent:.1f}%)",
                severity=severity,
                metric_type="CPU",
                detected_value=latest.cpu_usage_percent,
                expected_baseline=round(avg_cpu, 1),
                description=f"Host CPU utilization jumped to {latest.cpu_usage_percent:.1f}%, exceeding 2-hour baseline of {avg_cpu:.1f}%.",
                root_cause_summary="Potential CPU-bound runaway thread, crypto-mining loop, or unindexed database table scan.",
                recommended_action=f"Execute `top -b -n 1 -o %CPU | head -n 15` on {node.hostname} and inspect worker process threads.",
            )
            created_incidents.append(inc)

    # 2. Memory Spike Analysis
    mem_z = compute_z_score(history_mem, latest.memory_usage_percent)
    avg_mem = sum(history_mem) / len(history_mem)
    if latest.memory_usage_percent > 90.0 and (mem_z > 1.8 or latest.memory_usage_percent > 96.0):
        existing = AnomalyIncident.objects.filter(
            node=node, metric_type="MEMORY", status=AnomalyIncident.Status.ACTIVE
        ).first()

        if not existing:
            inc = AnomalyIncident.objects.create(
                node=node,
                title=f"Memory Exhaustion Risk ({latest.memory_usage_percent:.1f}%)",
                severity=AnomalyIncident.Severity.HIGH,
                metric_type="MEMORY",
                detected_value=latest.memory_usage_percent,
                expected_baseline=round(avg_mem, 1),
                description=f"Available memory depleted to critical levels. Baseline was {avg_mem:.1f}%.",
                root_cause_summary="Memory leak in application container or Redis eviction buffer saturation.",
                recommended_action=f"Inspect memory consumers with `ps aux --sort=-%mem | head -n 10` on {node.hostname}.",
            )
            created_incidents.append(inc)

    return created_incidents
