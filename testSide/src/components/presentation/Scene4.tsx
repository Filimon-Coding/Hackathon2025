import { Card } from "@/components/ui/card";
import { Brain, Shield, Gauge, Zap } from "lucide-react";

export const Scene4 = () => {
  const algorithms = [
    {
      icon: Brain,
      title: "Swarm Intelligence",
      description: "Collective decision-making via local interactions",
      color: "text-primary",
    },
    {
      icon: Shield,
      title: "Artificial Immune System",
      description: "Fault detection through anomaly patterns",
      color: "text-optimal",
    },
    {
      icon: Gauge,
      title: "Adaptive Control Theory",
      description: "Real-time feedback and correction",
      color: "text-cooling",
    },
    {
      icon: Zap,
      title: "Reinforcement Learning",
      description: "Energy optimization through learning",
      color: "text-warning",
    },
  ];

  return (
    <div className="relative w-full h-full bg-gradient-to-br from-primary/5 via-background to-secondary/5 overflow-hidden">
      {/* Network visualization background */}
      <div className="absolute inset-0 opacity-20">
        <svg className="w-full h-full">
          {[...Array(12)].map((_, i) => (
            <g key={i}>
              <circle
                cx={`${20 + (i % 4) * 20}%`}
                cy={`${30 + Math.floor(i / 4) * 20}%`}
                r="3"
                fill="currentColor"
                className="text-primary"
              >
                <animate
                  attributeName="opacity"
                  values="0.3;1;0.3"
                  dur={`${2 + Math.random()}s`}
                  repeatCount="indefinite"
                />
              </circle>
              {i % 4 !== 3 && (
                <line
                  x1={`${20 + (i % 4) * 20}%`}
                  y1={`${30 + Math.floor(i / 4) * 20}%`}
                  x2={`${20 + ((i % 4) + 1) * 20}%`}
                  y2={`${30 + Math.floor(i / 4) * 20}%`}
                  stroke="currentColor"
                  strokeWidth="1"
                  className="text-primary/30"
                />
              )}
            </g>
          ))}
        </svg>
      </div>

      <div className="relative z-10 flex flex-col items-center justify-center h-full px-8">
        <div className="max-w-6xl space-y-12">
          <h2 className="text-5xl md:text-6xl font-bold text-center text-foreground animate-fade-in">
            How It Works
          </h2>

          <div className="grid md:grid-cols-2 gap-6">
            {algorithms.map((algo, idx) => (
              <Card
                key={idx}
                className="p-8 bg-card/50 backdrop-blur-sm border-border hover:border-primary/50 transition-all duration-300 animate-scale-in"
                style={{ animationDelay: `${idx * 0.15}s` }}
              >
                <algo.icon className={`w-12 h-12 mb-4 ${algo.color}`} />
                <h3 className="text-xl font-bold text-foreground mb-2">
                  {algo.title}
                </h3>
                <p className="text-muted-foreground">{algo.description}</p>
              </Card>
            ))}
          </div>

          <Card className="p-8 bg-gradient-to-r from-primary/10 to-secondary/10 border-primary/30 animate-fade-in" style={{ animationDelay: "0.8s" }}>
            <p className="text-center text-lg md:text-xl text-foreground italic">
              "Each agent senses, decides, and acts independently — but collectively, they form a resilient, adaptive system."
            </p>
          </Card>
        </div>
      </div>
    </div>
  );
};
