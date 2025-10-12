import { Card } from "@/components/ui/card";
import { CheckCircle2, Circle } from "lucide-react";

export const Scene8 = () => {
  const phases = [
    {
      phase: "Phase 1",
      title: "Prototype Simulation",
      status: "completed",
      description: "AI algorithms tested and validated",
    },
    {
      phase: "Phase 2",
      title: "Real Sensor Integration",
      status: "in-progress",
      description: "Schneider Electric data integration",
    },
    {
      phase: "Phase 3",
      title: "Physical Lab Deployment",
      status: "planned",
      description: "Testing in controlled environment",
    },
    {
      phase: "Phase 4",
      title: "Industry-Scale Rollout",
      status: "planned",
      description: "Full data center implementation",
    },
  ];

  return (
    <div className="relative w-full h-full bg-gradient-to-br from-primary/5 via-background to-secondary/5 overflow-hidden">
      <div className="absolute inset-0 bg-[radial-gradient(circle_at_center,rgba(139,92,246,0.1)_0%,transparent_70%)]" />
      
      <div className="relative z-10 flex flex-col items-center justify-center h-full px-8">
        <div className="max-w-5xl w-full space-y-12">
          <div className="text-center space-y-4 animate-fade-in">
            <h2 className="text-5xl md:text-6xl font-bold text-foreground">
              The Roadmap
            </h2>
            <p className="text-xl text-muted-foreground">
              From prototype to production
            </p>
          </div>

          <div className="space-y-6">
            {phases.map((item, idx) => (
              <Card
                key={idx}
                className={`p-6 bg-card/50 backdrop-blur-sm border-border hover:border-primary/50 transition-all duration-300 animate-fade-in ${
                  item.status === "completed" ? "border-optimal/50" : ""
                }`}
                style={{ animationDelay: `${idx * 0.15}s` }}
              >
                <div className="flex items-start gap-6">
                  <div className="flex-shrink-0">
                    {item.status === "completed" ? (
                      <CheckCircle2 className="w-12 h-12 text-optimal" />
                    ) : (
                      <Circle className={`w-12 h-12 ${
                        item.status === "in-progress" ? "text-warning" : "text-muted-foreground"
                      }`} />
                    )}
                  </div>
                  <div className="flex-1">
                    <div className="flex items-center gap-3 mb-2">
                      <span className="text-sm font-semibold text-primary">
                        {item.phase}
                      </span>
                      {item.status === "completed" && (
                        <span className="text-xs px-2 py-1 rounded-full bg-optimal/20 text-optimal">
                          ✓ Complete
                        </span>
                      )}
                      {item.status === "in-progress" && (
                        <span className="text-xs px-2 py-1 rounded-full bg-warning/20 text-warning">
                          In Progress
                        </span>
                      )}
                    </div>
                    <h3 className="text-xl font-bold text-foreground mb-1">
                      {item.title}
                    </h3>
                    <p className="text-muted-foreground">{item.description}</p>
                  </div>
                </div>
              </Card>
            ))}
          </div>

          <Card className="p-8 bg-gradient-to-r from-primary/10 to-secondary/10 border-primary/30 animate-fade-in" style={{ animationDelay: "0.8s" }}>
            <p className="text-center text-lg md:text-xl text-foreground">
              Our system is <span className="font-bold text-primary">modular</span>,{" "}
              <span className="font-bold text-optimal">scalable</span>, and{" "}
              <span className="font-bold text-secondary">hardware-agnostic</span>.
              <br />
              It's built to grow with the data center of tomorrow.
            </p>
          </Card>
        </div>
      </div>
    </div>
  );
};
