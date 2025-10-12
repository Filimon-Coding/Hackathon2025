
import unittest
import numpy as np
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from models.anomaly_detector import AnomalyDetector, IsolationForestDetector, StatisticalDetector

class TestAnomalyDetector(unittest.TestCase):
    """Test cases for AnomalyDetector base class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.detector = AnomalyDetector(threshold=0.7)
    
    def test_initialization(self):
        """Test detector initialization."""
        self.assertEqual(self.detector.threshold, 0.7)
        self.assertFalse(self.detector.is_trained)
    
    def test_abstract_methods(self):
        """Test that abstract methods raise NotImplementedError."""
        with self.assertRaises(NotImplementedError):
            self.detector.train(np.array([]))
        
        with self.assertRaises(NotImplementedError):
            self.detector.detect(np.array([]))


class TestIsolationForestDetector(unittest.TestCase):
    """Test cases for IsolationForestDetector."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.detector = IsolationForestDetector(
            contamination=0.1,
            n_estimators=50
        )
        
        # Generate training data
        np.random.seed(42)
        self.normal_data = np.random.normal(25, 2, (100, 5))
        self.anomaly_data = np.random.normal(35, 5, (10, 5))
    
    def test_training(self):
        """Test model training."""
        self.detector.train(self.normal_data)
        self.assertTrue(self.detector.is_trained)
    
    def test_detection(self):
        """Test anomaly detection."""
        self.detector.train(self.normal_data)
        
        # Test normal data
        normal_scores = self.detector.detect(self.normal_data[:10])
        self.assertEqual(len(normal_scores), 10)
        
        # Test anomaly data
        anomaly_scores = self.detector.detect(self.anomaly_data)
        self.assertEqual(len(anomaly_scores), 10)
        
        # Anomalies should have higher scores
        self.assertGreater(np.mean(anomaly_scores), np.mean(normal_scores))
    
    def test_predict_anomalies(self):
        """Test binary anomaly prediction."""
        self.detector.train(self.normal_data)
        
        predictions = self.detector.predict_anomalies(self.anomaly_data)
        self.assertEqual(len(predictions), len(self.anomaly_data))
        
        # Should detect some anomalies
        self.assertGreater(np.sum(predictions), 0)
    
    def test_untrained_detection(self):
        """Test that detection fails when model is not trained."""
        with self.assertRaises(ValueError):
            self.detector.detect(self.normal_data)


class TestStatisticalDetector(unittest.TestCase):
    """Test cases for StatisticalDetector."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.detector = StatisticalDetector(
            window_size=10,
            n_sigma=3.0
        )
        
        # Generate time series data
        np.random.seed(42)
        self.normal_series = np.random.normal(25, 1, (100, 5))
        
        # Add anomalies
        self.anomaly_series = self.normal_series.copy()
        self.anomaly_series[50:55, 2] = 40  # Spike in agent 2
    
    def test_training(self):
        """Test statistical model training."""
        self.detector.train(self.normal_series)
        self.assertTrue(self.detector.is_trained)
        
        # Check that statistics are computed
        self.assertIsNotNone(self.detector.mean)
        self.assertIsNotNone(self.detector.std)
    
    def test_detection(self):
        """Test statistical anomaly detection."""
        self.detector.train(self.normal_series)
        
        scores = self.detector.detect(self.anomaly_series)
        self.assertEqual(len(scores), len(self.anomaly_series))
        
        # Anomaly region should have higher scores
        anomaly_region_scores = scores[50:55]
        normal_region_scores = scores[:40]
        
        self.assertGreater(np.mean(anomaly_region_scores), np.mean(normal_region_scores))
    
    def test_moving_average(self):
        """Test moving average calculation."""
        data = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
        window_size = 3
        
        ma = self.detector._moving_average(data, window_size)
        
        # Check length
        self.assertEqual(len(ma), len(data) - window_size + 1)
        
        # Check values
        expected = np.array([2, 3, 4, 5, 6, 7, 8, 9])
        np.testing.assert_array_almost_equal(ma, expected)
    
    def test_z_score_calculation(self):
        """Test z-score based anomaly detection."""
        self.detector.train(self.normal_series)
        
        # Test with extreme value
        extreme_data = np.array([[50, 50, 50, 50, 50]])
        scores = self.detector.detect(extreme_data)
        
        # Should detect as anomaly
        self.assertGreater(scores[0], self.detector.threshold)


if __name__ == '__main__':
    unittest.main()
