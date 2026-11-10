from django.db import models

from apps.telemetry.models import HostNode


class AnomalyIncident(models.Model):
    class Severity(models.TextChoices):
        LOW = "LOW", "Low"
        MEDIUM = "MEDIUM", "Medium"
        HIGH = "HIGH", "High"
        CRITICAL = "CRITICAL", "Critical"

    class Status(models.TextChoices):
        ACTIVE = "ACTIVE", "Active / Unresolved"
        INVESTIGATING = "INVESTIGATING", "Under Investigation"
        RESOLVED = "RESOLVED", "Resolved"

    node = models.ForeignKey(HostNode, on_delete=models.CASCADE, related_name="anomalies")
    title = models.CharField(max_length=200)
    severity = models.CharField(max_length=15, choices=Severity.choices, default=Severity.MEDIUM, db_index=True)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.ACTIVE, db_index=True)
    metric_type = models.CharField(max_length=50, default="CPU")
    detected_value = models.FloatField()
    expected_baseline = models.FloatField()
    description = models.TextField()
    root_cause_summary = models.TextField(blank=True, default="")
    recommended_action = models.TextField(blank=True, default="")
    detected_at = models.DateTimeField(auto_now_add=True, db_index=True)
    resolved_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        ordering = ["-detected_at"]

    def __str__(self):
        return f"[{self.severity}] {self.title} on {self.node.hostname}"
