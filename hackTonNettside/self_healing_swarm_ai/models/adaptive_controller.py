
"""
Adaptive Controller using Reinforcement Learning principles.
"""

import numpy as np
from typing import Dict, Tuple
import pickle
from pathlib import Path


class PIDController:
    """
    PID Controller for individual agent temperature control.
    """
    
    def __init__(self, kp: float, ki: float, kd: float):
        self.kp = kp
        self.ki = ki
        self.kd = kd
        self.integral = 0.0
        self.previous_error = 0.0
        
    def compute(self, error: float, dt: float = 1.0) -> float:
        """
        Compute PID control output.
        
        Args:
            error: Current error (target - actual)
            dt: Time step
            
        Returns:
            Control signal
        """
        self.integral += error * dt
        derivative = (error - self.previous_error) / dt
        
        output = self.kp * error + self.ki * self.integral + self.kd * derivative
        self.previous_error = error
        
        return output
    
    def reset(self):
        """Reset controller state."""
        self.integral = 0.0
        self.previous_error = 0.0


class AdaptiveController:
    """
    Adaptive PID-like controller with learning capabilities.
    Adjusts fan speed based on temperature error and learns optimal parameters.
    """
    
    def __init__(self, config: Dict):
        """
        Initialize adaptive controller.
        
        Args:
            config: System configuration dictionary
        """
        self.config = config
        control_config = config['control']
        
        # PID parameters (will be adapted)
        self.kp = control_config['kp']  # Proportional gain
        self.ki = control_config['ki']  # Integral gain
        self.kd = control_config['kd']  # Derivative gain
        
        # Learning parameters
        self.learning_rate = control_config['learning_rate']
        self.adaptation_rate = 0.01
        
        # State tracking
        self.integral_error = 0.0
        self.previous_error = 0.0
        self.control_history = []
        
    def predict(self, current_state: Dict, target_temp: float) -> float:
        """
        Compute control action (fan speed) based on current state.
        
        Args:
            current_state: Dictionary with temperature, fan_speed, ambient_temp
            target_temp: Target temperature to maintain
            
        Returns:
            New fan speed (0-1)
        """
        current_temp = current_state['temperature']
        current_fan = current_state['fan_speed']
        
        # Calculate error
        error = current_temp - target_temp
        
        # PID components
        p_term = self.kp * error
        
        # Integral term (with anti-windup)
        self.integral_error += error
        self.integral_error = np.clip(self.integral_error, -10, 10)
        i_term = self.ki * self.integral_error
        
        # Derivative term
        d_term = self.kd * (error - self.previous_error)
        
        # Compute control signal
        control_signal = p_term + i_term + d_term
        
        # Convert to fan speed (0-1)
        new_fan_speed = current_fan + control_signal * self.learning_rate
        new_fan_speed = np.clip(new_fan_speed, 0.0, 1.0)
        
        # Update state
        self.previous_error = error
        self.control_history.append({
            'error': error,
            'fan_speed': new_fan_speed,
            'p_term': p_term,
            'i_term': i_term,
            'd_term': d_term
        })
        
        return new_fan_speed
    
    def adapt_parameters(self, performance_metric: float):
        """
        Adapt PID parameters based on performance.
        
        Args:
            performance_metric: Performance score (lower is better)
        """
        # Simple gradient-free adaptation
        if performance_metric > 1.0:  # Poor performance
            # Increase proportional gain
            self.kp += self.adaptation_rate
            self.kp = np.clip(self.kp, 0.01, 1.0)
        elif performance_metric < 0.5:  # Good performance
            # Fine-tune by slightly reducing gains
            self.kp *= 0.99
            self.ki *= 0.99
    
    def reset(self):
        """Reset controller state."""
        self.integral_error = 0.0
        self.previous_error = 0.0
        self.control_history = []
    
    def save(self, filepath: Path):
        """Save controller parameters."""
        params = {
            'kp': self.kp,
            'ki': self.ki,
            'kd': self.kd,
            'learning_rate': self.learning_rate
        }
        with open(filepath, 'wb') as f:
            pickle.dump(params, f)
        print(f"✅ Controller saved to {filepath}")
    
    def load(self, filepath: Path):
        """Load controller parameters."""
        with open(filepath, 'rb') as f:
            params = pickle.load(f)
        self.kp = params['kp']
        self.ki = params['ki']
        self.kd = params['kd']
        self.learning_rate = params['learning_rate']
        print(f"✅ Controller loaded from {filepath}")


