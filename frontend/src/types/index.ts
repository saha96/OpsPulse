export interface HostNode {
  id: number;
  hostname: string;
  ip_address: string;
  os_name: string;
  cpu_cores: number;
  total_ram_gb: number;
  status: "ONLINE" | "DEGRADED" | "OFFLINE";
  region: string;
  tags: Record<string, any>;
  last_heartbeat: string;
}

export interface MetricPoint {
  id: number;
  timestamp: string;
  cpu_usage_percent: number;
  memory_usage_percent: number;
  disk_usage_percent: number;
  network_rx_mb: number;
  network_tx_mb: number;
}

export interface LogEntry {
  id: number;
  node_hostname: string;
  timestamp: string;
  service_name: string;
  level: "DEBUG" | "INFO" | "WARN" | "ERROR" | "CRITICAL";
  message: string;
  trace_id?: string;
  metadata: Record<string, any>;
}

export interface AnomalyIncident {
  id: number;
  node_id: number;
  node_hostname: string;
  title: string;
  severity: "LOW" | "MEDIUM" | "HIGH" | "CRITICAL";
  status: "ACTIVE" | "INVESTIGATING" | "RESOLVED";
  metric_type: string;
  detected_value: number;
  expected_baseline: number;
  description: string;
  root_cause_summary: string;
  recommended_action: string;
  detected_at: string;
  resolved_at?: string;
}

export interface ClusterOverview {
  total_nodes: number;
  healthy_nodes: number;
  degraded_nodes: number;
  offline_nodes: number;
  avg_cpu_percent: number;
  avg_memory_percent: number;
  active_anomalies_count: number;
  total_logs_24h: number;
}
