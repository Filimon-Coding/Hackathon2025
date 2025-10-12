import { useSimulation } from "@/hooks/useSimulation";
import { CoolingAgent } from "@/components/CoolingAgent";
import { MetricsPanel } from "@/components/MetricsPanel";
import { SimulationControls } from "@/components/SimulationControls";
import { Card } from "@/components/ui/card";

export const Scene6 = () => {
  const {
    data,
    isPlaying,
    handlePlayPause,
    handleReset,
    handleInjectFault,
    canInjectFault,
  } = useSimulation("vision");

  return (
    <div className="relative w-full h-full bg-gradient-to-br from-secondary/10 via-background to-primary/10 overflow-hidden">
      <div className="absolute inset-0 bg-[radial-gradient(circle_at_center,rgba(139,92,246,0.15)_0%,transparent_70%)]" />
      
      <div className="relative z-10 h-full overflow-y-auto py-20 px-8">
        <div className="max-w-7xl mx-auto space-y-8">
          <div className="text-center space-y-4 animate-fade-in">
            <h2 className="text-4xl md:text-5xl font-bold text-foreground">
              The Vision
            </h2>
            <p className="text-xl text-secondary font-semibold">
              Next-Generation Self-Healing at Scale
            </p>
          </div>

          <div className="grid lg:grid-cols-3 gap-6">
            <div className="lg:col-span-2 space-y-6">
              <Card className="p-6 bg-card/50 backdrop-blur-sm">
                <div className="grid grid-cols-5 gap-2">
                  {data.agents.map((agent) => (
                    <CoolingAgent key={agent.id} {...agent} size="small" />
                  ))}
                </div>
              </Card>

              <div className="grid md:grid-cols-3 gap-4 text-center animate-fade-in" style={{ animationDelay: "0.3s" }}>
                <Card className="p-4 bg-primary/10 border-primary/30">
                  <p className="text-sm text-foreground">Scaling from 6 agents to hundreds</p>
                </Card>
                <Card className="p-4 bg-optimal/10 border-optimal/30">
                  <p className="text-sm text-foreground">Zero downtime. Zero energy loss.</p>
                </Card>
                <Card className="p-4 bg-secondary/10 border-secondary/30">
                  <p className="text-sm text-foreground">A data center that heals itself</p>
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
              <MetricsPanel {...data} scenario="vision" />
            </div>
          </div>

          <Card className="p-6 bg-gradient-to-r from-secondary/20 to-primary/20 border-secondary/30 animate-fade-in" style={{ animationDelay: "0.5s" }}>
            <p className="text-center text-lg text-foreground">
              <span className="font-semibold">Perfect Coordination:</span> AI Communication Network maintaining seamless thermal balance across the entire facility
            </p>
          </Card>
        </div>
      </div>
    </div>
  );
};
