
import unittest
import numpy as np
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../self_healing_swarm_ai')))

from agents.swarm_controller import SwarmController

from agents.cooling_agent import CoolingAgent

class TestSwarmCooperation(unittest.TestCase):
    """Test cases for swarm cooperation behaviors."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.num_agents = 6
        self.controller = SwarmController(
            num_agents=self.num_agents,
            target_temp=25.0,
            communication_weight=0.5
        )
    
    def test_information_sharing(self):
        """Test that agents share information with neighbors."""
        agent_id = 0
        neighbors = self.controller.get_neighbors(agent_id)
        
        # Set different temperatures
        self.controller.agents[agent_id].current_temp = 30.0
        for neighbor_id in neighbors:
            self.controller.agents[neighbor_id].current_temp = 24.0
        
        # Get neighbor information
        neighbor_temps = self.controller.get_neighbor_temperatures(agent_id)
        
        self.assertEqual(len(neighbor_temps), len(neighbors))
        self.assertTrue(all(temp == 24.0 for temp in neighbor_temps))
    
    def test_consensus_reaching(self):
        """Test that swarm reaches temperature consensus."""
        # Set random initial temperatures
        np.random.seed(42)
        for agent in self.controller.agents:
            agent.current_temp = np.random.uniform(22, 30)
        
        initial_std = np.std([agent.current_temp for agent in self.controller.agents])
        
        # Run simulation
        for _ in range(200):
            self.controller.step(ambient_temp=27.0)
        
        final_std = np.std([agent.current_temp for agent in self.controller.agents])
        
        # Standard deviation should decrease
        self.assertLess(final_std, initial_std)
        
        # Temperatures should be close to target
        avg_temp = np.mean([agent.current_temp for agent in self.controller.agents])
        self.assertAlmostEqual(avg_temp, self.controller.target_temp, delta=2.0)
    
    def test_cooperative_fault_handling(self):
        """Test cooperative response to fault."""
        fault_agent_id = 3
        neighbors = self.controller.get_neighbors(fault_agent_id)
        
        # Record initial neighbor fan speeds
        initial_speeds = {n: self.controller.agents[n].fan_speed for n in neighbors}
        
        # Inject fault
        self.controller.agents[fault_agent_id].inject_fault('cooling_failure')
        self.controller.agents[fault_agent_id].current_temp = 35.0
        
        # Run simulation
        for _ in range(50):
            self.controller.step(ambient_temp=30.0)
        
        # Check neighbor response
        final_speeds = {n: self.controller.agents[n].fan_speed for n in neighbors}
        
        # At least some neighbors should increase fan speed
        increased = sum(1 for n in neighbors if final_speeds[n] > initial_speeds[n])
        self.assertGreater(increased, 0)
    
    def test_distributed_load_balancing(self):
        """Test distributed load balancing."""
        # Create hotspot
        hotspot_id = 2
        self.controller.agents[hotspot_id].current_temp = 32.0
        
        # Run simulation
        for _ in range(100):
            self.controller.step(ambient_temp=25.0)
        
        # Check that workload is distributed
        temps = [agent.current_temp for agent in self.controller.agents]
        std_dev = np.std(temps)
        
        # Standard deviation should be lower than initial
        self.assertLess(std_dev, 3.0)
