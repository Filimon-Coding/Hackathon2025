
"""
Anomaly Detection using Isolation Forest.
"""

import numpy as np
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler
import joblib
from pathlib import Path
from typing import Optional


class AnomalyDetector:
    """
    ML-based anomaly detector for identifying faulty cooling agents.
    Uses Isolation Forest algorithm for unsupervised anomaly detection.
    """
    
    def __init__(self, contamination: float = 0.1, random_state: int = 42):
        """
        Initialize anomaly detector.
        
        Args:
            contamination: Expected proportion of anomalies (0-0.5)
            random_state: Random seed for reproducibility
        """
        self.model = IsolationForest(
            contamination=contamination,
            random_state=random_state,
            n_estimators=100
        )
        self.scaler = StandardScaler()
        self.is_trained = False
        self.feature_names = ['temperature', 'humidity', 'power', 'fan_speed']
    
    def train(self, X: np.ndarray):
        """
        Train the anomaly detector on normal operating data.
        
        Args:
            X: Training data (n_samples, n_features)
        """
        print("🔄 Training anomaly detector...")
        
        # Normalize features
        X_scaled = self.scaler.fit_transform(X)
        
        # Train model
        self.model.fit(X_scaled)
        self.is_trained = True
        
        print(f"✅ Anomaly detector trained on {len(X)} samples")
    
    def predict(self, X: np.ndarray) -> np.ndarray:
        """
        Predict anomalies in new data.
        
        Args:
            X: Input data (n_samples, n_features)
            
        Returns:
            Predictions: 1 for normal, -1 for anomaly
        """
        if not self.is_trained:
            raise ValueError("Model must be trained before prediction")
        
        X_scaled = self.scaler.transform(X)
        predictions = self.model.predict(X_scaled)
        
        return predictions
    
    def get_anomaly_scores(self, X: np.ndarray) -> np.ndarray:
        """
        Get anomaly scores (lower = more anomalous).
        
        Args:
            X: Input data
            
        Returns:
            Anomaly scores
        """
        if not self.is_trained:
            raise ValueError("Model must be trained before scoring")
        
        X_scaled = self.scaler.transform(X)
        scores = self.model.score_samples(X_scaled)
        
        return scores


import numpy as np
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler
from typing import Dict, List, Tuple, Optional
import pickle
from pathlib import Path

class ArtificialImmuneSystem:
    """
    Artificial Immune System (AIS) for anomaly detection.
    Inspired by biological immune systems to detect abnormal patterns.
    """
    
    def __init__(self, config: Dict):
        self.config = config
        self.detectors = []
        self.self_radius = 0.1
        self.detection_threshold = config['anomaly_detection']['fault_threshold']
        self.scaler = StandardScaler()
        
    def train(self, normal_data: np.ndarray):
        """
        Train the AIS by generating detectors that don't match normal patterns.
        
        Args:
            normal_data: Array of normal operating conditions
        """
        # Normalize data
        self.scaler.fit(normal_data)
        normalized_data = self.scaler.transform(normal_data)
        
        # Generate random detectors
        num_detectors = 100
        feature_dim = normalized_data.shape[1]
        
        for _ in range(num_detectors):
            # Generate random detector
            detector = np.random.randn(feature_dim)
            
            # Check if detector matches any normal pattern
            matches_self = False
            for sample in normalized_data:
                distance = np.linalg.norm(detector - sample)
                if distance < self.self_radius:
                    matches_self = True
                    break
            
            # Keep detector if it doesn't match normal patterns
            if not matches_self:
                self.detectors.append(detector)
        
        print(f"AIS trained with {len(self.detectors)} detectors")
    
    def predict(self, data: np.ndarray) -> np.ndarray:
        """
        Detect anomalies in new data.
        
        Args:
            data: Array of sensor readings
            
        Returns:
            Array of anomaly scores (higher = more anomalous)
        """
        normalized_data = self.scaler.transform(data)
        anomaly_scores = []
        
        for sample in normalized_data:
            # Calculate minimum distance to any detector
            min_distance = float('inf')
            for detector in self.detectors:
                distance = np.linalg.norm(sample - detector)
                min_distance = min(min_distance, distance)
            
            # Lower distance to detector = higher anomaly score
            anomaly_score = 1.0 / (min_distance + 1e-6)
            anomaly_scores.append(anomaly_score)
        
        return np.array(anomaly_scores)
    
    def update(self, new_data: np.ndarray, labels: np.ndarray):
        """
        Update detectors based on new observations.
        
        Args:
            new_data: New sensor readings
            labels: True labels (0=normal, 1=anomaly)
        """
        # Add confirmed normal patterns to self
        normal_samples = new_data[labels == 0]
        if len(normal_samples) > 0:
            # Update scaler with new normal data
            combined_data = np.vstack([self.scaler.mean_.reshape(1, -1), normal_samples])
            self.scaler.partial_fit(combined_data)


class IsolationForestDetector:
    """
    Isolation Forest-based anomaly detector.
    Efficient for high-dimensional data and online learning.
    """
    
    def __init__(self, config: Dict):
        self.config = config
        ad_config = config['anomaly_detection']
        
        self.model = IsolationForest(
            contamination=ad_config['contamination'],
            n_estimators=ad_config['n_estimators'],
            max_samples=ad_config['max_samples'],
            random_state=42
        )
        self.scaler = StandardScaler()
        self.is_trained = False
    
    def train(self, normal_data: np.ndarray):
        """
        Train the Isolation Forest on normal operating data.
        
        Args:
            normal_data: Array of normal sensor readings
        """
        # Normalize data
        self.scaler.fit(normal_data)
        normalized_data = self.scaler.transform(normal_data)
        
        # Train the model
        self.model.fit(normalized_data)
        self.is_trained = True
        
    def predict(self, data: np.ndarray) -> np.ndarray:
        """
        Predict anomalies in new data.
        
        Args:
            data: Array of sensor readings
            
        Returns:
            Array of anomaly predictions (-1 for anomaly, 1 for normal)
        """
        if not self.is_trained:
            raise ValueError("Model must be trained before making predictions")
            
        normalized_data = self.scaler.transform(data)
        predictions = self.model.predict(normalized_data)
        return predictions
    
    def update(self, new_data: np.ndarray, labels: np.ndarray):
        """
        Update the model with new data.
        
        Args:
            new_data: New sensor readings
            labels: True labels (0=normal, 1=anomaly)
        """
        # For online learning, we could retrain with new data
        # In practice, this might involve more sophisticated incremental learning
        pass
