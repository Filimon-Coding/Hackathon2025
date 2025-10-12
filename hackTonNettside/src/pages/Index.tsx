import { useState } from "react";
import { CoolingAgent } from "@/components/CoolingAgent";
import { MetricsPanel } from "@/components/MetricsPanel";
import { SimulationControls } from "@/components/SimulationControls";
import { PhaseIndicator } from "@/components/PhaseIndicator";
import { useSimulation } from "@/hooks/useSimulation";
import { Button } from "@/components/ui/button";
import { Card } from "@/components/ui/card";

const Index = () => {
  const [scenario, setScenario] = useState<"prototype" | "vision">("prototype");
  
  const {
    step,
    maxSteps,
    isPlaying,
    data,
    handlePlayPause,
    handleReset,
    handleInjectFault,
    canInjectFault,
  } = useSimulation(scenario);

  return (
    <div className="min-h-screen bg-background text-foreground p-8">
      {/* Header */}
      <div className="max-w-7xl mx-auto mb-8">
        <div className="text-center mb-8 animate-fade-in">
          <h1 className="text-5xl font-bold mb-4 bg-gradient-to-r from-primary to-secondary bg-clip-text text-transparent">
            Self-Healing Swarm AI Cooling System
          </h1>
          <p className="text-xl text-muted-foreground">
            Interactive Simulation of Autonomous Data Center Thermal Management
          </p>
        </div>

        {/* Scenario Selector */}
        <Card className="p-4 bg-card border-border mb-8">
          <div className="flex gap-4 justify-center">
            <Button
              size="lg"
              variant={scenario === "prototype" ? "default" : "outline"}
              onClick={() => setScenario("prototype")}
              className={scenario === "prototype" ? "bg-primary text-primary-foreground" : ""}
            >
              📊 Prototype Results
              <span className="ml-2 text-xs opacity-75">(6 Agents - Realistic)</span>
            </Button>
            <Button
              size="lg"
              variant={scenario === "vision" ? "default" : "outline"}
              onClick={() => setScenario("vision")}
              className={scenario === "vision" ? "bg-secondary text-foreground" : ""}
            >
              🚀 Future Vision
              <span className="ml-2 text-xs opacity-75">(20 Agents - Ideal)</span>
            </Button>
          </div>
        </Card>

        {/* Phase Indicator */}
        <Card className="p-6 bg-card border-border mb-8">
          <PhaseIndicator
            phase={data.phase}
            description={data.phaseDescription}
            step={step}
            maxSteps={maxSteps}
          />
        </Card>
      </div>

      {/* Main Content */}
      <div className="max-w-7xl mx-auto grid grid-cols-1 lg:grid-cols-3 gap-8">
        {/* Agents Visualization */}
        <div className="lg:col-span-2">
          <Card className="p-8 bg-card border-border h-full">
            <h2 className="text-2xl font-semibold mb-6">
              {scenario === "prototype" ? "6-Agent System" : "20-Agent Swarm"}
            </h2>
            
            {/* Agent Grid */}
            <div
              className={`grid gap-6 mb-8 ${
                scenario === "prototype"
                  ? "grid-cols-3"
                  : "grid-cols-5"
              }`}
            >
              {data.agents.map((agent) => (
                <CoolingAgent
                  key={agent.id}
                  {...agent}
                  size={scenario === "prototype" ? "large" : "small"}
                />
              ))}
            </div>

            {/* Network Visualization (Vision only) */}
            {scenario === "vision" && (
              <div className="mt-6 p-4 bg-muted/50 rounded-lg border border-border">
                <div className="flex items-center gap-3 mb-2">
                  <div className="w-3 h-3 bg-primary rounded-full animate-pulse" />
                  <span className="text-sm font-medium">
                    AI Communication Network Active
                  </span>
                </div>
                <p className="text-xs text-muted-foreground">
                  {data.agents.filter((a) => a.status === "compensating").length} agents
                  actively coordinating thermal distribution
                </p>
              </div>
            )}
          </Card>
        </div>

        {/* Sidebar */}
        <div className="space-y-6">
          {/* Controls */}
          <Card className="p-6 bg-card border-border">
            <h3 className="text-lg font-semibold mb-4">Controls</h3>
            <SimulationControls
              isPlaying={isPlaying}
              onPlayPause={handlePlayPause}
              onReset={handleReset}
              onInjectFault={handleInjectFault}
              canInjectFault={canInjectFault}
            />
          </Card>

          {/* Metrics */}
          <MetricsPanel
            avgTemp={data.avgTemp}
            variance={data.variance}
            avgPower={data.avgPower}
            recoveryTime={data.recoveryTime}
            efficiency={data.efficiency}
            scenario={scenario}
          />

          {/* Info Card */}
          <Card className="p-6 bg-card border-border">
            <h3 className="text-lg font-semibold mb-3">Legend</h3>
            <div className="space-y-2 text-sm">
              <div className="flex items-center gap-2">
                <div className="w-4 h-4 bg-cooling rounded-full" />
                <span>Cooling ({"<"}24°C)</span>
              </div>
              <div className="flex items-center gap-2">
                <div className="w-4 h-4 bg-optimal rounded-full" />
                <span>Optimal (24-26°C)</span>
              </div>
              <div className="flex items-center gap-2">
                <div className="w-4 h-4 bg-heating rounded-full" />
                <span>Heating ({">"}26°C)</span>
              </div>
              <div className="flex items-center gap-2">
                <div className="w-4 h-4 bg-fault rounded-full" />
                <span>Faulty (Critical)</span>
              </div>
              <div className="flex items-center gap-2">
                <div className="w-4 h-4 bg-warning rounded-full" />
                <span>Compensating</span>
              </div>
            </div>
          </Card>
        </div>
      </div>

      {/* Footer Note */}
      <div className="max-w-7xl mx-auto mt-8 text-center">
        <p className="text-sm text-muted-foreground">
          {scenario === "prototype"
            ? "📊 Current prototype showing realistic fault recovery with 6 cooling agents"
            : "🚀 Future vision demonstrating ideal 20-agent system with perfect coordination"}
        </p>
      </div>
    </div>
  );
};

export default Index;
