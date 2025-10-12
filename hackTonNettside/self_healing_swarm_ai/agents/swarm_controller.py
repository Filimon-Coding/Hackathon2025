
import numpy as np
from typing import List, Dict, Optional, Tuple
from .cooling_agent import CoolingAgent

class SwarmController:
    """
    Controller for managing a swarm of cooling agents.
    Implements distributed coordination and self-healing mechanisms.
    """
    
    def __init__(self, 
                 num_agents: int,
                 target_temp: float = 25.0,
                 communication_weight: float = 0.3,
                 topology: str = 'ring'):
        """
        Initialize the swarm controller.
        
        Args:
            num_agents: Number of cooling agents
            target_temp: Target temperature for the system
            communication_weight: Weight for neighbor communication
            topology: Network topology ('ring', 'mesh', 'star')
        """
        self.num_agents = num_agents
        self.target_temp = target_temp
        self.communication_weight = communication_weight
        self.topology = topology
        
        # Initialize agents
        self.agents = [
            CoolingAgent(
                agent_id=i,
                target_temp=target_temp,
                learning_rate=0.1
            ) for i in range(num_agents)
        ]
        
        # Setup network topology
        self.neighbor_map = self._setup_topology()
        
        # Metrics tracking
        self.step_count = 0
        self.history = {
            'temperatures': [],
            'fan_speeds': [],
            'power_consumption': [],
            'faults': []
        }
    
    def _setup_topology(self) -> Dict[int, List[int]]:
        """
        Setup network topology for agent communication.
        
        Returns:
            Dictionary mapping agent IDs to their neighbors
        """
        neighbor_map = {}
        
        if self.topology == 'ring':
            # Ring topology: each agent connected to 2 neighbors
            for i in range(self.num_agents):
                left = (i - 1) % self.num_agents
                right = (i + 1) % self.num_agents
                neighbor_map[i] = [left, right]
        
        elif self.topology == 'mesh':
            # Mesh topology: all agents connected to all others
            for i in range(self.num_agents):
                neighbor_map[i] = [j for j in range(self.num_agents) if j != i]
        
        elif self.topology == 'star':
            # Star topology: all agents connected to agent 0
            neighbor_map[0] = list(range(1, self.num_agents))
            for i in range(1, self.num_agents):
                neighbor_map[i] = [0]
        
        else:
            raise ValueError(f"Unknown topology: {self.topology}")
        
        return neighbor_map
    
    def get_neighbors(self, agent_id: int) -> List[int]:
        """
        Get neighbors for a specific agent.
        
        Args:
            agent_id: ID of the agent
            
        Returns:
            List of neighbor agent IDs
        """
        return self.neighbor_map.get(agent_id, [])
    
    def get_neighbor_temperatures(self, agent_id: int) -> List[float]:
        """
        Get temperatures of neighboring agents.
        
        Args:
            agent_id: ID of the agent
            
        Returns:
            List of neighbor temperatures
        """
        neighbors = self.get_neighbors(agent_id)
        return [self.agents[n].current_temp for n in neighbors if self.agents[n].is_active]
    
    def step(self, ambient_temp: float, time_step: float = 0.1):
        """
        Execute one simulation step for all agents.
        
        Args:
            ambient_temp: Ambient temperature
            time_step: Time step size
        """
        # Collect neighbor information for all agents
        neighbor_info = {}
        for i in range(self.num_agents):
            neighbor_temps = self.get_neighbor_temperatures(i)
            neighbor_info[i] = neighbor_temps
        
        # Update all agents
        for i, agent in enumerate(self.agents):
            if not agent.is_active:
                continue
            
            # Apply neighbor influence
            if neighbor_info[i]:
                avg_neighbor_temp = np.mean(neighbor_info[i])
                neighbor_effect = self.communication_weight * (avg_neighbor_temp - agent.current_temp)
                agent.current_temp += neighbor_effect * time_step
            
            # Update agent state
            agent.update_temperature(ambient_temp, time_step)
            agent.adjust_fan_speed()
            
            # Self-healing: detect and compensate for faulty neighbors
            self._apply_self_healing(i, neighbor_info[i])
        
        # Record metrics
        self._record_metrics()
        self.step_count += 1
    
    def _apply_self_healing(self, agent_id: int, neighbor_temps: List[float]):
        """
        Apply self-healing mechanism for faulty neighbors.
        
        Args:
            agent_id: ID of the current agent
            neighbor_temps: Temperatures of neighbors
        """
        agent = self.agents[agent_id]
        neighbors = self.get_neighbors(agent_id)
        
        # Check for faulty neighbors
        for neighbor_id in neighbors:
            neighbor = self.agents[neighbor_id]
            
            if neighbor.is_faulty:
                # Increase fan speed to compensate
                compensation = 0.15
                agent.fan_speed = min(1.0, agent.fan_speed + compensation)
    
    def detect_faulty_agents(self) -> List[int]:
        """
        Detect faulty agents in the swarm.
        
        Returns:
            List of faulty agent IDs
        """
        return [i for i, agent in enumerate(self.agents) if agent.is_faulty]
    
    def get_system_metrics(self) -> Dict[str, float]:
        """
        Calculate system-wide metrics.
        
        Returns:
            Dictionary of system metrics
        """
        active_agents = [a for a in self.agents if a.is_active]
        
        if not active_agents:
            return {
                'avg_temperature': 0.0,
                'total_power': 0.0,
                'temperature_variance': 0.0,
                'num_faulty_agents': 0,
                'num_active_agents': 0
            }
        
        temps = [a.current_temp for a in active_agents]
        powers = [a.calculate_power_consumption() for a in active_agents]
        
        return {
            'avg_temperature': np.mean(temps),
            'total_power': np.sum(powers),
            'temperature_variance': np.var(temps),
            'num_faulty_agents': len(self.detect_faulty_agents()),
            'num_active_agents': len(active_agents),
            'max_temperature': np.max(temps),
            'min_temperature': np.min(temps)
        }
    
    def _record_metrics(self):
        """Record current system state to history."""
        temps = [agent.current_temp for agent in self.agents]
        fan_speeds = [agent.fan_speed for agent in self.agents]
        power = sum(agent.calculate_power_consumption() for agent in self.agents)
        
        self.history['temperatures'].append(temps)
        self.history['fan_speeds'].append(fan_speeds)
        self.history['power_consumption'].append(power)
        self.history['faults'].append(self.detect_faulty_agents())
    
    def reset(self):
        """Reset the swarm to initial state."""
        for agent in self.agents:
            agent.recover_from_fault()
            agent.current_temp = np.random.uniform(23, 27)
            agent.fan_speed = np.random.uniform(0.3, 0.7)
            agent.is_active = True
        
        self.step_count = 0
        self.history = {
            'temperatures': [],
            'fan_speeds': [],
            'power_consumption': [],
            'faults': []
        }
    
    def inject_fault(self, agent_id: int, fault_type: str = 'temperature_spike'):
        """
        Inject a fault into a specific agent.
        
        Args:
            agent_id: ID of the agent to fault
            fault_type: Type of fault to inject
        """
        if 0 <= agent_id < self.num_agents:
            self.agents[agent_id].inject_fault(fault_type)
    
    def get_history(self) -> Dict[str, List]:
        """
        Get simulation history.
        
        Returns:
            Dictionary containing historical data
        """
        return self.history
    
    def export_state(self) -> Dict:
        """
        Export current state of all agents.
        
        Returns:
            Dictionary containing agent states
        """
        return {
            'step_count': self.step_count,
            'agents': [agent.get_state() for agent in self.agents],
            'metrics': self.get_system_metrics()
        }
