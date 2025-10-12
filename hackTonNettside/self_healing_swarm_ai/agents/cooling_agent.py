
import numpy as np
from typing import Dict, Optional, List
from datetime import datetime

class CoolingAgent:
    """
    AI-powered cooling agent with self-healing capabilities.
    Each agent can sense, detect faults, control, and cooperate.
    """
    
    def __init__(self, agent_id: int, config: Dict, anomaly_detector, adaptive_controller):
        self.agent_id = agent_id
        self.config = config
        self.anomaly_detector = anomaly_detector
        self.adaptive_controller = adaptive_controller
        
        # Agent state
        self.temperature = np.random.uniform(23, 27)
        self.fan_speed = np.random.uniform(0.3, 0.7)
        self.power_consumption = np.random.uniform(100, 200)
        self.humidity = np.random.uniform(45, 55)
        self.load = 0.5
        
        # Status
        self.is_faulty = False
        self.is_active = True
        self.fault_history: List[Dict] = []
        self.last_updated = datetime.now()
        
        # Communication
        self.neighbors: List[int] = []
        self.coordination_signal: Optional[Dict] = None
        
        # Performance tracking
        self.control_history = []
        self.temperature_history = []
        
        # Anomaly detection
        self.anomaly_detected = False
        self.anomaly_score = 0.0
    
    def sense(self) -> Dict[str, float]:
        """
        Collect sensor readings from the environment.
        
        Returns:
            Dict of sensor readings
        """
        sensor_data = {
            'agent_id': self.agent_id,
            'temperature': self.temperature,
            'fan_speed': self.fan_speed,
            'power': self.power_consumption,
            'humidity': self.humidity,
            'load': self.load,
            'timestamp': datetime.now().timestamp()
        }
        
        # Add noise to simulate real sensors
        if not self.is_faulty:
            sensor_data['temperature'] += np.random.normal(0, 0.1)
            sensor_data['humidity'] += np.random.normal(0, 0.5)
        
        return sensor_data
    
    def detect_fault(self, sensor_data: Dict) -> bool:
        """
        Use anomaly detector to identify faults.
        
        Args:
            sensor_data: Current sensor readings
            
        Returns:
            True if fault detected
        """
        # Prepare data for anomaly detector
        features = np.array([[
            sensor_data['temperature'],
            sensor_data['humidity'],
            sensor_data['power'],
            sensor_data['fan_speed']
        ]])
        
        try:
            prediction = self.anomaly_detector.predict(features)
            is_anomaly = prediction[0] == -1  # Isolation Forest returns -1 for anomalies
            
            if is_anomaly:
                self.report_fault('anomaly_detected', severity=0.7)
                self.is_faulty = True
            
            return is_anomaly
        except Exception as e:
            print(f"Agent {self.agent_id}: Fault detection error - {e}")
            return False
    
    def control(self, target_temp: float, coordination_signal: Optional[Dict] = None) -> float:
        """
        Compute control action using adaptive controller.
        
        Args:
            target_temp: Target temperature
            coordination_signal: Signal from swarm coordinator
            
        Returns:
            New fan speed
        """
        current_state = {
            'temperature': self.temperature,
            'fan_speed': self.fan_speed,
            'ambient_temp': self.config['system']['ambient_temp']
        }
        
        # Get base control action
        new_fan_speed = self.adaptive_controller.predict(current_state, target_temp)
        
        # Apply coordination signal if available
        if coordination_signal:
            cooperation_signal = coordination_signal.get('cooperation_signal', 0.0)
            new_fan_speed += cooperation_signal
            new_fan_speed = np.clip(new_fan_speed, 0.0, 1.0)
        
        # If faulty, reduce effectiveness
        if self.is_faulty:
            new_fan_speed *= 0.3  # Degraded performance
        
        self.fan_speed = new_fan_speed
        self.control_history.append(new_fan_speed)
        
        return new_fan_speed
    
    def cooperate(self, neighbor_states: List[Dict]) -> Dict:
        """
        Share information and coordinate with neighbors.
        
        Args:
            neighbor_states: States of neighboring agents
            
        Returns:
            Message to broadcast to neighbors
        """
        message = {
            'agent_id': self.agent_id,
            'temperature': self.temperature,
            'fan_speed': self.fan_speed,
            'is_faulty': self.is_faulty,
            'load': self.load,
            'needs_help': self.is_faulty or (self.temperature > self.config['system']['target_temp'] + 3)
        }
        
        # If faulty, request load redistribution
        if self.is_faulty and neighbor_states:
            healthy_neighbors = [n for n in neighbor_states if not n.get('is_faulty', False)]
            if healthy_neighbors:
                message['load_transfer'] = self.load / len(healthy_neighbors)
        
        return message
    
    def update_state(self, dt: float = 1.0):
        """
        Update agent's physical state based on current control actions.
        
        Args:
            dt: Time step duration
        """
        target_temp = self.config['system']['target_temp']
        ambient_temp = self.config['system']['ambient_temp']
        
        # Thermal dynamics
        cooling_effect = self.fan_speed * (self.temperature - target_temp) * 0.3
        ambient_effect = 0.1 * (ambient_temp - self.temperature)
        load_effect = self.load * 0.2
        
        # Temperature update
        temp_change = -cooling_effect + ambient_effect + load_effect
        
        if self.is_faulty:
            temp_change += 0.3  # Fault causes temperature rise
        
        self.temperature += temp_change * dt
        self.temperature_history.append(self.temperature)
        
        # Power consumption
        self.power_consumption = 100 + self.fan_speed * 400 + self.load * 200
        
        # Update timestamp
        self.last_updated = datetime.now()
    
    def report_fault(self, fault_type: str, severity: float):
        """
        Log fault detection event.
        
        Args:
            fault_type: Type of fault detected
            severity: Fault severity (0-1)
        """
        fault_record = {
            'agent_id': self.agent_id,
            'fault_type': fault_type,
            'severity': severity,
            'temperature': self.temperature,
            'fan_speed': self.fan_speed,
            'timestamp': datetime.now().isoformat()
        }
        self.fault_history.append(fault_record)
        print(f"⚠️ Agent {self.agent_id}: Fault detected - {fault_type} (severity: {severity:.2f})")
    
    def heal_self(self) -> bool:
        """
        Attempt self-healing by resetting to safe state.
        
        Returns:
            True if healing successful
        """
        if not self.is_faulty:
            return True
        
        print(f"🔧 Agent {self.agent_id}: Attempting self-healing...")
        
        # Reset to safe operating state
        self.fan_speed = 0.8  # High cooling
        self.load = 0.3  # Reduce load
        
        # Check if temperature stabilizes
        if len(self.temperature_history) > 5:
            recent_temps = self.temperature_history[-5:]
            if max(recent_temps) - min(recent_temps) < 1.0:
                self.is_faulty = False
                print(f"✅ Agent {self.agent_id}: Self-healing successful")
                return True
        
        return False
    
    def get_state_dict(self) -> Dict:
        """Get complete agent state as dictionary."""
        return {
            'agent_id': self.agent_id,
            'temperature': self.temperature,
            'fan_speed': self.fan_speed,
            'power': self.power_consumption,
            'humidity': self.humidity,
            'load': self.load,
            'is_faulty': self.is_faulty,
            'is_active': self.is_active,
            'num_faults': len(self.fault_history)
        }
    
    def inject_fault(self, fault_type: str = 'sensor_failure'):
        """
        Manually inject a fault into this agent for testing.
        
        Args:
            fault_type: Type of fault to inject
        """
        self.is_faulty = True
        self.report_fault(fault_type, severity=0.9)
        
        # Simulate different fault types
        if fault_type == 'sensor_failure':
            self.temperature += np.random.uniform(2, 5)
        elif fault_type == 'actuator_failure':
            self.fan_speed *= 0.3
        elif fault_type == 'communication_failure':
            self.is_active = False
        
        print(f"💥 Agent {self.agent_id}: Fault injected - {fault_type}")
    
    def reset(self):
        """Reset agent to initial state."""
        self.temperature = np.random.uniform(23, 27)
        self.fan_speed = np.random.uniform(0.3, 0.7)
        self.power_consumption = np.random.uniform(100, 200)
        self.humidity = np.random.uniform(45, 55)
        self.load = 0.5
        self.is_faulty = False
        self.is_active = True
        self.fault_history.clear()
        self.control_history.clear()
        self.temperature_history.clear()
        self.anomaly_detected = False
        self.anomaly_score = 0.0
    
    def get_state(self) -> Dict:
        """Get current agent state (alias for get_state_dict)."""
        return self.get_state_dict()
    
    def detect_anomaly(self, anomaly_detector, step: int = 0) -> bool:
        """
        Check if agent is experiencing anomalous behavior.
        
        Args:
            anomaly_detector: Trained anomaly detection model
            step: Current simulation step (for warm-up period)
            
        Returns:
            True if anomaly detected, False otherwise
        """
        # Skip anomaly detection during warm-up period (first 10 steps)
        if step < 10:
            return False
        
        # Get current state
        state = np.array([[
            self.temperature,
            self.humidity,
            self.power_consumption,
            self.fan_speed
        ]])
        
        # Check for anomaly
        is_anomaly = anomaly_detector.predict(state)
        anomaly_scores = anomaly_detector.get_anomaly_scores(state)
        
        # Update anomaly detection
        if is_anomaly:
            self.anomaly_detected = True
            self.anomaly_score = anomaly_scores[0]
            return True
        
        self.anomaly_detected = False
        self.anomaly_score = 0.0
        return False
    
    def inject_fault(self, fault_type: str = 'sensor_failure'):
        """
        Manually inject a fault into this agent for testing.
        
        Args:
            fault_type: Type of fault to inject
        """
        self.is_faulty = True
        self.report_fault(fault_type, severity=0.9)
        
        # Simulate different fault types
        if fault_type == 'sensor_failure':
            self.temperature += np.random.uniform(2, 5)
        elif fault_type == 'actuator_failure':
            self.fan_speed *= 0.3
        elif fault_type == 'communication_failure':
            self.is_active = False
        
        print(f"💥 Agent {self.agent_id}: Fault injected - {fault_type}")
    
    def reset(self):
        """Reset agent to initial state."""
        self.temperature = np.random.uniform(23, 27)
        self.fan_speed = np.random.uniform(0.3, 0.7)
        self.power_consumption = np.random.uniform(100, 200)
        self.humidity = np.random.uniform(45, 55)
        self.load = 0.5
        self.is_faulty = False
        self.is_active = True
        self.fault_history.clear()
        self.control_history.clear()
        self.temperature_history.clear()
    
    def get_state(self) -> Dict:
        """Get current agent state (alias for get_state_dict)."""
        return self.get_state_dict()
    
    def detect_anomaly(self, anomaly_detector, step: int = 0) -> bool:
        """
        Check if agent is experiencing anomalous behavior.
        
        Args:
            anomaly_detector: Trained anomaly detection model
            step: Current simulation step (for warm-up period)
            
        Returns:
            True if anomaly detected, False otherwise
        """
        # Skip anomaly detection during warm-up period (first 10 steps)
        if step < 10:
            return False
        
        # Get current state
        state = np.array([[
            self.temperature,
            self.humidity,
            self.power_consumption,
            self.fan_speed
        ]])
        
        # Check for anomaly
        is_anomaly = anomaly_detector.predict(state)
        anomaly_scores = anomaly_detector.get_anomaly_scores(state)
        
        # Update anomaly detection
        if is_anomaly:
            self.anomaly_detected = True
            self.anomaly_score = anomaly_scores[0]
            return True
        
        self.anomaly_detected = False
        self.anomaly_score = 0.0
        return False
