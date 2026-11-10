import React from "react";
import { AlertTriangle, Terminal, Sparkles, CheckCircle2, ArrowRight } from "lucide-react";
import { Card, CardHeader, CardTitle, CardContent } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { AnomalyIncident } from "@/types";

interface IncidentPanelProps {
  incidents: AnomalyIncident[];
}

export function IncidentPanel({ incidents }: IncidentPanelProps) {
  if (!incidents || incidents.length === 0) {
    return (
      <Card className="border-border/70 bg-card/60 backdrop-blur-sm p-6 text-center">
        <CheckCircle2 className="h-8 w-8 text-emerald-500 mx-auto mb-2" />
        <h4 className="text-sm font-semibold text-foreground">No Active Anomaly Incidents</h4>
        <p className="text-xs text-muted-foreground mt-1">
          All statistical baselines are currently operating within acceptable variance limits.
        </p>
      </Card>
    );
  }

  const incident = incidents[0];

  return (
    <Card className="border-destructive/30 bg-card/60 backdrop-blur-sm overflow-hidden shadow-sm relative">
      <div className="absolute top-0 left-0 w-1.5 h-full bg-destructive" />
      <CardHeader className="p-4 border-b flex flex-row items-center justify-between pb-3">
        <div className="flex items-center gap-2.5">
          <div className="p-1.5 rounded-lg bg-destructive/15 text-destructive border border-destructive/20">
            <AlertTriangle className="h-4 w-4" />
          </div>
          <div>
            <div className="flex items-center gap-2">
              <CardTitle className="text-sm font-semibold text-foreground">{incident.title}</CardTitle>
              <Badge variant="destructive" className="text-[10px] uppercase font-mono py-0">
                {incident.severity}
              </Badge>
            </div>
            <p className="text-xs text-muted-foreground font-mono mt-0.5">
              Target Node: {incident.node_hostname} • Metric: {incident.metric_type} ({incident.detected_value}% vs baseline {incident.expected_baseline}%)
            </p>
          </div>
        </div>

        <Badge variant="outline" className="font-mono text-xs hidden sm:block">
          Incident #{incident.id}
        </Badge>
      </CardHeader>

      <CardContent className="p-4 space-y-3.5">
        <p className="text-xs text-muted-foreground leading-relaxed">
          {incident.description}
        </p>

        {/* AI Root-Cause Insight */}
        <div className="rounded-lg bg-primary/5 border border-primary/20 p-3 space-y-2">
          <div className="flex items-center gap-1.5 text-xs font-semibold text-primary">
            <Sparkles className="h-3.5 w-3.5 text-primary" />
            <span>AIOps Root-Cause Analysis</span>
          </div>
          <p className="text-xs text-foreground/90 font-medium leading-relaxed">
            {incident.root_cause_summary}
          </p>
        </div>

        {/* Suggested Operator Command */}
        {incident.recommended_action && (
          <div className="space-y-1.5">
            <div className="text-[11px] font-semibold text-muted-foreground uppercase tracking-wider flex items-center gap-1 font-mono">
              <Terminal className="h-3 w-3" />
              Suggested Remediation Command
            </div>
            <div className="rounded-md bg-secondary/80 border border-border/70 p-2.5 font-mono text-xs text-foreground flex items-center justify-between">
              <code>{incident.recommended_action}</code>
              <Button size="sm" variant="ghost" className="h-7 text-xs text-primary hover:text-primary">
                Copy
              </Button>
            </div>
          </div>
        )}

        <div className="pt-1 flex items-center justify-end gap-2">
          <Button variant="outline" size="sm" className="text-xs">
            Dismiss Alert
          </Button>
          <Button size="sm" className="text-xs gap-1.5">
            Acknowledge & Triage
            <ArrowRight className="h-3.5 w-3.5" />
          </Button>
        </div>
      </CardContent>
    </Card>
  );
}
