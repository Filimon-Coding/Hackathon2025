
"""
Base Agent class for the swarm cooling system.
"""

import numpy as np
from abc import ABC, abstractmethod


class BaseAgent(ABC):
    """
    Abstract base class for all agents in the swarm.
    
    Each agent maintains its own state and can communicate with neighbors.
    """
    
    def __init__(self, agent_id, initial_temp=25.0, initial_fan_speed=0.5):
        """
        Initialize a base agent.
        
        Args:
            agent_id: Unique identifier for this agent
            initial_temp: Starting temperature (°C)
            initial_fan_speed: Starting fan speed (0-1)
        """
        self.agent_id = agent_id
        self.temperature = initial_temp
        self.fan_speed = initial_fan_speed
        self.is_faulty = False
        self.energy_consumption = 0.0
        self.neighbors = []
        self.state_history = []
        
    def add_neighbor(self, neighbor):
        """Add a neighboring agent for communication."""
        if neighbor not in self.neighbors:
            self.neighbors.append(neighbor)
    
    def get_neighbor_temps(self):
        """Get temperatures from all neighbors."""
        return [n.temperature for n in self.neighbors if not n.is_faulty]
    
    def record_state(self):
        """Record current state to history."""
        self.state_history.append({
            'temperature': self.temperature,
            'fan_speed': self.fan_speed,
            'is_faulty': self.is_faulty,
            'energy': self.energy_consumption
        })
    
    @abstractmethod
    def update(self, target_temp, learning_rate, comm_weight):
        """Update agent state (must be implemented by subclasses)."""
        pass
    
    def __repr__(self):
        return f"Agent({self.agent_id}, T={self.temperature:.2f}°C, Fan={self.fan_speed:.2%})"
