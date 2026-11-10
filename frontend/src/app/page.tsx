"use client";

import React, { useState, useEffect } from "react";
import {
  Server,
  Cpu,
  Layers,
  AlertTriangle,
  FileText,
  RefreshCw,
  HardDrive,
  Zap,
} from "lucide-react";
import { DashboardHeader } from "@/components/dashboard/header";
import { DashboardSidebar } from "@/components/dashboard/sidebar";
import { MetricCard } from "@/components/dashboard/metric-card";
import { NodeTable } from "@/components/dashboard/node-table";
import { IncidentPanel } from "@/components/dashboard/incident-panel";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { api } from "@/lib/api";
import { ClusterOverview, HostNode, AnomalyIncident, LogEntry } from "@/types";

export default function DashboardPage() {
  const [activeTab, setActiveTab] = useState("overview");
  const [loading, setLoading] = useState(true);
  const [overview, setOverview] = useState<ClusterOverview | null>(null);
  const [nodes, setNodes] = useState<HostNode[]>([]);
  const [anomalies, setAnomalies] = useState<AnomalyIncident[]>([]);
  const [logs, setLogs] = useState<LogEntry[]>([]);

  const loadData = async () => {
    setLoading(true);
    try {
      const [ovData, nodeData, anomData, logData] = await Promise.all([
        api.getOverview(),
        api.getNodes(),
        api.getAnomalies(),
        api.getLogs(),
      ]);
      setOverview(ovData);
      setNodes(nodeData);
      setAnomalies(anomData);
      setLogs(logData);
    } catch (e) {
      console.error("Error loading dashboard data:", e);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadData();
    const interval = setInterval(loadData, 15000);
    return () => clearInterval(interval);
  }, []);

  return (
    <div className="min-h-screen bg-background flex flex-col">
      <DashboardHeader />

      <div className="flex flex-1">
        <DashboardSidebar activeTab={activeTab} setActiveTab={setActiveTab} />

        <main className="flex-1 p-6 space-y-6 max-w-7xl mx-auto w-full">
          {/* Top Actions & Subheader */}
          <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4">
            <div>
              <h1 className="text-xl font-bold tracking-tight text-foreground">
                Cluster Health & Telemetry
              </h1>
              <p className="text-xs text-muted-foreground mt-0.5">
                Real-time observability stream across all connected host nodes.
              </p>
            </div>

            <div className="flex items-center gap-2">
              <Button
                variant="outline"
                size="sm"
                onClick={loadData}
                disabled={loading}
                className="gap-2 text-xs"
              >
                <RefreshCw className={`h-3.5 w-3.5 ${loading ? "animate-spin" : ""}`} />
                Sync Telemetry
              </Button>
              <Button size="sm" className="gap-2 text-xs bg-primary hover:bg-primary/90">
                <Zap className="h-3.5 w-3.5" />
                Add Host Agent
              </Button>
            </div>
          </div>

          {/* Key Metrics Grid */}
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
            <MetricCard
              title="Active Compute Nodes"
              value={overview?.healthy_nodes || 0}
              subValue={`/ ${overview?.total_nodes || 0} online`}
              icon={Server}
              change="99.98% Uptime"
              trend="up"
              statusColor="text-emerald-500"
            />
            <MetricCard
              title="Average CPU Load"
              value={`${overview?.avg_cpu_percent || 0}%`}
              icon={Cpu}
              change="+3.2% vs 1h"
              trend="neutral"
              statusColor="text-primary"
            />
            <MetricCard
              title="Average Memory Load"
              value={`${overview?.avg_memory_percent || 0}%`}
              icon={Layers}
              change="Stable"
              trend="neutral"
              statusColor="text-primary"
            />
            <MetricCard
              title="Active Anomaly Incidents"
              value={overview?.active_anomalies_count || 0}
              icon={AlertTriangle}
              change="1 Requires Review"
              trend="down"
              statusColor="text-destructive"
            />
          </div>

          {/* Incident Triage Panel */}
          <div className="space-y-2">
            <div className="flex items-center justify-between">
              <h2 className="text-sm font-semibold text-foreground flex items-center gap-2">
                <AlertTriangle className="h-4 w-4 text-destructive" />
                Active AIOps Anomaly Triage
              </h2>
              <span className="text-xs text-muted-foreground font-mono">
                Statistical Z-Score Engine
              </span>
            </div>
            <IncidentPanel incidents={anomalies} />
          </div>

          {/* Host Nodes Inventory */}
          <div className="space-y-2">
            <NodeTable nodes={nodes} />
          </div>

          {/* Live Structured Logs Explorer */}
          <div className="rounded-xl border bg-card/60 backdrop-blur-sm overflow-hidden shadow-sm">
            <div className="p-4 border-b flex items-center justify-between">
              <div>
                <h3 className="font-semibold text-sm text-foreground flex items-center gap-2">
                  <FileText className="h-4 w-4 text-primary" />
                  Live Structured Log Stream
                </h3>
                <p className="text-xs text-muted-foreground mt-0.5">
                  Recent system events and microservice trace logs
                </p>
              </div>
              <Badge variant="outline" className="font-mono text-xs">
                {logs.length} Recent Events
              </Badge>
            </div>

            <div className="divide-y divide-border/50 text-xs font-mono">
              {logs.map((log) => (
                <div
                  key={log.id}
                  className="p-3.5 flex flex-col md:flex-row md:items-center justify-between gap-2 hover:bg-accent/40 transition-colors"
                >
                  <div className="flex items-center gap-3">
                    <Badge
                      variant={
                        log.level === "ERROR"
                          ? "destructive"
                          : log.level === "WARN"
                          ? "warning"
                          : "secondary"
                      }
                      className="text-[10px] py-0 px-2 uppercase font-bold"
                    >
                      {log.level}
                    </Badge>
                    <span className="text-primary font-medium">{log.service_name}</span>
                    <span className="text-muted-foreground hidden sm:inline">•</span>
                    <span className="text-foreground/90 font-sans text-xs">{log.message}</span>
                  </div>

                  <div className="flex items-center gap-4 text-muted-foreground text-[11px] shrink-0">
                    <span className="text-primary/70">{log.node_hostname}</span>
                    {log.trace_id && (
                      <span className="border border-border/80 px-1.5 py-0.5 rounded text-[10px]">
                        {log.trace_id}
                      </span>
                    )}
                    <span>{new Date(log.timestamp).toLocaleTimeString()}</span>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </main>
      </div>
    </div>
  );
}
