import { useState, useEffect, useCallback } from "react";
import { AgentStatus } from "@/components/CoolingAgent";

export interface AgentData {
  id: number;
  temperature: number;
  fanSpeed: number;
  power: number;
  status: AgentStatus;
}

interface SimulationData {
  agents: AgentData[];
  avgTemp: number;
  variance: number;
  avgPower: number;
  recoveryTime: number;
  efficiency: number;
  phase: string;
  phaseDescription: string;
}

export const useSimulation = (scenario: "prototype" | "vision") => {
  const [step, setStep] = useState(0);
  const [isPlaying, setIsPlaying] = useState(false);
  const [faultInjected, setFaultInjected] = useState(false);

  const maxSteps = scenario === "prototype" ? 200 : 250;
  const numAgents = scenario === "prototype" ? 6 : 20;
  const faultStep = scenario === "prototype" ? 50 : 100;

  const calculateSimulationData = useCallback(
    (currentStep: number, manualFault = false): SimulationData => {
      const agents: AgentData[] = [];
      const targetTemp = 25.0;
      
      // Determine phase
      let phase = "";
      let phaseDescription = "";
      
      if (currentStep < faultStep) {
        phase = "Stable Operation";
        phaseDescription = scenario === "prototype" 
          ? "System Stable — Energy Efficient Cooling"
          : "AI Swarm Maintaining Thermal Balance";
      } else if (currentStep === faultStep || manualFault) {
        phase = "Fault Detected";
        phaseDescription = scenario === "prototype"
          ? "⚠️ Fault Detected — Cooling Failure in Agent " + (numAgents - 1)
          : "⚙️ Autonomous Self-Healing in Progress — Multi-Fault Adaptation";
      } else if (currentStep < faultStep + 50) {
        phase = "Self-Healing Response";
        phaseDescription = scenario === "prototype"
          ? "Self-Healing in Progress — Adaptive Load Redistribution"
          : "⚙️ Autonomous Self-Healing in Progress";
      } else {
        phase = "System Stabilized";
        phaseDescription = scenario === "prototype"
          ? "✅ System Stabilized — Partial Recovery Achieved"
          : "✅ System Restored — Zero Downtime Achieved";
      }

      // Generate agent data
      for (let i = 0; i < numAgents; i++) {
        let temp = targetTemp;
        let fanSpeed = 50;
        let power = 430;
        let status: AgentStatus = "healthy";

        if (currentStep >= faultStep || manualFault) {
          // After fault injection
          const isFaultyAgent = scenario === "prototype" 
            ? i === numAgents - 1 
            : i === numAgents - 1 || i === numAgents - 2 || i === numAgents - 3;
          
          if (isFaultyAgent && currentStep < faultStep + 100) {
            // Faulty agent
            temp = targetTemp + 5 + Math.random() * 3;
            fanSpeed = 0;
            power = 0;
            status = "faulty";
          } else if (!isFaultyAgent && Math.abs(i - (numAgents - 1)) <= (scenario === "vision" ? 5 : 2)) {
            // Neighboring agents compensating (exclude faulty agents)
            if (currentStep < faultStep + 50) {
              status = "compensating";
              fanSpeed = 75 + Math.random() * 20;
              power = 500 + Math.random() * 100;
              temp = targetTemp - 0.5 - Math.random();
            } else {
              status = "healthy";
              fanSpeed = 55 + Math.random() * 10;
              power = 440 + Math.random() * 20;
              temp = targetTemp + (Math.random() - 0.5) * 0.5;
            }
          } else {
            // Other agents
            temp = targetTemp + (Math.random() - 0.5) * (scenario === "vision" ? 0.2 : 1);
            fanSpeed = 50 + Math.random() * 10;
            power = 430 + Math.random() * 20;
          }
        } else {
          // Before fault
          temp = targetTemp + (Math.random() - 0.5) * (scenario === "vision" ? 0.1 : 0.4);
          fanSpeed = 50 + Math.random() * 5;
          power = 430 + Math.random() * 10;
        }

        agents.push({ id: i, temperature: temp, fanSpeed, power, status });
      }

      // Calculate metrics
      const avgTemp = agents.reduce((sum, a) => sum + a.temperature, 0) / numAgents;
      const variance = agents.reduce((sum, a) => sum + Math.pow(a.temperature - avgTemp, 2), 0) / numAgents;
      const avgPower = agents.reduce((sum, a) => sum + a.power, 0) / numAgents;
      
      let recoveryTime = 0;
      if (currentStep > faultStep && currentStep < faultStep + 50) {
        recoveryTime = currentStep - faultStep;
      }
      
      const efficiency = scenario === "vision" 
        ? (currentStep > faultStep + 100 ? 1.0 : 0.85)
        : (currentStep < faultStep ? 0.42 : currentStep > faultStep + 100 ? 0.38 : 0.30);

      return {
        agents,
        avgTemp,
        variance,
        avgPower,
        recoveryTime,
        efficiency,
        phase,
        phaseDescription,
      };
    },
    [scenario, numAgents, faultStep]
  );

  const [data, setData] = useState<SimulationData>(() => calculateSimulationData(0));

  useEffect(() => {
    if (isPlaying) {
      const interval = setInterval(() => {
        setStep((prev) => {
          const next = prev >= maxSteps ? 0 : prev + 1;
          setData(calculateSimulationData(next, faultInjected));
          return next;
        });
      }, 100); // 10 steps per second

      return () => clearInterval(interval);
    }
  }, [isPlaying, maxSteps, calculateSimulationData, faultInjected]);

  const handlePlayPause = () => {
    setIsPlaying((prev) => !prev);
  };

  const handleReset = () => {
    setStep(0);
    setIsPlaying(false);
    setFaultInjected(false);
    setData(calculateSimulationData(0));
  };

  const handleInjectFault = () => {
    if (!faultInjected) {
      setFaultInjected(true);
      setStep(faultStep);
      setData(calculateSimulationData(faultStep, true));
    }
  };

  return {
    step,
    maxSteps,
    isPlaying,
    data,
    handlePlayPause,
    handleReset,
    handleInjectFault,
    canInjectFault: !faultInjected && step < faultStep,
  };
};
