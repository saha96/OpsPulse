from datetime import datetime
from typing import Any

from pydantic import BaseModel, Field


class HostNodeOut(BaseModel):
    id: int
    hostname: str
    ip_address: str
    os_name: str
    cpu_cores: int
    total_ram_gb: float
    status: str
    region: str
    tags: dict[str, Any]
    last_heartbeat: datetime


class MetricPointOut(BaseModel):
    id: int
    timestamp: datetime
    cpu_usage_percent: float
    memory_usage_percent: float
    disk_usage_percent: float
    network_rx_mb: float
    network_tx_mb: float


class MetricIngestIn(BaseModel):
    hostname: str
    timestamp: datetime | None = None
    cpu_usage_percent: float = Field(..., ge=0.0, le=100.0)
    memory_usage_percent: float = Field(..., ge=0.0, le=100.0)
    disk_usage_percent: float = Field(..., ge=0.0, le=100.0)
    network_rx_mb: float = 0.0
    network_tx_mb: float = 0.0


class LogEntryOut(BaseModel):
    id: int
    node_hostname: str
    timestamp: datetime
    service_name: str
    level: str
    message: str
    trace_id: str | None = None
    metadata: dict[str, Any]


class LogIngestIn(BaseModel):
    hostname: str
    timestamp: datetime | None = None
    service_name: str
    level: str = "INFO"
    message: str
    trace_id: str | None = None
    metadata: dict[str, Any] | None = None


class ClusterOverviewOut(BaseModel):
    total_nodes: int
    healthy_nodes: int
    degraded_nodes: int
    offline_nodes: int
    avg_cpu_percent: float
    avg_memory_percent: float
    active_anomalies_count: int
    total_logs_24h: int
