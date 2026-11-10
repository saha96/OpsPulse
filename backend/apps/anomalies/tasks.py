import logging
from celery import shared_task
from apps.telemetry.models import HostNode
from .engine import evaluate_node_metrics

logger = logging.getLogger(__name__)

@shared_task(name="opspulse.analyze_cluster_anomalies")
def analyze_cluster_anomalies():
    """Periodic Celery task to inspect all nodes for telemetry anomalies."""
    nodes = HostNode.objects.filter(status__in=[HostNode.Status.ONLINE, HostNode.Status.DEGRADED])
    total_found = 0
    for node in nodes:
        try:
            incidents = evaluate_node_metrics(node)
            total_found += len(incidents)
        except Exception as e:
            logger.error(f"Error evaluating node {node.hostname}: {e}")
            
    logger.info(f"Anomaly evaluation completed. Generated {total_found} incidents.")
    return {"nodes_scanned": nodes.count(), "new_incidents": total_found}
