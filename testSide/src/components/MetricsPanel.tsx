import { Card } from "@/components/ui/card";

interface MetricsPanelProps {
  avgTemp: number;
  variance: number;
  avgPower: number;
  recoveryTime: number;
  efficiency: number;
  scenario: "prototype" | "vision";
}

export const MetricsPanel = ({
  avgTemp,
  variance,
  avgPower,
  recoveryTime,
  efficiency,
  scenario,
}: MetricsPanelProps) => {
  const MetricItem = ({
    label,
    value,
    unit,
    ideal,
  }: {
    label: string;
    value: number;
    unit: string;
    ideal?: boolean;
  }) => (
    <div className="flex flex-col gap-1">
      <div className="text-xs text-muted-foreground">{label}</div>
      <div className="flex items-baseline gap-2">
        <span className={`text-2xl font-bold ${ideal ? "text-optimal" : "text-primary"}`}>
          {value.toFixed(2)}
        </span>
        <span className="text-sm text-muted-foreground">{unit}</span>
      </div>
    </div>
  );

  return (
    <Card className="p-6 bg-card border-border">
      <h3 className="text-lg font-semibold mb-4 text-foreground">
        System Metrics
      </h3>
      <div className="grid grid-cols-2 gap-6">
        <MetricItem
          label="Average Temperature"
          value={avgTemp}
          unit="°C"
          ideal={scenario === "vision"}
        />
        <MetricItem
          label="Temperature Variance"
          value={variance}
          unit="°C²"
          ideal={scenario === "vision"}
        />
        <MetricItem
          label="Average Power"
          value={avgPower}
          unit="W"
        />
        <MetricItem
          label="Recovery Time"
          value={recoveryTime}
          unit="steps"
          ideal={scenario === "vision"}
        />
        <MetricItem
          label="Energy Efficiency"
          value={efficiency}
          unit=""
          ideal={scenario === "vision"}
        />
        
        {/* Status Indicator */}
        <div className="col-span-2 mt-4">
          <div className="flex items-center gap-3">
            <div
              className={`w-4 h-4 rounded-full ${
                efficiency > 0.8 ? "bg-optimal" : efficiency > 0.5 ? "bg-warning" : "bg-fault"
              } animate-pulse`}
            />
            <span className="text-sm font-medium">
              {efficiency > 0.8
                ? "Optimal Performance"
                : efficiency > 0.5
                ? "Stabilizing"
                : "Recovery in Progress"}
            </span>
          </div>
        </div>
      </div>
    </Card>
  );
};
