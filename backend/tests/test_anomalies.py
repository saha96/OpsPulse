from datetime import UTC, datetime, timedelta

import pytest

from apps.anomalies.engine import compute_z_score, evaluate_node_metrics
from apps.anomalies.models import AnomalyIncident
from apps.telemetry.models import MetricPoint


@pytest.mark.django_db
class TestAnomalyEngineAndAPI:
    def test_compute_z_score_basic(self):
        values = [10.0, 10.0, 10.0, 10.0, 10.0]
        # When variance is zero, z-score should be 0
        assert compute_z_score(values, 10.0) == 0.0

        history = [20.0, 22.0, 19.0, 21.0, 20.0]
        # A value of 50 is heavily elevated
        z = compute_z_score(history, 50.0)
        assert z > 3.0

    def test_evaluate_node_metrics_detects_spike(self, sample_node):
        now = datetime.now(UTC)
        # Create normal historical points
        points = []
        for i in range(10):
            points.append(
                MetricPoint(
                    node=sample_node,
                    timestamp=now - timedelta(minutes=(11 - i) * 5),
                    cpu_usage_percent=30.0,
                    memory_usage_percent=40.0,
                    disk_usage_percent=50.0,
                )
            )
        # Add critical spike point
        points.append(
            MetricPoint(
                node=sample_node,
                timestamp=now,
                cpu_usage_percent=98.0,
                memory_usage_percent=45.0,
                disk_usage_percent=50.0,
            )
        )
        MetricPoint.objects.bulk_create(points)

        incidents = evaluate_node_metrics(sample_node)
        assert len(incidents) == 1
        assert incidents[0].severity == AnomalyIncident.Severity.CRITICAL
        assert "CPU Spike Detected" in incidents[0].title

    def test_list_incidents_api(self, client, auth_headers, sample_incident):
        response = client.get("/anomalies/incidents", headers=auth_headers)
        assert response.status_code == 200
        data = response.json()
        assert len(data) >= 1
        assert data[0]["title"] == sample_incident.title

    def test_resolve_incident_api(self, client, auth_headers, sample_incident):
        payload = {"resolution_notes": "Cluster auto-scaler handled load."}
        response = client.post(
            f"/anomalies/incidents/{sample_incident.id}/resolve",
            json=payload,
            headers=auth_headers,
        )
        assert response.status_code == 200

        sample_incident.refresh_from_db()
        assert sample_incident.status == AnomalyIncident.Status.RESOLVED
        assert "Cluster auto-scaler" in sample_incident.description
