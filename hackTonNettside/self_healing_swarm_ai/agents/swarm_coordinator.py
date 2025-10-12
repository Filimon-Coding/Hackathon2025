
"""
Swarm Coordinator for managing multiple cooling agents.
"""

import numpy as np
from typing import List, Dict, Optional, Tuple
from datetime import datetime
from .cooling_agent import CoolingAgent


class SwarmCoordinator:
    """
    Coordinates multiple cooling agents using swarm intelligence principles.
    Implements self-healing and load balancing capabilities.
    """
    
    def __init__(self, num_agents: int, config: Dict, 
                 anomaly_detector=None, adaptive_controller=None):
        """
        Initialize swarm coordinator.
        
        Args:
            num_agents: Number of cooling agents
            config: System configuration
            anomaly_detector: Anomaly detection model
            adaptive_controller: Adaptive control model
        """
        self.num_agents = num_agents
        self.config = config
        self.anomaly_detector = anomaly_detector
        self.adaptive_controller = adaptive_controller
        
        # Initialize agents
        self.agents: List[CoolingAgent] = []
        for i in range(num_agents):
            agent = CoolingAgent(
                agent_id=i,
                config=config,
                anomaly_detector=anomaly_detector,
                adaptive_controller=adaptive_controller
            )
            self.agents.append(agent)
        
        # Swarm parameters
        self.communication_weight = config['swarm']['communication_weight']
        self.cooperation_strength = config['swarm']['cooperation_strength']
        self.topology = config['swarm']['topology']
        
        # State tracking
        self.temps = np.array([agent.temperature for agent in self.agents])
        self.fan_speeds = np.array([agent.fan_speed for agent in self.agents])
        self.faulty_agents = set()
        
        # History for visualization
        self.temp_history = []
        self.energy_history = []
        self.fault_events = []
        
        # Build communication topology
        self.neighbors = self._build_topology()
        
        # Simulation step counter
        self.current_step = 0
        
        print(f"✅ Swarm initialized with {num_agents} agents")
        print(f"   Topology: {self.topology}")
    
    def _build_topology(self) -> Dict[int, List[int]]:
        """
        Build communication topology between agents.
        
        Returns:
            Dictionary mapping agent ID to list of neighbor IDs
        """
        neighbors = {}
        
        if self.topology == "ring":
            # Each agent connects to left and right neighbors
            for i in range(self.num_agents):
                left = (i - 1) % self.num_agents
                right = (i + 1) % self.num_agents
                neighbors[i] = [left, right]
        
        elif self.topology == "mesh":
            # Each agent connects to all others
            for i in range(self.num_agents):
                neighbors[i] = [j for j in range(self.num_agents) if j != i]
        
        elif self.topology == "star":
            # Agent 0 is hub, connects to all
            neighbors[0] = list(range(1, self.num_agents))
            for i in range(1, self.num_agents):
                neighbors[i] = [0]
        
        else:
            raise ValueError(f"Unknown topology: {self.topology}")
        
        return neighbors
    
    def step(self):
        """
        Execute one simulation step for the entire swarm.
        """
        # Detect anomalies in all agents
        for agent in self.agents:
            if agent.detect_anomaly(self.anomaly_detector, self.current_step):
                if not agent.is_faulty:
                    print(f"⚠️  Fault detected in Agent {agent.agent_id} at step {self.current_step}")
                    agent.is_faulty = True
                    agent.fault_start_time = self.current_step
        
        # Update each agent's state
        for agent in self.agents:
            agent.update_state()
        
        # Swarm communication and cooperation
        self._swarm_communication()
        
        # Detect and handle faults
        self._detect_faults()
        
        # Self-healing behavior
        if self.faulty_agents:
            self._self_heal()
        
        # Update history
        self.temps = np.array([agent.temperature for agent in self.agents])
        self.fan_speeds = np.array([agent.fan_speed for agent in self.agents])
        self.temp_history.append(self.temps.copy())
        
        # Calculate total energy
        total_energy = sum(agent.power_consumption for agent in self.agents)
        self.energy_history.append(total_energy)
        
        # Increment step counter at the end
        self.current_step += 1
    
    def _swarm_communication(self):
        """
        Implement swarm communication between neighboring agents.
        Agents share temperature information and adjust accordingly.
        """
        new_temps = self.temps.copy()
        
        for i, agent in enumerate(self.agents):
            if i in self.faulty_agents:
                continue
            
            # Get neighbor temperatures
            neighbor_temps = [self.agents[n].temperature for n in self.neighbors[i]]
            avg_neighbor_temp = np.mean(neighbor_temps)
            
            # Apply swarm influence
            temp_diff = avg_neighbor_temp - agent.temperature
            swarm_adjustment = self.communication_weight * temp_diff
            
            # Update temperature (simulating heat transfer)
            new_temps[i] += swarm_adjustment * 0.1
        
        # Apply new temperatures
        for i, agent in enumerate(self.agents):
            if i not in self.faulty_agents:
                agent.temperature = new_temps[i]
    
    def _detect_faults(self):
        """
        Detect faulty agents using anomaly detection.
        """
        if self.anomaly_detector is None:
            return
        
        for i, agent in enumerate(self.agents):
            if i in self.faulty_agents:
                continue
            
            # Prepare sensor data
            sensor_data = np.array([[
                agent.temperature,
                agent.humidity,
                agent.power_consumption,
                agent.fan_speed
            ]])
            
            # Detect anomaly
            is_anomaly = agent.detect_anomaly(sensor_data)
            
            if is_anomaly:
                self.faulty_agents.add(i)
                agent.is_faulty = True
                
                # Log fault event
                self.fault_events.append({
                    'agent_id': i,
                    'detection_time': len(self.temp_history),
                    'temperature': agent.temperature
                })
                
                print(f"⚠️  Fault detected in Agent {i} at step {len(self.temp_history)}")
    
    def _self_heal(self):
        """
        Implement self-healing behavior.
        Healthy neighbors compensate for faulty agents.
        """
        for faulty_id in self.faulty_agents:
            # Get healthy neighbors
            healthy_neighbors = [
                n for n in self.neighbors[faulty_id] 
                if n not in self.faulty_agents
            ]
            
            if not healthy_neighbors:
                continue
            
            # Distribute load to healthy neighbors
            for neighbor_id in healthy_neighbors:
                neighbor = self.agents[neighbor_id]
                
                # Increase cooling effort
                compensation = self.cooperation_strength
                neighbor.fan_speed = min(1.0, neighbor.fan_speed + compensation)
                
                # Adjust temperature target
                neighbor.temperature -= compensation * 0.5
    
    def inject_fault(self, agent_id: Optional[int] = None) -> int:
        """
        Inject a fault into a specific agent or random agent.
        
        Args:
            agent_id: ID of agent to fault (random if None)
            
        Returns:
            ID of faulted agent
        """
        if agent_id is None:
            # Select random healthy agent
            healthy_agents = [i for i in range(self.num_agents) if i not in self.faulty_agents]
            if not healthy_agents:
                print("⚠️  No healthy agents available for fault injection")
                return -1
            agent_id = np.random.choice(healthy_agents)
        
        # Inject fault
        agent = self.agents[agent_id]
        agent.inject_fault()
        self.faulty_agents.add(agent_id)
        
        # Log event
        self.fault_events.append({
            'agent_id': agent_id,
            'injection_time': len(self.temp_history),
            'temperature': agent.temperature
        })
        
        print(f"💥 Fault injected into Agent {agent_id}")
        return agent_id
    
    def get_system_state(self) -> dict:
        """
        Get current system state metrics.
        
        Returns:
            Dictionary containing system state information
        """
        return {
            'avg_temperature': np.mean(self.temps),
            'temp_variance': np.var(self.temps),
            'avg_fan_speed': np.mean(self.fan_speeds),
            'total_power': sum(agent.power_consumption for agent in self.agents),
            'num_faulty': sum(1 for agent in self.agents if agent.is_faulty),
            'num_healthy': sum(1 for agent in self.agents if not agent.is_faulty)
        }
    
    def get_agent_states(self) -> List[Dict]:
        """
        Get states of all agents.
        
        Returns:
            List of agent state dictionaries
        """
        return [agent.get_state() for agent in self.agents]
    
    def reset(self):
        """Reset swarm to initial state."""
        for agent in self.agents:
            agent.reset()
        
        self.faulty_agents.clear()
        self.temp_history.clear()
        self.energy_history.clear()
        self.fault_events.clear()
        
        self.temps = np.array([agent.temperature for agent in self.agents])
        self.fan_speeds = np.array([agent.fan_speed for agent in self.agents])
        
        print("🔄 Swarm reset to initial state")
