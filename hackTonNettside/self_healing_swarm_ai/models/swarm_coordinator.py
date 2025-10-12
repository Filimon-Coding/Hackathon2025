
import numpy as np
from typing import Dict, List, Tuple, Optional
import json
from pathlib import Path

class SwarmCoordinator:
    """
    Multi-agent coordination using swarm intelligence and game theory.
    Implements consensus algorithms and cooperative optimization.
    """
    
    def __init__(self, config: Dict, topology_file: str = "config/swarm_topology.json"):
        self.config = config
        self.swarm_config = config['swarm_coordination']
        
        # Load topology
        with open(topology_file, 'r') as f:
            self.topology = json.load(f)
        
        self.num_agents = self.topology['num_agents']
        self.adjacency_matrix = np.array(self.topology['adjacency_matrix'])
        self.consensus_iterations = self.swarm_config['consensus_iterations']
        self.cooperation_radius = self.swarm_config['cooperation_radius']
        self.load_balancing_weight = self.swarm_config['load_balancing_weight']
        
        # Communication graph
        self.neighbors = self._build_neighbor_list()
        
    def _build_neighbor_list(self) -> Dict[int, List[int]]:
        """Build neighbor list from adjacency matrix."""
        neighbors = {}
        for i in range(self.num_agents):
            neighbors[i] = [j for j in range(self.num_agents) if self.adjacency_matrix[i, j] == 1]
        return neighbors
    
    def train(self, historical_interactions: Optional[np.ndarray] = None):
        """
        Train coordination strategies from historical multi-agent interactions.
        
        Args:
            historical_interactions: Optional historical data
        """
        # In a full implementation, this could learn optimal cooperation weights
        print("Swarm coordinator initialized with topology:", self.topology['topology_type'])
    
    def predict(self, agent_states: List[Dict]) -> List[Dict]:
        """
        Compute coordinated actions for all agents using consensus.
        
        Args:
            agent_states: List of agent state dicts with 'temperature', 'fan_speed', etc.
            
        Returns:
            List of coordination signals for each agent
        """
        coordination_signals = []
        
        for agent_id in range(self.num_agents):
            signal = self._compute_coordination_signal(agent_id, agent_states)
            coordination_signals.append(signal)
        
        return coordination_signals
    
    def _compute_coordination_signal(self, agent_id: int, agent_states: List[Dict]) -> Dict:
        """
        Compute coordination signal for a specific agent.
        
        Args:
            agent_id: Agent identifier
            agent_states: All agent states
            
        Returns:
            Coordination signal dict
        """
        my_state = agent_states[agent_id]
        neighbors = self.neighbors[agent_id]
        
        if not neighbors:
            return {'load_adjustment': 0.0, 'consensus_temp': my_state['temperature']}
        
        # Consensus on temperature
        neighbor_temps = [agent_states[n]['temperature'] for n in neighbors]
        consensus_temp = np.mean(neighbor_temps + [my_state['temperature']])
        
        # Load balancing
        neighbor_loads = [agent_states[n].get('load', 0.5) for n in neighbors]
        my_load = my_state.get('load', 0.5)
        avg_load = np.mean(neighbor_loads)
        
        load_adjustment = self.load_balancing_weight * (avg_load - my_load)
        
        # Cooperative cooling: if neighbor is overheating, increase my cooling
        max_neighbor_temp = max(neighbor_temps) if neighbor_temps else my_state['temperature']
        cooperation_signal = 0.0
        
        if max_neighbor_temp > self.config['system']['target_temp'] + 2.0:
            cooperation_signal = 0.1  # Increase cooling to help neighbors
        
        return {
            'load_adjustment': load_adjustment,
            'consensus_temp': consensus_temp,
            'cooperation_signal': cooperation_signal,
            'neighbor_temps': neighbor_temps
        }
    
    def update(self, performance_metrics: List[float]):
        """
        Update coordination parameters based on system performance.
        
        Args:
            performance_metrics: Performance metric for each agent
        """
        # Adapt cooperation weights based on system-wide performance
        avg_performance = np.mean(performance_metrics)
        
        if avg_performance > 1.5:  # Poor coordination
            self.load_balancing_weight = min(1.0, self.load_balancing_weight * 1.1)
        elif avg_performance < 0.5:  # Good coordination
            self.load_balancing_weight = max(0.1, self.load_balancing_weight * 0.95)
    
    def detect_network_partition(self, agent_states: List[Dict]) -> bool:
        """
        Detect if the communication network has been partitioned.
        
        Args:
            agent_states: All agent states
            
        Returns:
            True if partition detected
        """
        # Simple connectivity check using BFS
        visited = set()
        queue = [0]
        visited.add(0)
        
        while queue:
            current = queue.pop(0)
            for neighbor in self.neighbors[current]:
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append(neighbor)
        
        return len(visited) < self.num_agents
    
    def compute_nash_equilibrium(self, agent_states: List[Dict]) -> List[float]:
        """
        Compute Nash equilibrium for competitive-cooperative game.
        
        Args:
            agent_states: All agent states
            
        Returns:
            Equilibrium fan speeds for all agents
        """
        # Simplified Nash equilibrium computation
        # In practice, this would solve a game-theoretic optimization
        
        equilibrium_speeds = []
        target_temp = self.config['system']['target_temp']
        
        for agent_id, state in enumerate(agent_states):
            temp_error = state['temperature'] - target_temp
            
            # Consider neighbors' actions
            neighbor_speeds = [agent_states[n]['fan_speed'] for n in self.neighbors[agent_id]]
            avg_neighbor_speed = np.mean(neighbor_speeds) if neighbor_speeds else 0.5
            
            # Best response: balance own cooling need with coordination
            own_need = 0.5 + 0.3 * temp_error
            coordination_term = 0.3 * avg_neighbor_speed
            
            equilibrium_speed = np.clip(own_need + coordination_term, 0.0, 1.0)
            equilibrium_speeds.append(equilibrium_speed)
        
        return equilibrium_speeds
