import { cn } from "@/lib/utils";

interface PhaseIndicatorProps {
  phase: string;
  description: string;
  step: number;
  maxSteps: number;
}

export const PhaseIndicator = ({
  phase,
  description,
  step,
  maxSteps,
}: PhaseIndicatorProps) => {
  const getPhaseIcon = () => {
    if (phase.includes("Stable")) return "🌱";
    if (phase.includes("Fault")) return "⚠️";
    if (phase.includes("Healing")) return "⚙️";
    if (phase.includes("Recovery")) return "✅";
    return "🔄";
  };

  return (
    <div className="space-y-4">
      {/* Phase Header */}
      <div className="flex items-center gap-3">
        <span className="text-3xl">{getPhaseIcon()}</span>
        <div>
          <h2 className="text-2xl font-bold text-foreground">{phase}</h2>
          <p className="text-muted-foreground">{description}</p>
        </div>
      </div>

      {/* Progress Bar */}
      <div className="w-full h-2 bg-muted rounded-full overflow-hidden">
        <div
          className={cn(
            "h-full transition-all duration-300 ease-linear",
            "bg-gradient-to-r from-primary to-secondary"
          )}
          style={{ width: `${(step / maxSteps) * 100}%` }}
        />
      </div>

      {/* Step Counter */}
      <div className="text-sm text-muted-foreground text-right">
        Step {step} / {maxSteps}
      </div>
    </div>
  );
};
