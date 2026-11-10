import pytest
from django.contrib.auth import get_user_model
from ninja.testing import TestClient

from apps.anomalies.models import AnomalyIncident
from apps.telemetry.models import HostNode
from core.api import api

User = get_user_model()


@pytest.fixture
def client():
    """Ninja TestClient fixture."""
    return TestClient(api)


@pytest.fixture
def test_user(db):
    """Create a default active engineer user."""
    user = User.objects.create_user(
        username="testengineer",
        email="engineer@opspulse.local",
        password="ValidPassword123!",
        role=User.Role.ENGINEER,
        department="Site Reliability",
    )
    return user


@pytest.fixture
def auth_headers(client, test_user):
    """Retrieve Authorization Bearer headers for the test user."""
    response = client.post(
        "/auth/login",
        json={"username": "testengineer", "password": "ValidPassword123!"},
    )
    assert response.status_code == 200
    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


@pytest.fixture
def sample_node(db):
    """Create a test host node."""
    return HostNode.objects.create(
        hostname="test-node-01",
        ip_address="192.168.1.50",
        cpu_cores=16,
        total_ram_gb=64.0,
        status=HostNode.Status.ONLINE,
        region="eu-west-1",
    )


@pytest.fixture
def sample_incident(db, sample_node):
    """Create a test anomaly incident."""
    return AnomalyIncident.objects.create(
        node=sample_node,
        title="Simulated CPU Anomaly",
        severity=AnomalyIncident.Severity.HIGH,
        metric_type="CPU",
        detected_value=94.5,
        expected_baseline=35.0,
        description="CPU surge during stress test benchmark.",
        root_cause_summary="Stress testing harness execution.",
        recommended_action="Wait for benchmark completion or terminate runner.",
    )
