import React from "react";
import { Server, Activity, ShieldCheck, AlertCircle } from "lucide-react";
import { Badge } from "@/components/ui/badge";
import { HostNode } from "@/types";

interface NodeTableProps {
  nodes: HostNode[];
}

export function NodeTable({ nodes }: NodeTableProps) {
  return (
    <div className="rounded-xl border bg-card/60 backdrop-blur-sm overflow-hidden shadow-sm">
      <div className="p-4 border-b flex items-center justify-between">
        <div>
          <h3 className="font-semibold text-sm text-foreground flex items-center gap-2">
            <Server className="h-4 w-4 text-primary" />
            Cluster Node Inventory
          </h3>
          <p className="text-xs text-muted-foreground mt-0.5">
            Active compute nodes transmitting health telemetry to OpsPulse
          </p>
        </div>
        <Badge variant="outline" className="font-mono text-xs">
          {nodes.length} Registered Nodes
        </Badge>
      </div>

      <div className="overflow-x-auto">
        <table className="w-full text-xs text-left">
          <thead className="bg-secondary/40 text-muted-foreground border-b text-[11px] font-semibold uppercase tracking-wider">
            <tr>
              <th className="px-4 py-3">Hostname</th>
              <th className="px-4 py-3">Status</th>
              <th className="px-4 py-3">IP Address</th>
              <th className="px-4 py-3">Compute Cores</th>
              <th className="px-4 py-3">Total RAM</th>
              <th className="px-4 py-3">Region</th>
              <th className="px-4 py-3 text-right">Heartbeat</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-border/50">
            {nodes.map((node) => {
              const isOnline = node.status === "ONLINE";
              const isDegraded = node.status === "DEGRADED";
              return (
                <tr key={node.id} className="hover:bg-accent/40 transition-colors">
                  <td className="px-4 py-3.5 font-medium text-foreground flex items-center gap-2 font-mono">
                    <span className="h-2 w-2 rounded-full bg-primary/60" />
                    {node.hostname}
                  </td>
                  <td className="px-4 py-3.5">
                    {isOnline && (
                      <Badge variant="success" className="gap-1 py-0.5">
                        <span className="h-1.5 w-1.5 rounded-full bg-emerald-500" />
                        Healthy
                      </Badge>
                    )}
                    {isDegraded && (
                      <Badge variant="warning" className="gap-1 py-0.5">
                        <AlertCircle className="h-3 w-3" />
                        Degraded
                      </Badge>
                    )}
                    {!isOnline && !isDegraded && (
                      <Badge variant="destructive" className="gap-1 py-0.5">
                        Offline
                      </Badge>
                    )}
                  </td>
                  <td className="px-4 py-3.5 font-mono text-muted-foreground">{node.ip_address}</td>
                  <td className="px-4 py-3.5 font-mono text-foreground">{node.cpu_cores} vCPUs</td>
                  <td className="px-4 py-3.5 font-mono text-foreground">{node.total_ram_gb} GB</td>
                  <td className="px-4 py-3.5 text-muted-foreground">{node.region}</td>
                  <td className="px-4 py-3.5 text-right font-mono text-[11px] text-muted-foreground">
                    Just now
                  </td>
                </tr>
              );
            })}
          </tbody>
        </table>
      </div>
    </div>
  );
}
