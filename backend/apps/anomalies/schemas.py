from datetime import datetime

from pydantic import BaseModel


class AnomalyIncidentOut(BaseModel):
    id: int
    node_id: int
    node_hostname: str
    title: str
    severity: str
    status: str
    metric_type: str
    detected_value: float
    expected_baseline: float
    description: str
    root_cause_summary: str
    recommended_action: str
    detected_at: datetime
    resolved_at: datetime | None = None


class AnomalyResolveIn(BaseModel):
    resolution_notes: str | None = "Resolved by operator"
