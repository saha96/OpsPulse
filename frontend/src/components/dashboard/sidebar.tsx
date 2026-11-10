"use client";

import React from "react";
import {
  LayoutDashboard,
  Server,
  Activity,
  AlertTriangle,
  FileText,
  Sliders,
  Shield,
  ExternalLink,
} from "lucide-react";
import { cn } from "@/lib/utils";

interface SidebarProps {
  activeTab: string;
  setActiveTab: (tab: string) => void;
}

export function DashboardSidebar({ activeTab, setActiveTab }: SidebarProps) {
  const navItems = [
    { id: "overview", label: "Overview", icon: LayoutDashboard },
    { id: "nodes", label: "Host Nodes", icon: Server },
    { id: "telemetry", label: "Live Telemetry", icon: Activity },
    { id: "anomalies", label: "AIOps Incidents", icon: AlertTriangle, badge: "1" },
    { id: "logs", label: "Log Explorer", icon: FileText },
    { id: "settings", label: "Cluster Settings", icon: Sliders },
  ];

  return (
    <aside className="w-64 border-r bg-card/50 flex flex-col justify-between shrink-0 hidden md:flex min-h-[calc(100vh-4rem)]">
      <div className="p-4 space-y-6">
        <div>
          <div className="text-[10px] font-semibold uppercase tracking-wider text-muted-foreground px-3 mb-2 font-mono">
            Platform Observability
          </div>
          <nav className="space-y-1">
            {navItems.map((item) => {
              const Icon = item.icon;
              const isActive = activeTab === item.id;
              return (
                <button
                  key={item.id}
                  onClick={() => setActiveTab(item.id)}
                  className={cn(
                    "flex w-full items-center justify-between rounded-lg px-3 py-2 text-xs font-medium transition-colors",
                    isActive
                      ? "bg-primary text-primary-foreground shadow-sm"
                      : "text-muted-foreground hover:bg-accent hover:text-foreground"
                  )}
                >
                  <div className="flex items-center gap-2.5">
                    <Icon className="h-4 w-4" />
                    <span>{item.label}</span>
                  </div>
                  {item.badge && (
                    <span
                      className={cn(
                        "rounded-full px-1.5 py-0.5 text-[10px] font-bold font-mono",
                        isActive
                          ? "bg-primary-foreground text-primary"
                          : "bg-destructive/20 text-destructive border border-destructive/30"
                      )}
                    >
                      {item.badge}
                    </span>
                  )}
                </button>
              );
            })}
          </nav>
        </div>

        <div className="pt-4 border-t">
          <div className="text-[10px] font-semibold uppercase tracking-wider text-muted-foreground px-3 mb-2 font-mono">
            Integrations & APIs
          </div>
          <div className="space-y-1 text-xs">
            <a
              href="http://localhost:8000/api/v1/docs"
              target="_blank"
              rel="noreferrer"
              className="flex items-center justify-between rounded-lg px-3 py-2 text-muted-foreground hover:bg-accent hover:text-foreground transition-colors"
            >
              <div className="flex items-center gap-2.5">
                <Shield className="h-4 w-4" />
                <span>Django Ninja Docs</span>
              </div>
              <ExternalLink className="h-3 w-3 opacity-60" />
            </a>
          </div>
        </div>
      </div>

      <div className="p-4 border-t">
        <div className="rounded-lg bg-secondary/50 p-3 border text-xs space-y-1.5">
          <div className="font-semibold text-foreground flex items-center justify-between">
            <span>Metifi-Grade Stack</span>
            <span className="text-[10px] text-primary font-mono">v1.0</span>
          </div>
          <p className="text-[11px] text-muted-foreground leading-relaxed">
            Django 5 Async backend with Next.js 15 App Router & shadcn/ui.
          </p>
        </div>
      </div>
    </aside>
  );
}
