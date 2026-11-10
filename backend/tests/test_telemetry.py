import pytest

from apps.telemetry.models import HostNode, MetricPoint, StructuredLog


@pytest.mark.django_db
class TestTelemetryAPI:
    def test_list_nodes(self, client, auth_headers, sample_node):
        response = client.get("/telemetry/nodes", headers=auth_headers)
        assert response.status_code == 200
        nodes = response.json()
        assert len(nodes) >= 1
        assert nodes[0]["hostname"] == sample_node.hostname

    def test_ingest_metrics_success(self, client):
        payload = {
            "hostname": "agent-runner-01",
            "cpu_usage_percent": 45.5,
            "memory_usage_percent": 62.0,
            "disk_usage_percent": 50.0,
            "network_rx_mb": 150.2,
            "network_tx_mb": 80.4,
        }
        response = client.post("/telemetry/ingest/metrics", json=payload)
        assert response.status_code == 200
        assert response.json()["status"] == "success"

        node = HostNode.objects.get(hostname="agent-runner-01")
        assert node.status == HostNode.Status.ONLINE
        assert MetricPoint.objects.filter(node=node).count() == 1

    def test_critical_metric_marks_node_degraded(self, client):
        payload = {
            "hostname": "overloaded-worker-01",
            "cpu_usage_percent": 96.5,
            "memory_usage_percent": 88.0,
            "disk_usage_percent": 75.0,
        }
        response = client.post("/telemetry/ingest/metrics", json=payload)
        assert response.status_code == 200

        node = HostNode.objects.get(hostname="overloaded-worker-01")
        assert node.status == HostNode.Status.DEGRADED

    def test_ingest_structured_log(self, client, sample_node):
        payload = {
            "hostname": sample_node.hostname,
            "service_name": "ingress-controller",
            "level": "WARN",
            "message": "Certificate expires in 5 days.",
            "trace_id": "tr-abc12345",
        }
        response = client.post("/telemetry/ingest/logs", json=payload)
        assert response.status_code == 200
        assert response.json()["status"] == "success"

        log = StructuredLog.objects.get(trace_id="tr-abc12345")
        assert log.level == "WARN"
        assert log.service_name == "ingress-controller"

    def test_cluster_overview_metrics(self, client, auth_headers, sample_node):
        response = client.get("/telemetry/overview", headers=auth_headers)
        assert response.status_code == 200
        data = response.json()
        assert data["total_nodes"] >= 1
        assert "avg_cpu_percent" in data
        assert "avg_memory_percent" in data
