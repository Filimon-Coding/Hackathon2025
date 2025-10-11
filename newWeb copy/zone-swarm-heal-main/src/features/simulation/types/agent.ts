export type HealthStatus = "healthy" | "warning" | "failed" | "healing";

export interface Agent {
  id: number;
  temperature: number;
  targetTemperature: number;
  load: number;
  fanSpeed: number;
  healthStatus: HealthStatus;
  neighbors: number[];
  isHealing: boolean;
  communicating: boolean;
}

export interface SimulationStats {
  averageTemperature: number;
  healthyAgents: number;
  failedAgents: number;
  totalLoad: number;
}
