
"""Metrics collection and analysis utilities."""

import numpy as np
from typing import Dict, List
from collections import defaultdict


class MetricsCollector:
    """Collects and analyzes simulation metrics."""
    
    def __init__(self):
        """Initialize metrics collector."""
        self.metrics_history = defaultdict(list)
        self.step_count = 0
    
    def record(self, step: int, **kwargs):
        """Record metrics for a given step."""
        self.step_count = step
        for key, value in kwargs.items():
            self.metrics_history[key].append(value)
    
    def get_metric_history(self, metric_name: str) -> List:
        """Get historical values for a specific metric."""
        return self.metrics_history.get(metric_name, [])
    
    def get_all_metrics(self) -> Dict:
        """Get all recorded metrics."""
        return dict(self.metrics_history)
    
    def clear_history(self):
        """Clear all recorded metrics."""
        self.metrics_history.clear()
        self.step_count = 0

class MetricsCalculator:
    """
    Calculate and track performance metrics for the cooling system.
    """
    
    def __init__(self):
        self.metrics_history = {
            'temperature_rmse': [],
            'temperature_mae': [],
            'power_consumption': [],
            'fault_recovery_time': [],
            'system_stability': [],
            'coordination_efficiency': []
        }
    
    def calculate_temperature_error(self, actual_temps: List[float], target_temp: float) -> Dict[str, float]:
        """
        Calculate temperature tracking errors.
        
        Args:
            actual_temps: List of actual temperatures
            target_temp: Target temperature
            
        Returns:
            Dict with RMSE and MAE
        """
        target_array = np.full(len(actual_temps), target_temp)
        
        rmse = np.sqrt(mean_squared_error(target_array, actual_temps))
        mae = mean_absolute_error(target_array, actual_temps)
        
        self.metrics_history['temperature_rmse'].append(rmse)
        self.metrics_history['temperature_mae'].append(mae)
        
        return {
            'rmse': rmse,
            'mae': mae,
            'max_deviation': max(abs(t - target_temp) for t in actual_temps)
        }
    
    def calculate_power_efficiency(self, power_consumption: List[float], 
                                   temperature_errors: List[float]) -> float:
        """
        Calculate power efficiency metric.
        
        Args:
            power_consumption: List of power consumption values
            temperature_errors: List of temperature errors
            
        Returns:
            Efficiency score (higher is better)
        """
        total_power = sum(power_consumption)
        avg_error = np.mean(temperature_errors)
        
        # Efficiency = 1 / (power * error)
        efficiency = 1.0 / (total_power * (avg_error + 1e-6))
        
        self.metrics_history['power_consumption'].append(total_power)
        
        return efficiency
    
    def calculate_fault_recovery_time(self, fault_injection_step: int, 
                                      recovery_step: int) -> int:
        """
        Calculate time taken to recover from fault.
        
        Args:
            fault_injection_step: Step when fault was injected
            recovery_step: Step when system recovered
            
        Returns:
            Recovery time in steps
        """
        recovery_time = recovery_step - fault_injection_step
        self.metrics_history['fault_recovery_time'].append(recovery_time)
        return recovery_time
    
    def calculate_system_stability(self, temperature_variance: List[float]) -> float:
        """
        Calculate system stability based on temperature variance.
        
        Args:
            temperature_variance: List of temperature variances over time
            
        Returns:
            Stability score (0-1, higher is more stable)
        """
        if not temperature_variance:
            return 0.0
        
        # Stability inversely proportional to variance
        avg_variance = np.mean(temperature_variance)
        stability = 1.0 / (1.0 + avg_variance)
        
        self.metrics_history['system_stability'].append(stability)
        
        return stability
    
    def calculate_coordination_efficiency(self, agent_states: List[Dict]) -> float:
        """
        Calculate how well agents are coordinating.
        
        Args:
            agent_states: List of agent state dictionaries
            
        Returns:
            Coordination efficiency score
        """
        if not agent_states:
            return 0.0
        
        # Calculate temperature uniformity
        temps = [state['temperature'] for state in agent_states]
        temp_std = np.std(temps)
        
        # Calculate load balance
        loads = [state.get('load', 0.5) for state in agent_states]
        load_std = np.std(loads)
        
        # Lower variance = better coordination
        coordination = 1.0 / (1.0 + temp_std + load_std)
        
        self.metrics_history['coordination_efficiency'].append(coordination)
        
        return coordination
    
    def get_summary_statistics(self) -> Dict:
        """
        Get summary statistics of all metrics.
        
        Returns:
            Dict with mean, std, min, max for each metric
        """
        summary = {}
        
        for metric_name, values in self.metrics_history.items():
            if values:
                summary[metric_name] = {
                    'mean': np.mean(values),
                    'std': np.std(values),
                    'min': np.min(values),
                    'max': np.max(values),
                    'latest': values[-1]
                }
        
        return summary
    
    def reset(self):
        """Reset all metrics history."""
        for key in self.metrics_history:
            self.metrics_history[key] = []
