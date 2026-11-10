import React from "react";
import { LucideIcon } from "lucide-react";
import { Card, CardContent } from "@/components/ui/card";
import { cn } from "@/lib/utils";

interface MetricCardProps {
  title: string;
  value: string | number;
  subValue?: string;
  icon: LucideIcon;
  change?: string;
  trend?: "up" | "down" | "neutral";
  statusColor?: string;
}

export function MetricCard({
  title,
  value,
  subValue,
  icon: Icon,
  change,
  trend = "neutral",
  statusColor = "text-primary",
}: MetricCardProps) {
  return (
    <Card className="overflow-hidden relative border-border/70 bg-card/60 backdrop-blur-sm transition-all hover:border-border hover:shadow-md">
      <CardContent className="p-5">
        <div className="flex items-center justify-between">
          <p className="text-xs font-medium text-muted-foreground">{title}</p>
          <div className={cn("p-2 rounded-lg bg-secondary/80 border border-border/40", statusColor)}>
            <Icon className="h-4 w-4" />
          </div>
        </div>

        <div className="mt-3 flex items-baseline justify-between">
          <div>
            <span className="text-2xl font-bold tracking-tight text-foreground font-mono">
              {value}
            </span>
            {subValue && (
              <span className="ml-1.5 text-xs text-muted-foreground font-medium">
                {subValue}
              </span>
            )}
          </div>

          {change && (
            <span
              className={cn(
                "inline-flex items-center text-xs font-semibold px-1.5 py-0.5 rounded",
                trend === "up" && "bg-emerald-500/10 text-emerald-500",
                trend === "down" && "bg-destructive/10 text-destructive",
                trend === "neutral" && "bg-secondary text-muted-foreground"
              )}
            >
              {change}
            </span>
          )}
        </div>
      </CardContent>
    </Card>
  );
}
