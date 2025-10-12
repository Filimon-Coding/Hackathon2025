
import unittest
import numpy as np
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from data.datasets import CoolingDataset, DataGenerator

class TestCoolingDataset(unittest.TestCase):
    """Test cases for CoolingDataset class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.num_agents = 5
        self.time_steps = 100
        self.dataset = CoolingDataset(
            num_agents=self.num_agents,
            time_steps=self.time_steps,
            target_temp=25.0,
            ambient_temp=30.0
        )
    
    def test_initialization(self):
        """Test dataset initialization."""
        self.assertEqual(self.dataset.num_agents, self.num_agents)
        self.assertEqual(self.dataset.time_steps, self.time_steps)
        self.assertEqual(self.dataset.target_temp, 25.0)
        self.assertEqual(self.dataset.ambient_temp, 30.0)
    
    def test_generate_normal_data(self):
        """Test normal data generation."""
        data = self.dataset.generate_normal_data()
        
        self.assertIn('temperatures', data)
        self.assertIn('fan_speeds', data)
        self.assertIn('power_consumption', data)
        
        # Check shapes
        self.assertEqual(data['temperatures'].shape, (self.time_steps, self.num_agents))
        self.assertEqual(data['fan_speeds'].shape, (self.time_steps, self.num_agents))
        self.assertEqual(len(data['power_consumption']), self.time_steps)
    
    def test_generate_faulty_data(self):
        """Test faulty data generation."""
        fault_agent = 2
        fault_step = 50
        
        data = self.dataset.generate_faulty_data(
            fault_agent_id=fault_agent,
            fault_step=fault_step
        )
        
        self.assertIn('temperatures', data)
        self.assertIn('fault_info', data)
        
        # Check fault info
        self.assertEqual(data['fault_info']['agent_id'], fault_agent)
        self.assertEqual(data['fault_info']['fault_step'], fault_step)
        
        # Verify temperature spike at fault
        temp_before = data['temperatures'][fault_step - 1, fault_agent]
        temp_after = data['temperatures'][fault_step, fault_agent]
        self.assertGreater(temp_after, temp_before)
    
    def test_temperature_bounds(self):
        """Test that temperatures stay within reasonable bounds."""
        data = self.dataset.generate_normal_data()
        temps = data['temperatures']
        
        # Temperatures should be between 20°C and 35°C
        self.assertTrue(np.all(temps >= 20.0))
        self.assertTrue(np.all(temps <= 35.0))
    
    def test_fan_speed_bounds(self):
        """Test that fan speeds are normalized."""
        data = self.dataset.generate_normal_data()
        fan_speeds = data['fan_speeds']
        
        # Fan speeds should be between 0 and 1
        self.assertTrue(np.all(fan_speeds >= 0.0))
        self.assertTrue(np.all(fan_speeds <= 1.0))


class TestDataGenerator(unittest.TestCase):
    """Test cases for DataGenerator class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.generator = DataGenerator(
            num_agents=5,
            target_temp=25.0,
            ambient_temp=30.0
        )
    
    def test_initialization(self):
        """Test generator initialization."""
        self.assertEqual(self.generator.num_agents, 5)
        self.assertEqual(self.generator.target_temp, 25.0)
        self.assertEqual(self.generator.ambient_temp, 30.0)
    
    def test_generate_batch(self):
        """Test batch generation."""
        batch_size = 10
        time_steps = 50
        
        batch = self.generator.generate_batch(
            batch_size=batch_size,
            time_steps=time_steps
        )
        
        self.assertEqual(len(batch), batch_size)
        
        for sample in batch:
            self.assertIn('temperatures', sample)
            self.assertIn('fan_speeds', sample)
            self.assertEqual(sample['temperatures'].shape[0], time_steps)
    
    def test_generate_with_faults(self):
        """Test generation with fault injection."""
        batch = self.generator.generate_batch(
            batch_size=5,
            time_steps=100,
            fault_probability=1.0  # Ensure faults are injected
        )
        
        # Check that at least some samples have faults
        has_fault = any('fault_info' in sample for sample in batch)
        self.assertTrue(has_fault)
    
    def test_reproducibility(self):
        """Test that setting seed produces reproducible results."""
        gen1 = DataGenerator(num_agents=5, seed=42)
        gen2 = DataGenerator(num_agents=5, seed=42)
        
        batch1 = gen1.generate_batch(batch_size=3, time_steps=50)
        batch2 = gen2.generate_batch(batch_size=3, time_steps=50)
        
        # Compare first sample temperatures
        np.testing.assert_array_almost_equal(
            batch1[0]['temperatures'],
            batch2[0]['temperatures']
        )


if __name__ == '__main__':
    unittest.main()
