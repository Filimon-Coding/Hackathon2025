import { cn } from "@/lib/utils";

export type AgentStatus = "healthy" | "faulty" | "compensating" | "cooling";

interface CoolingAgentProps {
  id: number;
  temperature: number;
  fanSpeed: number;
  power: number;
  status: AgentStatus;
  size?: "small" | "large";
  onClick?: () => void;
}

export const CoolingAgent = ({
  id,
  temperature,
  fanSpeed,
  power,
  status,
  size = "large",
  onClick,
}: CoolingAgentProps) => {
  const getStatusColor = () => {
    if (status === "faulty") return "bg-fault";
    if (status === "compensating") return "bg-warning";
    if (temperature < 24) return "bg-cooling";
    if (temperature < 26) return "bg-optimal";
    return "bg-heating";
  };

  const getGlow = () => {
    if (status === "faulty") return "glow-fault";
    if (temperature < 26) return "glow-optimal";
    return "";
  };

  const sizeClass = size === "small" ? "w-20 h-20" : "w-32 h-32";

  return (
    <div
      className={cn(
        "relative flex flex-col items-center gap-2 transition-all duration-500 cursor-pointer",
        onClick && "hover:scale-105"
      )}
      onClick={onClick}
    >
      {/* Agent Circle */}
      <div
        className={cn(
          sizeClass,
          "relative rounded-full border-2 border-border flex items-center justify-center",
          getStatusColor(),
          getGlow(),
          "transition-all duration-500"
        )}
      >
        {/* Fan Animation */}
        {status !== "faulty" && (
          <div
            className="absolute inset-0 rounded-full border-4 border-transparent border-t-foreground/30"
            style={{
              animation: `spin ${4 - (fanSpeed / 100) * 2}s linear infinite`,
            }}
          />
        )}

        {/* Temperature Display */}
        <div className="text-center z-10">
          <div className="text-lg font-bold text-foreground">
            {temperature.toFixed(1)}°C
          </div>
          {size === "large" && (
            <div className="text-xs text-muted-foreground">
              {fanSpeed}% | {power}W
            </div>
          )}
        </div>

        {/* Fault Indicator */}
        {status === "faulty" && (
          <div className="absolute -top-2 -right-2 w-6 h-6 bg-fault rounded-full animate-pulse flex items-center justify-center text-xs font-bold">
            ⚠
          </div>
        )}
      </div>

      {/* Agent Label */}
      <div className="text-sm font-medium text-foreground">
        Agent {id}
      </div>

      {/* Status Badge */}
      {size === "large" && (
        <div
          className={cn(
            "px-2 py-1 rounded-full text-xs font-semibold",
            status === "healthy" && "bg-optimal/20 text-optimal",
            status === "faulty" && "bg-fault/20 text-fault",
            status === "compensating" && "bg-warning/20 text-warning",
            status === "cooling" && "bg-cooling/20 text-cooling"
          )}
        >
          {status.toUpperCase()}
        </div>
      )}
    </div>
  );
};
