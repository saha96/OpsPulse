import { ClusterOverview, HostNode, AnomalyIncident, LogEntry } from "@/types";

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000/api/v1";

async function fetchJson<T>(endpoint: string, options?: RequestInit): Promise<T> {
  const url = `${API_BASE_URL}${endpoint}`;
  try {
    const res = await fetch(url, {
      ...options,
      headers: {
        "Content-Type": "application/json",
        ...options?.headers,
      },
    });

    if (!res.ok) {
      throw new Error(`API error ${res.status}: ${res.statusText}`);
    }

    return (await res.json()) as T;
  } catch (error) {
    console.warn(`Falling back to mock data for ${endpoint}:`, error);
    throw error;
  }
}

export const api = {
  getOverview: async (): Promise<ClusterOverview> => {
    try {
      return await fetchJson<ClusterOverview>("/telemetry/overview");
    } catch {
      // Robust offline mock data for instant preview
      return {
        total_nodes: 5,
        healthy_nodes: 4,
        degraded_nodes: 1,
        offline_nodes: 0,
        avg_cpu_percent: 44.8,
        avg_memory_percent: 58.2,
        active_anomalies_count: 1,
        total_logs_24h: 12450,
      };
    }
  },

  getNodes: async (): Promise<HostNode[]> => {
    try {
      return await fetchJson<HostNode[]>("/telemetry/nodes");
    } catch {
      return [
        {
          id: 1,
          hostname: "k8s-control-plane-01",
          ip_address: "10.0.1.10",
          os_name: "Ubuntu 24.04 LTS",
          cpu_cores: 16,
          total_ram_gb: 64.0,
          status: "ONLINE",
          region: "us-east-1",
          tags: { role: "master", cluster: "prod-alpha" },
          last_heartbeat: new Date().toISOString(),
        },
        {
          id: 2,
          hostname: "k8s-worker-node-01",
          ip_address: "10.0.1.21",
          os_name: "Ubuntu 24.04 LTS",
          cpu_cores: 32,
          total_ram_gb: 128.0,
          status: "ONLINE",
          region: "us-east-1",
          tags: { role: "worker", pool: "compute-heavy" },
          last_heartbeat: new Date().toISOString(),
        },
        {
          id: 3,
          hostname: "k8s-worker-node-02",
          ip_address: "10.0.1.22",
          os_name: "Ubuntu 24.04 LTS",
          cpu_cores: 32,
          total_ram_gb: 128.0,
          status: "DEGRADED",
          region: "us-east-1",
          tags: { role: "worker", pool: "compute-heavy" },
          last_heartbeat: new Date().toISOString(),
        },
        {
          id: 4,
          hostname: "db-primary-postgres",
          ip_address: "10.0.2.15",
          os_name: "Debian 12 Bookworm",
          cpu_cores: 16,
          total_ram_gb: 64.0,
          status: "ONLINE",
          region: "us-east-1",
          tags: { tier: "database", engine: "postgres-16" },
          last_heartbeat: new Date().toISOString(),
        },
        {
          id: 5,
          hostname: "edge-proxy-gw-01",
          ip_address: "10.0.3.5",
          os_name: "Alpine Linux 3.19",
          cpu_cores: 8,
          total_ram_gb: 16.0,
          status: "ONLINE",
          region: "us-east-1",
          tags: { tier: "edge", proxy: "envoy" },
          last_heartbeat: new Date().toISOString(),
        },
      ];
    }
  },

  getAnomalies: async (): Promise<AnomalyIncident[]> => {
    try {
      return await fetchJson<AnomalyIncident[]>("/anomalies/incidents");
    } catch {
      return [
        {
          id: 101,
          node_id: 3,
          node_hostname: "k8s-worker-node-02",
          title: "Sustained High CPU Load on Worker Node",
          severity: "HIGH",
          status: "ACTIVE",
          metric_type: "CPU",
          detected_value: 88.4,
          expected_baseline: 42.0,
          description: "Worker node CPU sustained above 85% for 45 consecutive minutes, threatening pod eviction boundaries.",
          root_cause_summary: "High thread contention in container image transcoding service queue.",
          recommended_action: "Execute `kubectl top pods -n default` and scale replica count from 3 to 6.",
          detected_at: new Date(Date.now() - 3600000).toISOString(),
        },
      ];
    }
  },

  getLogs: async (): Promise<LogEntry[]> => {
    try {
      return await fetchJson<LogEntry[]>("/telemetry/logs");
    } catch {
      return [
        {
          id: 1,
          node_hostname: "edge-proxy-gw-01",
          timestamp: new Date().toISOString(),
          service_name: "api-gateway",
          level: "INFO",
          message: "Incoming HTTP POST /v1/chat/completions upstream proxy 200 OK (latency: 18ms)",
          trace_id: "tr-94812",
          metadata: { ip: "192.168.1.10" },
        },
        {
          id: 2,
          node_hostname: "k8s-worker-node-02",
          timestamp: new Date(Date.now() - 60000).toISOString(),
          service_name: "image-transcoder",
          level: "WARN",
          message: "Thread executor queue backlog exceeded 250 items. Throttling non-essential tasks.",
          trace_id: "tr-94811",
          metadata: { queue_size: 254 },
        },
        {
          id: 3,
          node_hostname: "db-primary-postgres",
          timestamp: new Date(Date.now() - 120000).toISOString(),
          service_name: "postgres-pool",
          level: "WARN",
          message: "Query duration 420ms exceeds 200ms threshold: SELECT * FROM telemetry_metricpoint",
          trace_id: "tr-94810",
          metadata: { duration_ms: 420 },
        },
      ];
    }
  },
};
