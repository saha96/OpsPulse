from django.db import models

class HostNode(models.Model):
    class Status(models.TextChoices):
        ONLINE = 'ONLINE', 'Healthy / Online'
        DEGRADED = 'DEGRADED', 'Performance Degraded'
        OFFLINE = 'OFFLINE', 'Unreachable / Offline'

    hostname = models.CharField(max_length=150, unique=True, db_index=True)
    ip_address = models.GenericIPAddressField()
    os_name = models.CharField(max_length=100, default='Ubuntu 24.04 LTS')
    cpu_cores = models.PositiveIntegerField(default=8)
    total_ram_gb = models.FloatField(default=32.0)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.ONLINE)
    region = models.CharField(max_length=50, default='us-east-1')
    tags = models.JSONField(default=dict, blank=True)
    last_heartbeat = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['hostname']

    def __str__(self):
        return f"{self.hostname} [{self.status}]"

class MetricPoint(models.Model):
    node = models.ForeignKey(HostNode, on_delete=models.CASCADE, related_name='metrics')
    timestamp = models.DateTimeField(db_index=True)
    cpu_usage_percent = models.FloatField()
    memory_usage_percent = models.FloatField()
    disk_usage_percent = models.FloatField()
    network_rx_mb = models.FloatField(default=0.0)
    network_tx_mb = models.FloatField(default=0.0)

    class Meta:
        ordering = ['-timestamp']
        indexes = [
            models.Index(fields=['node', '-timestamp']),
        ]

    def __str__(self):
        return f"{self.node.hostname} @ {self.timestamp}: CPU {self.cpu_usage_percent}%"

class StructuredLog(models.Model):
    class Level(models.TextChoices):
        DEBUG = 'DEBUG', 'Debug'
        INFO = 'INFO', 'Info'
        WARN = 'WARN', 'Warning'
        ERROR = 'ERROR', 'Error'
        CRITICAL = 'CRITICAL', 'Critical'

    node = models.ForeignKey(HostNode, on_delete=models.CASCADE, related_name='logs')
    timestamp = models.DateTimeField(db_index=True)
    service_name = models.CharField(max_length=100, db_index=True)
    level = models.CharField(max_length=10, choices=Level.choices, default=Level.INFO, db_index=True)
    message = models.TextField()
    trace_id = models.CharField(max_length=64, blank=True, null=True, db_index=True)
    metadata = models.JSONField(default=dict, blank=True)

    class Meta:
        ordering = ['-timestamp']
        indexes = [
            models.Index(fields=['level', '-timestamp']),
            models.Index(fields=['service_name', '-timestamp']),
        ]

    def __str__(self):
        return f"[{self.level}] {self.service_name}: {self.message[:50]}"
