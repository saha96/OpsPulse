import random
from datetime import UTC, datetime, timedelta

from django.core.management.base import BaseCommand

from apps.anomalies.models import AnomalyIncident
from apps.authentication.models import User
from apps.telemetry.models import HostNode, MetricPoint, StructuredLog


class Command(BaseCommand):
    help = "Seed mock cluster nodes, telemetry metrics, and logs for development."

    def handle(self, *args, **options):
        self.stdout.write("Seeding OpsPulse development data...")

        # 1. Admin & Engineer User
        admin_user, _ = User.objects.get_or_create(
            username="admin",
            defaults={
                "email": "admin@opspulse.local",
                "role": User.Role.ADMIN,
                "department": "Cloud Architecture",
            },
        )
        admin_user.set_password("admin123")
        admin_user.save()

        # 2. Host Nodes
        sample_nodes = [
            {
                "hostname": "k8s-control-plane-01",
                "ip": "10.0.1.10",
                "cores": 16,
                "ram": 64.0,
                "status": HostNode.Status.ONLINE,
            },
            {
                "hostname": "k8s-worker-node-01",
                "ip": "10.0.1.21",
                "cores": 32,
                "ram": 128.0,
                "status": HostNode.Status.ONLINE,
            },
            {
                "hostname": "k8s-worker-node-02",
                "ip": "10.0.1.22",
                "cores": 32,
                "ram": 128.0,
                "status": HostNode.Status.DEGRADED,
            },
            {
                "hostname": "db-primary-postgres",
                "ip": "10.0.2.15",
                "cores": 16,
                "ram": 64.0,
                "status": HostNode.Status.ONLINE,
            },
            {
                "hostname": "edge-proxy-gw-01",
                "ip": "10.0.3.5",
                "cores": 8,
                "ram": 16.0,
                "status": HostNode.Status.ONLINE,
            },
        ]

        nodes = []
        for n in sample_nodes:
            node, _ = HostNode.objects.get_or_create(
                hostname=n["hostname"],
                defaults={
                    "ip_address": n["ip"],
                    "cpu_cores": n["cores"],
                    "total_ram_gb": n["ram"],
                    "status": n["status"],
                    "region": "us-east-1",
                },
            )
            nodes.append(node)

        # 3. Generate Historical Metric Points (last 2 hours)
        now = datetime.now(UTC)
        self.stdout.write("Generating time-series metrics...")
        for node in nodes:
            is_degraded = node.status == HostNode.Status.DEGRADED
            base_cpu = 75.0 if is_degraded else 35.0
            base_mem = 82.0 if is_degraded else 48.0

            points = []
            for i in range(40):
                ts = now - timedelta(minutes=i * 3)
                points.append(
                    MetricPoint(
                        node=node,
                        timestamp=ts,
                        cpu_usage_percent=min(99.0, max(5.0, base_cpu + random.uniform(-10.0, 15.0))),
                        memory_usage_percent=min(98.0, max(15.0, base_mem + random.uniform(-5.0, 8.0))),
                        disk_usage_percent=random.uniform(40.0, 65.0),
                        network_rx_mb=round(random.uniform(120.0, 540.0), 2),
                        network_tx_mb=round(random.uniform(80.0, 420.0), 2),
                    )
                )
            MetricPoint.objects.bulk_create(points)

        # 4. Generate Structured Logs
        services = ["api-gateway", "auth-service", "k8s-kubelet", "postgres-pool", "celery-worker"]
        log_messages = [
            ("INFO", "Successfully refreshed OAuth token cache."),
            ("INFO", "Pod readiness check passed (HTTP 200)."),
            ("WARN", "Slow query detected: query duration 420ms exceeds 200ms threshold."),
            ("ERROR", "Connection pool timeout waiting for database socket."),
            ("INFO", "TLS handshake completed with ingress load balancer."),
            ("WARN", "Disk space watermark reached 80% on /var/log volume."),
        ]

        logs = []
        for _ in range(60):
            node = random.choice(nodes)
            level, msg = random.choice(log_messages)
            logs.append(
                StructuredLog(
                    node=node,
                    timestamp=now - timedelta(minutes=random.randint(1, 180)),
                    service_name=random.choice(services),
                    level=level,
                    message=msg,
                    trace_id=f"trace-{random.randint(100000, 999999)}",
                    metadata={"cluster": "production-us-east", "env": "prod"},
                )
            )
        StructuredLog.objects.bulk_create(logs)

        # 5. Seed Anomaly Incident
        degraded_node = next((n for n in nodes if n.status == HostNode.Status.DEGRADED), nodes[0])
        AnomalyIncident.objects.get_or_create(
            node=degraded_node,
            title="Sustained High CPU Load on Worker Node",
            defaults={
                "severity": AnomalyIncident.Severity.HIGH,
                "status": AnomalyIncident.Status.ACTIVE,
                "metric_type": "CPU",
                "detected_value": 88.4,
                "expected_baseline": 42.0,
                "description": "Worker node CPU sustained above 85% for 45 consecutive minutes.",
                "root_cause_summary": "High thread contention in container image transcoding service.",
                "recommended_action": "Scale horizontal pod replica count from 3 to 6 or restart hung worker pods.",
            },
        )

        self.stdout.write(self.style.SUCCESS("OpsPulse demo data seeded successfully!"))
