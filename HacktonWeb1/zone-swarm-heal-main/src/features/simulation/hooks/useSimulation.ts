import { useState, useEffect, useCallback } from "react";
import { Agent, HealthStatus, SimulationStats } from "@/features/simulation/types/agent";

const INITIAL_TEMP = 25;
const TARGET_TEMP = 22;
const TEMP_THRESHOLD_HIGH = 28;
const TEMP_THRESHOLD_LOW = 20;
const COOLING_RATE = 0.5;
const HEATING_RATE = 0.3;
const SIMULATION_SPEED = 500; // ms

const createInitialAgents = (count: number): Agent[] => {
  const agents: Agent[] = [];
  
  for (let i = 0; i < count; i++) {
    // Each agent communicates with adjacent agents (circular topology)
    const neighbors = [
      (i - 1 + count) % count,
      (i + 1) % count,
    ];
    
    agents.push({
      id: i,
      temperature: INITIAL_TEMP + Math.random() * 4 - 2,
      targetTemperature: TARGET_TEMP,
      load: Math.random() * 50 + 25,
      fanSpeed: 50,
      healthStatus: "healthy",
      neighbors,
      isHealing: false,
      communicating: false,
    });
  }
  
  return agents;
};

export const useSimulation = (agentCount: number = 5) => {
  const [agents, setAgents] = useState<Agent[]>(() => createInitialAgents(agentCount));
  const [isRunning, setIsRunning] = useState(false);
  const [temperatureHistory, setTemperatureHistory] = useState<{ time: number; [key: string]: number }[]>([]);
  const [time, setTime] = useState(0);

  const calculateStats = useCallback((currentAgents: Agent[]): SimulationStats => {
    const avgTemp = currentAgents.reduce((sum, a) => sum + a.temperature, 0) / currentAgents.length;
    const healthy = currentAgents.filter(a => a.healthStatus === "healthy").length;
    const failed = currentAgents.filter(a => a.healthStatus === "failed").length;
    const totalLoad = currentAgents.reduce((sum, a) => sum + a.load, 0);
    
    return {
      averageTemperature: avgTemp,
      healthyAgents: healthy,
      failedAgents: failed,
      totalLoad,
    };
  }, []);

  const updateAgent = useCallback((agent: Agent, allAgents: Agent[]): Agent => {
    if (agent.healthStatus === "failed") {
      // Failed agents don't cool and overheat
      return {
        ...agent,
        temperature: Math.min(agent.temperature + HEATING_RATE * 2, 40),
        fanSpeed: 0,
      };
    }

    // Get neighbor info
    const neighborAgents = agent.neighbors.map(id => allAgents[id]);
    const failedNeighbors = neighborAgents.filter(n => n.healthStatus === "failed");
    const healthyNeighbors = neighborAgents.filter(n => n.healthStatus === "healthy" || n.healthStatus === "healing");

    // Detect anomalies and trigger healing
    let newHealthStatus: HealthStatus = agent.healthStatus;
    let isHealing = agent.isHealing;
    
    if (failedNeighbors.length > 0 && agent.healthStatus === "healthy") {
      // Start healing process to compensate for failed neighbors
      newHealthStatus = "healing";
      isHealing = true;
    } else if (isHealing && failedNeighbors.length === 0) {
      // Healing complete
      newHealthStatus = "healthy";
      isHealing = false;
    }

    // Calculate load redistribution from failed neighbors
    const extraLoad = failedNeighbors.reduce((sum, n) => sum + n.load, 0) / healthyNeighbors.length;
    const effectiveLoad = agent.load + (extraLoad || 0);

    // Adjust fan speed based on temperature and load
    let targetFanSpeed = 50;
    if (agent.temperature > TEMP_THRESHOLD_HIGH) {
      targetFanSpeed = 100;
    } else if (agent.temperature > agent.targetTemperature + 2) {
      targetFanSpeed = 75;
    } else if (agent.temperature < TEMP_THRESHOLD_LOW) {
      targetFanSpeed = 25;
    }

    // Compensate for high load
    if (effectiveLoad > 60) {
      targetFanSpeed = Math.min(100, targetFanSpeed + 20);
    }

    // Smooth fan speed adjustment
    const newFanSpeed = agent.fanSpeed + (targetFanSpeed - agent.fanSpeed) * 0.3;

    // Calculate temperature change
    const coolingEffect = (newFanSpeed / 100) * COOLING_RATE;
    const heatingEffect = (effectiveLoad / 100) * HEATING_RATE;
    const tempChange = heatingEffect - coolingEffect;
    const newTemp = agent.temperature + tempChange;

    // Check health status based on temperature
    if (newTemp > 35) {
      newHealthStatus = "warning";
    } else if (newTemp <= agent.targetTemperature + 3 && newHealthStatus === "warning") {
      newHealthStatus = isHealing ? "healing" : "healthy";
    }

    return {
      ...agent,
      temperature: Math.max(18, Math.min(40, newTemp)),
      fanSpeed: newFanSpeed,
      healthStatus: newHealthStatus,
      load: effectiveLoad > agent.load ? effectiveLoad * 0.95 : agent.load, // Gradually reduce redistributed load
      isHealing,
      communicating: failedNeighbors.length > 0,
    };
  }, []);

  const simulationStep = useCallback(() => {
    setAgents(currentAgents => {
      const updatedAgents = currentAgents.map(agent => updateAgent(agent, currentAgents));
      
      // Update temperature history
      setTemperatureHistory(prev => {
        const newEntry: { time: number; [key: string]: number } = { time };
        updatedAgents.forEach(agent => {
          newEntry[`agent${agent.id}`] = Math.round(agent.temperature * 10) / 10;
        });
        
        const newHistory = [...prev, newEntry];
        // Keep only last 50 data points
        return newHistory.slice(-50);
      });
      
      setTime(t => t + 1);
      return updatedAgents;
    });
  }, [time, updateAgent]);

  useEffect(() => {
    if (!isRunning) return;

    const interval = setInterval(simulationStep, SIMULATION_SPEED);
    return () => clearInterval(interval);
  }, [isRunning, simulationStep]);

  const toggleSimulation = useCallback(() => {
    setIsRunning(prev => !prev);
  }, []);

  const resetSimulation = useCallback(() => {
    setAgents(createInitialAgents(agentCount));
    setTemperatureHistory([]);
    setTime(0);
    setIsRunning(false);
  }, [agentCount]);

  const triggerFailure = useCallback((agentId: number) => {
    setAgents(currentAgents =>
      currentAgents.map(agent =>
        agent.id === agentId
          ? { ...agent, healthStatus: "failed" as HealthStatus, fanSpeed: 0 }
          : agent
      )
    );
  }, []);

  const repairAgent = useCallback((agentId: number) => {
    setAgents(currentAgents =>
      currentAgents.map(agent =>
        agent.id === agentId
          ? { ...agent, healthStatus: "healthy" as HealthStatus, isHealing: false }
          : agent
      )
    );
  }, []);

  return {
    agents,
    isRunning,
    temperatureHistory,
    time,
    stats: calculateStats(agents),
    toggleSimulation,
    resetSimulation,
    triggerFailure,
    repairAgent,
  };
};
