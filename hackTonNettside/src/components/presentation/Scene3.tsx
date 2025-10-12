import { useSimulation } from "@/hooks/useSimulation";
import { CoolingAgent } from "@/components/CoolingAgent";
import { MetricsPanel } from "@/components/MetricsPanel";
import { SimulationControls } from "@/components/SimulationControls";
import { Card } from "@/components/ui/card";

export const Scene3 = () => {
  const {
    data,
    isPlaying,
    handlePlayPause,
    handleReset,
    handleInjectFault,
    canInjectFault,
  } = useSimulation("prototype");

  return (
    <div className="relative w-full h-full bg-gradient-to-br from-cooling/10 via-background to-background overflow-hidden">
      <div className="absolute inset-0 bg-[radial-gradient(circle_at_center,rgba(79,209,197,0.1)_0%,transparent_70%)]" />
      
      <div className="relative z-10 h-full overflow-y-auto py-20 px-8">
        <div className="max-w-7xl mx-auto space-y-8">
          <div className="text-center space-y-4 animate-fade-in">
            <h2 className="text-4xl md:text-5xl font-bold text-foreground">
              The Solution
            </h2>
            <p className="text-xl text-primary font-semibold">
              The Self-Healing Swarm
            </p>
          </div>

          <div className="grid lg:grid-cols-3 gap-6">
            <div className="lg:col-span-2 space-y-6">
              <Card className="p-6 bg-card/50 backdrop-blur-sm">
                <div className="grid grid-cols-3 gap-4">
                  {data.agents.map((agent) => (
                    <CoolingAgent
                      key={agent.id}
                      {...agent}
                      size="small"
                    />
                  ))}
                </div>
              </Card>

              <div className="grid md:grid-cols-3 gap-4 text-center animate-fade-in" style={{ animationDelay: "0.3s" }}>
                <Card className="p-4 bg-optimal/10 border-optimal/30">
                  <p className="text-sm text-foreground">Each zone is an intelligent agent</p>
                </Card>
                <Card className="p-4 bg-warning/10 border-warning/30">
                  <p className="text-sm text-foreground">When one fails, others adapt</p>
                </Card>
                <Card className="p-4 bg-primary/10 border-primary/30">
                  <p className="text-sm text-foreground">Collective intelligence stabilizes</p>
                </Card>
              </div>
            </div>

            <div className="space-y-6">
              <SimulationControls
                isPlaying={isPlaying}
                onPlayPause={handlePlayPause}
                onReset={handleReset}
                onInjectFault={handleInjectFault}
                canInjectFault={canInjectFault}
              />
              <MetricsPanel {...data} scenario="prototype" />
            </div>
          </div>

          <Card className="p-6 bg-primary/5 border-primary/30 animate-fade-in" style={{ animationDelay: "0.5s" }}>
            <p className="text-center text-sm text-muted-foreground">
              <span className="font-semibold text-primary">Hover for details:</span> Swarm Intelligence + Self-Healing Control Algorithms
            </p>
          </Card>
        </div>
      </div>
    </div>
  );
};
