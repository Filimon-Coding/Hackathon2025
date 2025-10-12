
import unittest
import numpy as np
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from agents.cooling_agent import CoolingAgent
from agents.swarm_controller import SwarmController

class TestCoolingAgent(unittest.TestCase):
    """Test cases for CoolingAgent class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.agent = CoolingAgent(
            agent_id=0,
            target_temp=25.0,
            learning_rate=0.1
        )
    
    def test_initialization(self):
        """Test agent initialization."""
        self.assertEqual(self.agent.agent_id, 0)
        self.assertEqual(self.agent.target_temp, 25.0)
        self.assertEqual(self.agent.learning_rate, 0.1)
        self.assertFalse(self.agent.is_faulty)
        self.assertTrue(self.agent.is_active)
    
    def test_temperature_update(self):
        """Test temperature update logic."""
        initial_temp = 28.0
        self.agent.current_temp = initial_temp
        self.agent.fan_speed = 0.5
        
        # Update temperature
        self.agent.update_temperature(ambient_temp=30.0, time_step=0.1)
        
        # Temperature should change
        self.assertNotEqual(self.agent.current_temp, initial_temp)
    
    def test_fan_speed_adjustment(self):
        """Test fan speed adjustment based on temperature."""
        self.agent.current_temp = 28.0
        initial_fan_speed = self.agent.fan_speed
        
        # Adjust fan speed
        self.agent.adjust_fan_speed()
        
        # Fan speed should increase when temp > target
        self.assertGreaterEqual(self.agent.fan_speed, initial_fan_speed)
    
    def test_fault_injection(self):
        """Test fault injection."""
        self.agent.inject_fault(fault_type='temperature_spike')
        
        self.assertTrue(self.agent.is_faulty)
        self.assertIsNotNone(self.agent.fault_type)
    
    def test_fault_recovery(self):
        """Test fault recovery."""
        self.agent.inject_fault(fault_type='sensor_failure')
        self.assertTrue(self.agent.is_faulty)
        
        self.agent.recover_from_fault()
        self.assertFalse(self.agent.is_faulty)
        self.assertIsNone(self.agent.fault_type)
    
    def test_neighbor_communication(self):
        """Test communication with neighbors."""
        neighbor_temps = [24.0, 26.0, 25.5]
        
        avg_neighbor_temp = self.agent.get_neighbor_average(neighbor_temps)
        
        expected_avg = np.mean(neighbor_temps)
        self.assertAlmostEqual(avg_neighbor_temp, expected_avg)
    
    def test_power_consumption(self):
        """Test power consumption calculation."""
        self.agent.fan_speed = 0.5
        
        power = self.agent.calculate_power_consumption()
        
        # Power should be positive
        self.assertGreater(power, 0)
        
        # Higher fan speed should consume more power
        self.agent.fan_speed = 0.8
        higher_power = self.agent.calculate_power_consumption()
        self.assertGreater(higher_power, power)
    
    def test_state_export(self):
        """Test state export."""
        state = self.agent.get_state()
        
        self.assertIn('agent_id', state)
        self.assertIn('current_temp', state)
        self.assertIn('fan_speed', state)
        self.assertIn('is_faulty', state)
        self.assertIn('is_active', state)


class TestSwarmController(unittest.TestCase):
    """Test cases for SwarmController class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.num_agents = 5
        self.controller = SwarmController(
            num_agents=self.num_agents,
            target_temp=25.0,
            communication_weight=0.3
        )
    
    def test_initialization(self):
        """Test controller initialization."""
        self.assertEqual(len(self.controller.agents), self.num_agents)
        self.assertEqual(self.controller.target_temp, 25.0)
        self.assertEqual(self.controller.communication_weight, 0.3)
    
    def test_neighbor_topology(self):
        """Test neighbor topology setup."""
        # Check that each agent has neighbors
        for agent_id in range(self.num_agents):
            neighbors = self.controller.get_neighbors(agent_id)
            self.assertGreater(len(neighbors), 0)
            self.assertLessEqual(len(neighbors), self.num_agents - 1)
    
    def test_step_simulation(self):
        """Test single simulation step."""
        initial_temps = [agent.current_temp for agent in self.controller.agents]
        
        self.controller.step(ambient_temp=30.0)
        
        final_temps = [agent.current_temp for agent in self.controller.agents]
        
        # Temperatures should change
        self.assertFalse(np.array_equal(initial_temps, final_temps))
    
    def test_fault_detection(self):
        """Test fault detection in swarm."""
        # Inject fault
        fault_agent_id = 2
        self.controller.agents[fault_agent_id].inject_fault('temperature_spike')
        
        # Detect faults
        faulty_agents = self.controller.detect_faulty_agents()
        
        self.assertIn(fault_agent_id, faulty_agents)
    
    def test_load_balancing(self):
        """Test load balancing among agents."""
        # Create imbalanced load
        self.controller.agents[0].current_temp = 30.0
        self.controller.agents[1].current_temp = 22.0
        
        initial_variance = np.var([agent.current_temp for agent in self.controller.agents])
        
        # Run multiple steps
        for _ in range(50):
            self.controller.step(ambient_temp=28.0)
        
        final_variance = np.var([agent.current_temp for agent in self.controller.agents])
        
        # Variance should decrease (temperatures converge)
        self.assertLess(final_variance, initial_variance)
    
    def test_self_healing(self):
        """Test self-healing behavior."""
        fault_agent_id = 2
        
        # Inject fault
        self.controller.agents[fault_agent_id].inject_fault('cooling_failure')
        self.controller.agents[fault_agent_id].current_temp = 35.0
        
        # Get neighbors
        neighbors = self.controller.get_neighbors(fault_agent_id)
        
        # Run simulation
        for _ in range(100):
            self.controller.step(ambient_temp=30.0)
        
        # Neighbors should compensate
        neighbor_fan_speeds = [self.controller.agents[n].fan_speed for n in neighbors]
        avg_neighbor_speed = np.mean(neighbor_fan_speeds)
        
        # Neighbors should have increased fan speeds
        self.assertGreater(avg_neighbor_speed, 0.5)
    
    def test_system_metrics(self):
        """Test system-wide metrics calculation."""
        metrics = self.controller.get_system_metrics()
        
        self.assertIn('avg_temperature', metrics)
        self.assertIn('total_power', metrics)
        self.assertIn('temperature_variance', metrics)
        self.assertIn('num_faulty_agents', metrics)
        self.assertIn('num_active_agents', metrics)
    
    def test_reset(self):
        """Test system reset."""
        # Modify system state
        self.controller.agents[0].inject_fault('sensor_failure')
        self.controller.step(ambient_temp=30.0)
        
        # Reset
        self.controller.reset()
        
        # Check all agents are healthy and at initial state
        for agent in self.controller.agents:
            self.assertFalse(agent.is_faulty)
            self.assertTrue(agent.is_active)


if __name__ == '__main__':
    unittest.main()
