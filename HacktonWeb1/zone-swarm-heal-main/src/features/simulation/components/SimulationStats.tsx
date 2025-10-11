import { Card } from "@/components/ui/card";
import { SimulationStats as Stats } from "@/features/simulation/types/agent";
import { Thermometer, Activity, AlertCircle, Zap } from "lucide-react";

interface SimulationStatsProps {
  stats: Stats;
  totalAgents: number;
}

export const SimulationStats = ({ stats, totalAgents }: SimulationStatsProps) => {
  const getTempColor = () => {
    if (stats.averageTemperature > 28) return "text-destructive";
    if (stats.averageTemperature > 24) return "text-warning";
    return "text-primary";
  };

  return (
    <Card className="p-6">
      <h2 className="text-xl font-semibold mb-4">System Statistics</h2>
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
        <div className="space-y-1">
          <div className="flex items-center gap-2 text-muted-foreground">
            <Thermometer className="h-4 w-4" />
            <span className="text-sm">Avg Temperature</span>
          </div>
          <p className={`data-value text-2xl ${getTempColor()}`}>
            {stats.averageTemperature.toFixed(1)}°C
          </p>
        </div>
        
        <div className="space-y-1">
          <div className="flex items-center gap-2 text-muted-foreground">
            <Activity className="h-4 w-4" />
            <span className="text-sm">Healthy Agents</span>
          </div>
          <p className="data-value text-2xl text-accent">
            {stats.healthyAgents}/{totalAgents}
          </p>
        </div>
        
        <div className="space-y-1">
          <div className="flex items-center gap-2 text-muted-foreground">
            <AlertCircle className="h-4 w-4" />
            <span className="text-sm">Failed Agents</span>
          </div>
          <p className="data-value text-2xl text-destructive">
            {stats.failedAgents}
          </p>
        </div>
        
        <div className="space-y-1">
          <div className="flex items-center gap-2 text-muted-foreground">
            <Zap className="h-4 w-4" />
            <span className="text-sm">Total Load</span>
          </div>
          <p className="data-value text-2xl">
            {stats.totalLoad.toFixed(0)}%
          </p>
        </div>
      </div>
    </Card>
  );
};
