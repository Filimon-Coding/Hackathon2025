import { TrendingUp, AlertTriangle, Clock } from "lucide-react";
import { Card } from "@/components/ui/card";

export const Scene2 = () => {
  const problems = [
    {
      icon: TrendingUp,
      text: "Cooling = 40% of data center energy",
      color: "text-heating",
    },
    {
      icon: AlertTriangle,
      text: "Faults cause downtime and energy waste",
      color: "text-fault",
    },
    {
      icon: Clock,
      text: "Current systems react after it's too late",
      color: "text-warning",
    },
  ];

  return (
    <div className="relative w-full h-full bg-gradient-to-br from-fault/10 via-background to-background overflow-hidden">
      <div className="absolute inset-0 bg-[radial-gradient(circle_at_center,rgba(255,68,68,0.1)_0%,transparent_70%)]" />
      
      <div className="relative z-10 flex flex-col items-center justify-center h-full px-8">
        <div className="max-w-5xl space-y-12 animate-fade-in">
          <h2 className="text-5xl md:text-6xl font-bold text-center text-foreground mb-12">
            The Problem
          </h2>

          <div className="grid md:grid-cols-3 gap-6">
            {problems.map((problem, idx) => (
              <Card
                key={idx}
                className="p-8 bg-card/50 backdrop-blur-sm border-border hover:border-primary/50 transition-all duration-300 animate-scale-in"
                style={{ animationDelay: `${idx * 0.2}s` }}
              >
                <problem.icon className={`w-12 h-12 mb-4 ${problem.color}`} />
                <p className="text-lg text-foreground">{problem.text}</p>
              </Card>
            ))}
          </div>

          <div className="text-center mt-16 space-y-4 animate-fade-in" style={{ animationDelay: "0.8s" }}>
            <div className="text-2xl md:text-3xl text-muted-foreground italic max-w-3xl mx-auto">
              "We needed a way for data centers to adapt, self-correct, and stay efficient — without human intervention."
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};