class ModelPredictiveController:
    """
    Model Predictive Control (MPC) for advanced multi-step optimization.
    """
    
    def __init__(self, config: Dict):
        self.config = config
        self.horizon = config['adaptive_control']['control_horizon']
        self.target_temp = config['system']['target_temp']
        
    def predict_trajectory(self, current_state: Dict, control_sequence: np.ndarray) -> np.ndarray:
        """
        Predict temperature trajectory given a control sequence.
        
        Args:
            current_state: Current system state
            control_sequence: Sequence of fan speeds
            
        Returns:
            Predicted temperature trajectory
        """
        trajectory = [current_state['temperature']]
        temp = current_state['temperature']
        
        for fan_speed in control_sequence:
            # Simple thermal model
            cooling_effect = fan_speed * (temp - self.target_temp) * 0.3
            ambient_effect = 0.1 * (current_state.get('ambient_temp', 30) - temp)
            temp_change = -cooling_effect + ambient_effect
            temp = temp + temp_change
            trajectory.append(temp)
        
        return np.array(trajectory)
    
    def optimize_control(self, current_state: Dict) -> float:
        """
        Optimize control action over prediction horizon.
        
        Args:
            current_state: Current system state
            
        Returns:
            Optimal fan speed for next step
        """
        best_cost = float('inf')
        best_fan_speed = current_state['fan_speed']
        
        # Grid search over possible fan speeds
        for fan_speed in np.linspace(0, 1, 20):
            control_sequence = np.full(self.horizon, fan_speed)
            trajectory = self.predict_trajectory(current_state, control_sequence)
            
            # Cost function: tracking error + energy
            tracking_cost = np.sum((trajectory - self.target_temp) ** 2)
            energy_cost = np.sum(control_sequence ** 2) * 0.1
            total_cost = tracking_cost + energy_cost
            
            if total_cost < best_cost:
                best_cost = total_cost
                best_fan_speed = fan_speed
        
        return best_fan_speed


class QLearningController:
    """
    Q-Learning based controller for more advanced adaptation.
    """
    
    def __init__(self, config: Dict):
        """
        Initialize Q-Learning controller.
        
        Args:
            config: System configuration
        """
        self.config = config
        
        # Discretize state and action spaces
        self.temp_bins = np.linspace(20, 35, 15)
        self.fan_bins = np.linspace(0, 1, 10)
        
        # Q-table: state -> action -> value
        self.q_table = {}
        
        # Learning parameters
        self.alpha = 0.1  # Learning rate
        self.gamma = 0.95  # Discount factor
        self.epsilon = 0.1  # Exploration rate
        
    def _discretize_state(self, temperature: float, fan_speed: float) -> Tuple[int, int]:
        """Convert continuous state to discrete bins."""
        temp_idx = np.digitize(temperature, self.temp_bins)
        fan_idx = np.digitize(fan_speed, self.fan_bins)
        return (temp_idx, fan_idx)
    
    def _get_q_value(self, state: Tuple, action: int) -> float:
        """Get Q-value for state-action pair."""
        if state not in self.q_table:
            self.q_table[state] = np.zeros(len(self.fan_bins))
        return self.q_table[state][action]
    
    def predict(self, current_state: Dict, target_temp: float) -> float:
        """
        Select action using epsilon-greedy policy.
        
        Args:
            current_state: Current system state
            target_temp: Target temperature
            
        Returns:
            New fan speed
        """
        temp = current_state['temperature']
        fan = current_state['fan_speed']
        
        state = self._discretize_state(temp, fan)
        
        # Epsilon-greedy action selection
        if np.random.random() < self.epsilon:
            # Explore: random action
            action_idx = np.random.randint(len(self.fan_bins))
        else:
            # Exploit: best action
            if state not in self.q_table:
                self.q_table[state] = np.zeros(len(self.fan_bins))
            action_idx = np.argmax(self.q_table[state])
        
        # Convert action index to fan speed
        new_fan_speed = self.fan_bins[action_idx]
        
        return new_fan_speed
    
    def update(self, state: Dict, action: float, reward: float, next_state: Dict):
        """
        Update Q-table based on experience.
        
        Args:
            state: Previous state
            action: Action taken
            reward: Reward received
            next_state: Resulting state
        """
        # Discretize states
        s = self._discretize_state(state['temperature'], state['fan_speed'])
        s_next = self._discretize_state(next_state['temperature'], next_state['fan_speed'])
        
        # Find action index
        action_idx = np.argmin(np.abs(self.fan_bins - action))
        
        # Q-learning update
        current_q = self._get_q_value(s, action_idx)
        max_next_q = np.max(self.q_table.get(s_next, np.zeros(len(self.fan_bins))))
        
        new_q = current_q + self.alpha * (reward + self.gamma * max_next_q - current_q)
        
        if s not in self.q_table:
            self.q_table[s] = np.zeros(len(self.fan_bins))
        self.q_table[s][action_idx] = new_q
