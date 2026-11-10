"use client";

import React from "react";
import { Activity, Bell, ShieldCheck, Terminal, Search, Cpu } from "lucide-react";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";

export function DashboardHeader() {
  return (
    <header className="sticky top-0 z-30 flex h-16 w-full items-center justify-between border-b bg-background/95 px-6 backdrop-blur supports-[backdrop-filter]:bg-background/60">
      <div className="flex items-center gap-4">
        <div className="flex items-center gap-2">
          <div className="flex h-9 w-9 items-center justify-center rounded-lg bg-primary/10 text-primary border border-primary/20">
            <Activity className="h-5 w-5 animate-pulse" />
          </div>
          <div>
            <div className="flex items-center gap-2">
              <span className="font-bold tracking-tight text-foreground">OpsPulse</span>
              <Badge variant="outline" className="text-[10px] uppercase font-mono py-0">v1.0.0-rc</Badge>
            </div>
            <p className="text-xs text-muted-foreground hidden sm:block">Cloud Telemetry & AIOps Engine</p>
          </div>
        </div>

        <div className="hidden md:flex items-center gap-2 pl-6 border-l">
          <Badge variant="success" className="gap-1.5 py-0.5">
            <span className="h-1.5 w-1.5 rounded-full bg-emerald-500 animate-ping" />
            Cluster Healthy
          </Badge>
          <span className="text-xs text-muted-foreground font-mono">us-east-1 (5 Nodes)</span>
        </div>
      </div>

      <div className="flex items-center gap-3">
        <div className="relative hidden lg:block w-64">
          <Search className="absolute left-2.5 top-2.5 h-4 w-4 text-muted-foreground" />
          <input
            type="text"
            placeholder="Search hosts, logs, trace..."
            className="h-9 w-full rounded-md border border-input bg-background pl-9 pr-4 text-xs text-foreground placeholder:text-muted-foreground focus:outline-none focus:ring-1 focus:ring-ring"
          />
        </div>

        <Button variant="outline" size="sm" className="hidden sm:flex items-center gap-2 text-xs">
          <Terminal className="h-3.5 w-3.5" />
          CLI Mode
        </Button>

        <Button variant="ghost" size="icon" className="relative text-muted-foreground hover:text-foreground">
          <Bell className="h-4 w-4" />
          <span className="absolute top-2 right-2 h-2 w-2 rounded-full bg-primary" />
        </Button>

        <div className="flex items-center gap-2 pl-3 border-l">
          <div className="h-8 w-8 rounded-full bg-secondary flex items-center justify-center font-medium text-xs text-foreground border border-border">
            AH
          </div>
          <div className="hidden xl:block text-left">
            <div className="text-xs font-medium text-foreground">Amir Hossein</div>
            <div className="text-[10px] text-muted-foreground">Platform Lead</div>
          </div>
        </div>
      </div>
    </header>
  );
}
