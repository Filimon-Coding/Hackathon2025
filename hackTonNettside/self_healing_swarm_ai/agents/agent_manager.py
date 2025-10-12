
import numpy as np
from typing import Dict, List, Optional
from datetime import datetime
from agents.cooling_agent import CoolingAgent
from models.swarm_coordinator import SwarmCoordinator

class AgentManager:
    """
    Orchestrates all cooling agents and manages system-level operations.
    Handles agent initialization, updates, and metric aggregation.
    """
    
    def __init__(self, config: Dict, anomaly_detector, adaptive_controller, swarm_coordinator: SwarmCoordinator):
        self.config = config
        self.anomaly_detector = anomaly_detector
        self.adaptive_controller = adaptive_controller
        self.swarm_coordinator = swarm_coordinator
        
        self.num_agents = config['system']['num_agents']
        self.target_temp = config['system']['target_temp']
        
        # Initialize agents
        self.agents: List[CoolingAgent] = []
        self._initialize_agents()
        
        # System metrics
        self.system_metrics = {
            'avg_temperature': [],
            'total_power': [],
            'num_faults': [],
            'temperature_variance': [],
            'energy_efficiency': []
        }
        
        self.timestep = 0
        
    def _initialize_agents(self):
        """Create and initialize all cooling agents."""
        print(f"Initializing {self.num_agents} cooling agents...")
        
        for agent_id in range(self.num_agents):
            agent = CoolingAgent(
                agent_id=agent_id,
                config=self.config,
                anomaly_detector=self.anomaly_detector,
                adaptive_controller=self.adaptive_controller
            )
            
            # Set neighbors from topology
            agent.neighbors = self.swarm_coordinator.neighbors.get(agent_id, [])
            
            self.agents.append(agent)
        
        print(f"✅ Initialized {len(self.agents)} agents")
    
    def step(self, inject_fault: bool = False, fault_agent_id: Optional[int] = None) -> Dict:
        """
        Execute one simulation timestep for all agents.
        
        Args:
            inject_fault: Whether to inject a fault this step
            fault_agent_id: Specific agent to fault (random if None)
            
        Returns:
            Dict of system metrics for this timestep
        """
        self.timestep += 1
        
        # Inject fault if specified
        if inject_fault:
            if fault_agent_id is None:
                fault_agent_id = np.random.randint(0, self.num_agents)
            self.agents[fault_agent_id].is_faulty = True
            self.agents[fault_agent_id].report_fault('injected_fault', severity=0.8)
            print(f"💥 Fault injected in Agent {fault_agent_id} at timestep {self.timestep}")
        
        # 1. SENSE: All agents collect sensor data
        sensor_readings = []
        for agent in self.agents:
            reading = agent.sense()
            sensor_readings.append(reading)
        
        # 2. DETECT: Check for anomalies
        for i, agent in enumerate(self.agents):
            if agent.is_active:
                agent.detect_fault(sensor_readings[i])
        
        # 3. COORDINATE: Get swarm coordination signals
        agent_states = [agent.get_state_dict() for agent in self.agents]
        coordination_signals = self.swarm_coordinator.predict(agent_states)
        
        # 4. CONTROL: Each agent computes control action
        for i, agent in enumerate(self.agents):
            if agent.is_active:
                agent.control(self.target_temp, coordination_signals[i])
        
        # 5. COOPERATE: Agents share information
        for agent in self.agents:
            if agent.is_active:
                neighbor_states = [self.agents[n].get_state_dict() for n in agent.neighbors]
                message = agent.cooperate(neighbor_states)
                
                # Process cooperation messages
                if message.get('needs_help', False):
                    self._redistribute_load(agent.agent_id, neighbor_states)
        
        # 6. HEAL: Attempt self-healing for faulty agents
        for agent in self.agents:
            if agent.is_faulty:
                healed = agent.heal_self()
                if healed:
                    print(f"✅ Agent {agent.agent_id} successfully healed")
        
        # 7. UPDATE: Update physical states
        for agent in self.agents:
            if agent.is_active:
                agent.update_state(dt=self.config['system']['time_step_duration'])
        
        # 8. AGGREGATE: Update system metrics
        self._update_system_metrics(sensor_readings)
        
        # Return current metrics
        return {
            'timestep': self.timestep,
            'avg_temperature': self.system_metrics['avg_temperature'][-1],
            'total_power': self.system_metrics['total_power'][-1],
            'num_faults': self.system_metrics['num_faults'][-1],
            'temperature_variance': self.system_metrics['temperature_variance'][-1],
            'energy_efficiency': self.system_metrics['energy_efficiency'][-1]
        }
    
    def _redistribute_load(self, faulty_agent_id: int, neighbor_states: List[Dict]):
        """
        Redistribute load from faulty agent to healthy neighbors.
        
        Args:
            faulty_agent_id: ID of agent that needs help
            neighbor_states: States of neighboring agents
        """
        faulty_agent = self.agents[faulty_agent_id]
        load_to_transfer = faulty_agent.load
        
        # Find healthy neighbors
        healthy_neighbors = [
            self.agents[n['agent_id']] 
            for n in neighbor_states 
            if not n.get('is_faulty', False)
        ]
        
        if healthy_neighbors:
            load_per_neighbor = load_to_transfer / len(healthy_neighbors)
            
            for neighbor in healthy_neighbors:
                neighbor.load += load_per_neighbor
                neighbor.load = min(neighbor.load, 1.0)  # Cap at 100%
            
            faulty_agent.load = 0.1  # Minimal load
            print(f"🔄 Load redistributed from Agent {faulty_agent_id} to {len(healthy_neighbors)} neighbors")
    
    def _update_system_metrics(self, sensor_readings: List[Dict]):
        """
        Aggregate and store system-level metrics.
        
        Args:
            sensor_readings: List of sensor readings from all agents
        """
        temperatures = [r['temperature'] for r in sensor_readings]
        powers = [r['power'] for r in sensor_readings]
        
        self.system_metrics['avg_temperature'].append(np.mean(temperatures))
        self.system_metrics['total_power'].append(np.sum(powers))
        self.system_metrics['temperature_variance'].append(np.var(temperatures))
        
        # Count faults
        num_faults = sum(1 for agent in self.agents if agent.is_faulty)
        self.system_metrics['num_faults'].append(num_faults)
        
        # Calculate energy efficiency (cooling per watt)
        temp_error = np.mean([abs(t - self.target_temp) for t in temperatures])
        total_power = np.sum(powers)
        efficiency = 1.0 / (temp_error * total_power + 1e-8)
        self.system_metrics['energy_efficiency'].append(efficiency)
        
        # Trim metrics to keep window size reasonable
        for key in self.system_metrics:
            if len(self.system_metrics[key]) > 1000:
                self.system_metrics[key] = self.system_metrics[key][-1000:]
    
    def get_agent_status(self) -> List[Dict]:
        """
        Return detailed status of all agents.
        
        Returns:
            List of agent status dictionaries
        """
        return [agent.get_state_dict() for agent in self.agents]
    
    def get_system_summary(self) -> Dict:
        """
        Get high-level system summary.
        
        Returns:
            Dict with system-wide statistics
        """
        if not self.system_metrics['avg_temperature']:
            return {}
        
        return {
            'timestep': self.timestep,
            'num_agents': self.num_agents,
            'active_agents': sum(1 for a in self.agents if a.is_active),
            'faulty_agents': sum(1 for a in self.agents if a.is_faulty),
            'avg_temperature': self.system_metrics['avg_temperature'][-1],
            'target_temperature': self.target_temp,
            'total_power': self.system_metrics['total_power'][-1],
            'temperature_variance': self.system_metrics['temperature_variance'][-1],
            'energy_efficiency': self.system_metrics['energy_efficiency'][-1],
            'total_faults_detected': sum(len(a.fault_history) for a in self.agents)
        }
    
    def reset(self):
        """Reset all agents and metrics."""
        self.timestep = 0
        self.system_metrics = {
            'avg_temperature': [],
            'total_power': [],
            'num_faults': [],
            'temperature_variance': [],
            'energy_efficiency': []
        }
        
        # Reinitialize agents
        self.agents.clear()
        self._initialize_agents()
        
        print("🔄 System reset complete")
    
    def save_state(self, filepath: str):
        """
        Save current system state to file.
        
        Args:
            filepath: Path to save state
        """
        import pickle
        
        state = {
            'timestep': self.timestep,
            'agents': [a.get_state_dict() for a in self.agents],
            'metrics': self.system_metrics
        }
        
        with open(filepath, 'wb') as f:
            pickle.dump(state, f)
        
        print(f"💾 System state saved to {filepath}")
    
    def load_state(self, filepath: str):
        """
        Load system state from file.
        
        Args:
            filepath: Path to load state from
        """
        import pickle
        
        with open(filepath, 'rb') as f:
            state = pickle.load(f)
        
        self.timestep = state['timestep']
        self.system_metrics = state['metrics']
        
        # Restore agent states
        for i, agent_state in enumerate(state['agents']):
            if i < len(self.agents):
                self.agents[i].load = agent_state['load']
                self.agents[i].current_temp = agent_state['temperature']
                self.agents[i].current_power = agent_state['power']
                self.agents[i].is_faulty = agent_state['is_faulty']
                self.agents[i].is_active = agent_state['is_active']
                self.agents[i].last_control_action = agent_state['control_action']
        
        print(f"📂 System state loaded from {filepath}")
