import { useEffect, useState } from "react";
import { Card } from "@/components/ui/card";
import { TrendingUp } from "lucide-react";

export const Scene5 = () => {
  const [counts, setCounts] = useState({
    temp: 0,
    variance: 0,
    recovery: 0,
    efficiency: 0,
  });

  useEffect(() => {
    const duration = 2000;
    const steps = 60;
    const interval = duration / steps;

    const targets = {
      temp: 24.94,
      variance: 4.08,
      recovery: 0,
      efficiency: 98,
    };

    let currentStep = 0;
    const timer = setInterval(() => {
      currentStep++;
      const progress = currentStep / steps;

      setCounts({
        temp: parseFloat((targets.temp * progress).toFixed(2)),
        variance: parseFloat((targets.variance * progress).toFixed(2)),
        recovery: Math.floor(targets.recovery * progress),
        efficiency: Math.floor(targets.efficiency * progress),
      });

      if (currentStep >= steps) {
        clearInterval(timer);
        setCounts(targets);
      }
    }, interval);

    return () => clearInterval(timer);
  }, []);

  const metrics = [
    {
      label: "Average Temperature",
      value: counts.temp,
      unit: "°C",
      color: "text-optimal",
    },
    {
      label: "Temperature Variance",
      value: counts.variance,
      unit: "°C²",
      color: "text-primary",
    },
    {
      label: "Recovery Time",
      value: counts.recovery,
      unit: "steps",
      color: "text-cooling",
    },
    {
      label: "System Efficiency",
      value: counts.efficiency,
      unit: "%",
      color: "text-optimal",
    },
  ];

  return (
    <div className="relative w-full h-full bg-gradient-to-br from-optimal/10 via-background to-background overflow-hidden">
      <div className="absolute inset-0 bg-[radial-gradient(circle_at_center,rgba(16,185,129,0.1)_0%,transparent_70%)]" />
      
      <div className="relative z-10 flex flex-col items-center justify-center h-full px-8">
        <div className="max-w-5xl space-y-12">
          <div className="text-center space-y-4 animate-fade-in">
            <TrendingUp className="w-16 h-16 mx-auto text-optimal" />
            <h2 className="text-5xl md:text-6xl font-bold text-foreground">
              The Results
            </h2>
          </div>

          <div className="grid md:grid-cols-2 gap-6">
            {metrics.map((metric, idx) => (
              <Card
                key={idx}
                className="p-8 bg-card/50 backdrop-blur-sm border-border hover:border-optimal/50 transition-all duration-300 animate-scale-in"
                style={{ animationDelay: `${idx * 0.1}s` }}
              >
                <div className="text-sm text-muted-foreground mb-2">
                  {metric.label}
                </div>
                <div className="flex items-baseline gap-2">
                  <span className={`text-5xl font-bold ${metric.color}`}>
                    {metric.value}
                  </span>
                  <span className="text-2xl text-muted-foreground">
                    {metric.unit}
                  </span>
                </div>
              </Card>
            ))}
          </div>

          <Card className="p-8 bg-gradient-to-r from-optimal/20 to-cooling/20 border-optimal/30 animate-fade-in" style={{ animationDelay: "0.6s" }}>
            <p className="text-center text-xl md:text-2xl text-foreground font-semibold">
              The swarm healed itself instantly — maintaining balance and minimizing energy waste.
            </p>
          </Card>
        </div>
      </div>
    </div>
  );
};
