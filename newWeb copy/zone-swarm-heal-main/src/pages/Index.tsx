import { useSimulation } from "@/features/simulation/hooks/useSimulation";
import { CoolingAgent } from "@/features/simulation/components/CoolingAgent";
import { TemperatureChart } from "@/features/simulation/components/TemperatureChart";
import { ControlPanel } from "@/features/simulation/components/ControlPanel";
import { SimulationStats } from "@/features/simulation/components/SimulationStats";
import { Server } from "lucide-react";

const AGENT_COUNT = 5;

const Index = () => {
  const {
    agents,
    isRunning,
    temperatureHistory,
    time,
    stats,
    toggleSimulation,
    resetSimulation,
    triggerFailure,
    repairAgent,
  } = useSimulation(AGENT_COUNT);

  return (
    <div className="min-h-screen bg-background p-4 md:p-8">
      <div className="max-w-7xl mx-auto space-y-6">
        {/* Header */}
        <div className="text-center space-y-2">
          <div className="flex items-center justify-center gap-3 mb-2">
            <Server className="h-8 w-8 text-primary" />
            <h1 className="text-4xl font-bold bg-gradient-to-r from-primary to-accent bg-clip-text text-transparent">
              Self-Healing Swarm Cooling System
            </h1>
          </div>
          <p className="text-muted-foreground max-w-2xl mx-auto">
            Autonomous data center cooling simulation with fault detection, load balancing, and self-healing capabilities
          </p>
        </div>

        {/* Control Panel */}
        <ControlPanel
          isRunning={isRunning}
          onToggle={toggleSimulation}
          onReset={resetSimulation}
          time={time}
        />

        {/* Stats */}
        <SimulationStats stats={stats} totalAgents={AGENT_COUNT} />

        {/* Cooling Agents Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-5 gap-4">
          {agents.map((agent) => (
            <CoolingAgent
              key={agent.id}
              agent={agent}
              onTriggerFailure={() => triggerFailure(agent.id)}
              onRepair={() => repairAgent(agent.id)}
            />
          ))}
        </div>

        {/* Temperature Chart */}
        {temperatureHistory.length > 0 && (
          <TemperatureChart data={temperatureHistory} agentCount={AGENT_COUNT} />
        )}

        {/* Info Panel */}
        <div className="bg-card border border-border rounded-lg p-6 space-y-3">
          <h3 className="text-lg font-semibold">How It Works</h3>
          <div className="grid md:grid-cols-2 gap-4 text-sm text-muted-foreground">
            <div>
              <h4 className="font-medium text-foreground mb-2">🔍 Fault Detection</h4>
              <p>Each agent monitors its own temperature and health status. When an agent fails, its neighbors detect the anomaly.</p>
            </div>
            <div>
              <h4 className="font-medium text-foreground mb-2">🔄 Load Redistribution</h4>
              <p>Healthy agents automatically redistribute the load from failed agents to maintain system operation.</p>
            </div>
            <div>
              <h4 className="font-medium text-foreground mb-2">💬 Agent Communication</h4>
              <p>Agents communicate with neighbors in a circular topology to share status and coordinate responses.</p>
            </div>
            <div>
              <h4 className="font-medium text-foreground mb-2">🛠️ Self-Healing</h4>
              <p>The swarm autonomously adapts fan speeds and load distribution to compensate for failures without manual intervention.</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Index;
