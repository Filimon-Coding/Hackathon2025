import { Agent } from "@/features/simulation/types/agent";
import { Card } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { Progress } from "@/components/ui/progress";
import { AlertCircle, CheckCircle, Zap, Wind, AlertTriangle, Wrench } from "lucide-react";
import { cn } from "@/lib/utils";

interface CoolingAgentProps {
  agent: Agent;
  onTriggerFailure: () => void;
  onRepair: () => void;
}

export const CoolingAgent = ({ agent, onTriggerFailure, onRepair }: CoolingAgentProps) => {
  const getHealthIcon = () => {
    switch (agent.healthStatus) {
      case "healthy":
        return <CheckCircle className="h-5 w-5 text-accent" />;
      case "healing":
        return <Wrench className="h-5 w-5 text-primary" />;
      case "warning":
        return <AlertTriangle className="h-5 w-5 text-warning" />;
      case "failed":
        return <AlertCircle className="h-5 w-5 text-destructive" />;
    }
  };

  const getHealthBadgeVariant = () => {
    switch (agent.healthStatus) {
      case "healthy":
        return "default";
      case "healing":
        return "secondary";
      case "warning":
        return "outline";
      case "failed":
        return "destructive";
    }
  };

  const getCardClassName = () => {
    const base = "relative transition-all duration-300";
    
    if (agent.healthStatus === "failed") {
      return cn(base, "glow-destructive");
    }
    if (agent.isHealing) {
      return cn(base, "animate-healing");
    }
    if (agent.communicating) {
      return cn(base, "animate-pulse-glow");
    }
    return base;
  };

  const getTempColor = () => {
    if (agent.temperature > 30) return "text-destructive";
    if (agent.temperature > 25) return "text-warning";
    return "text-primary";
  };

  return (
    <Card className={getCardClassName()}>
      <div className="p-6 space-y-4">
        {/* Header */}
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-2">
            <h3 className="text-lg font-semibold">Agent {agent.id}</h3>
            {getHealthIcon()}
          </div>
          <Badge variant={getHealthBadgeVariant()} className="capitalize">
            {agent.healthStatus}
          </Badge>
        </div>

        {/* Temperature Display */}
        <div className="space-y-2">
          <div className="flex items-center justify-between">
            <span className="text-sm text-muted-foreground">Temperature</span>
            <span className={cn("data-value text-2xl", getTempColor())}>
              {agent.temperature.toFixed(1)}°C
            </span>
          </div>
          <Progress 
            value={(agent.temperature / 40) * 100} 
            className="h-2"
          />
        </div>

        {/* Fan Speed */}
        <div className="space-y-2">
          <div className="flex items-center justify-between">
            <span className="text-sm text-muted-foreground flex items-center gap-1">
              <Wind className="h-4 w-4" />
              Fan Speed
            </span>
            <span className="data-value text-primary">
              {agent.fanSpeed.toFixed(0)}%
            </span>
          </div>
          <Progress value={agent.fanSpeed} className="h-2" />
        </div>

        {/* Load */}
        <div className="space-y-2">
          <div className="flex items-center justify-between">
            <span className="text-sm text-muted-foreground flex items-center gap-1">
              <Zap className="h-4 w-4" />
              Load
            </span>
            <span className="data-value">
              {agent.load.toFixed(0)}%
            </span>
          </div>
          <Progress value={agent.load} className="h-2" />
        </div>

        {/* Communication Status */}
        {agent.communicating && (
          <div className="text-xs text-primary flex items-center gap-1">
            <div className="h-2 w-2 rounded-full bg-primary animate-pulse" />
            Communicating with neighbors
          </div>
        )}

        {agent.isHealing && (
          <div className="text-xs text-accent flex items-center gap-1">
            <Wrench className="h-3 w-3" />
            Self-healing in progress...
          </div>
        )}

        {/* Controls */}
        <div className="pt-2 flex gap-2">
          {agent.healthStatus === "failed" ? (
            <Button 
              onClick={onRepair} 
              variant="outline" 
              size="sm"
              className="w-full"
            >
              Repair
            </Button>
          ) : (
            <Button 
              onClick={onTriggerFailure} 
              variant="destructive" 
              size="sm"
              className="w-full"
            >
              Trigger Failure
            </Button>
          )}
        </div>
      </div>
    </Card>
  );
};
