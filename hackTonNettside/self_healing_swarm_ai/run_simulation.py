
"""
Main simulation runner for the Self-Healing Swarm AI Cooling System.
"""

import numpy as np
import yaml
from pathlib import Path
from datetime import datetime
from typing import Tuple

# Import core components
from agents.swarm_coordinator import SwarmCoordinator
from models.anomaly_detector import AnomalyDetector
from models.adaptive_controller import AdaptiveController

# Import visualization utilities
from utils import (
    plot_temperature_evolution,
    plot_energy_consumption,
    plot_fault_recovery
)


def load_config(config_path: str = "config/config.yaml") -> dict:
    """
    Load configuration from YAML file.
    
    Args:
        config_path: Path to configuration file
        
    Returns:
        Configuration dictionary
    """
    config_file = Path(config_path)
    
    if not config_file.exists():
        print(f"⚠️  Config file not found: {config_path}")
        print("Creating default configuration...")
        
        # Create default config
        default_config = {
            'system': {
                'num_agents': 6,
                'target_temp': 25.0,
                'ambient_temp': 30.0,
                'initial_temp_range': [23.0, 27.0],
                'initial_fan_range': [0.3, 0.7]
            },
            'simulation': {
                'total_steps': 200,
                'dt': 1.0,
                'fault_injection_step': 50,
                'random_seed': 42
            },
            'anomaly_detection': {
                'contamination': 0.1,
                'n_estimators': 100,
                'max_samples': 256,
                'fault_threshold': 0.7
            },
            'control': {
                'kp': 0.3,
                'ki': 0.05,
                'kd': 0.1,
                'learning_rate': 0.1,
                'max_fan_speed': 1.0,
                'min_fan_speed': 0.0
            },
            'swarm': {
                'communication_weight': 0.3,
                'cooperation_strength': 0.15,
                'topology': 'ring'
            },
            'agent': {
                'temp_sensor_noise': 0.1,
                'humidity_sensor_noise': 0.5,
                'power_base': 100,
                'power_per_fan': 400,
                'power_per_load': 200
            },
            'healing': {
                'self_heal_attempts': 3,
                'heal_threshold': 1.0,
                'recovery_time': 10
            }
        }
        
        # Create config directory if it doesn't exist
        config_file.parent.mkdir(parents=True, exist_ok=True)
        
        # Save default config
        with open(config_file, 'w') as f:
            yaml.dump(default_config, f, default_flow_style=False)
        
        return default_config
    
    # Load existing config
    with open(config_file, 'r') as f:
        config = yaml.safe_load(f)
    
    print(f"✅ Configuration loaded from {config_path}")
    return config


def train_models(config: dict) -> Tuple[AnomalyDetector, AdaptiveController]:
    """
    Train anomaly detector and controller on baseline data.
    
    Args:
        config: System configuration
        
    Returns:
        Trained anomaly detector and controller
    """
    print("\n" + "="*60)
    print("TRAINING MODELS")
    print("="*60)
    
    # Generate training data (normal operating conditions)
    num_samples = 1000
    training_data = []
    
    for _ in range(num_samples):
        temp = np.random.normal(config['system']['target_temp'], 1.0)
        humidity = np.random.normal(50, 5)
        power = np.random.normal(200, 30)
        fan_speed = np.random.uniform(0.3, 0.7)
        
        training_data.append([temp, humidity, power, fan_speed])
    
    training_data = np.array(training_data)
    
    # Train anomaly detector
    anomaly_detector = AnomalyDetector(
        contamination=config['anomaly_detection']['contamination']
    )
    anomaly_detector.train(training_data)
    
    # Initialize controller
    adaptive_controller = AdaptiveController(config)
    
    print("✅ Models trained successfully\n")
    
    return anomaly_detector, adaptive_controller


def run_simulation(config: dict, anomaly_detector: AnomalyDetector, 
                   adaptive_controller: AdaptiveController):
    """
    Run the main swarm cooling simulation.
    
    Args:
        config: System configuration
        anomaly_detector: Trained anomaly detection model
        adaptive_controller: Adaptive controller
    """
    print("\n" + "="*60)
    print("RUNNING SIMULATION")
    print("="*60)
    
    # Set random seed for reproducibility
    if 'random_seed' in config['simulation']:
        np.random.seed(config['simulation']['random_seed'])
    
    # Initialize swarm
    swarm = SwarmCoordinator(
        num_agents=config['system']['num_agents'],
        config=config,
        anomaly_detector=anomaly_detector,
        adaptive_controller=adaptive_controller
    )
    
    # Simulation parameters
    total_steps = config['simulation']['total_steps']
    fault_step = config['simulation']['fault_injection_step']
    
    print(f"\n📊 Simulation Parameters:")
    print(f"   - Number of agents: {config['system']['num_agents']}")
    print(f"   - Target temperature: {config['system']['target_temp']}°C")
    print(f"   - Total steps: {total_steps}")
    print(f"   - Fault injection at step: {fault_step}")
    print()
    
    # Run simulation
    faulty_agent = None
    for step in range(total_steps):
        # Inject fault at specified step
        if step == fault_step:
            faulty_agent = swarm.inject_fault()
        
        # Execute swarm behavior
        swarm.step()
        
        # Log step information
        if step % 50 == 0:
            avg_temp = np.mean(swarm.temps)
            print(f"   Step {step:3d}: Avg Temp = {avg_temp:.2f}°C")
    
    print("\n✅ Simulation complete!")
    
    # Generate visualizations
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_dir = Path("results") / timestamp
    output_dir.mkdir(parents=True, exist_ok=True)
    
    print(f"\n📊 Generating visualizations...")
    print(f"📁 Output directory: {output_dir.absolute()}")
    
    # Plot temperature evolution
    try:
        print("   Creating temperature evolution plot...")
        plot_temperature_evolution(
            swarm.temp_history,
            config['system']['target_temp'],
            fault_step,
            output_dir / "temperature_evolution.png",
            faulty_agent=faulty_agent
        )
        print("   ✅ Temperature evolution plot created")
    except Exception as e:
        print(f"   ⚠️  Error creating temperature plot: {e}")
    
    # Plot energy consumption
    try:
        print("   Creating energy consumption plot...")
        plot_energy_consumption(
            swarm.energy_history,
            fault_step,
            output_dir / "energy_consumption.png"
        )
        print("   ✅ Energy consumption plot created")
    except Exception as e:
        print(f"   ⚠️  Error creating energy plot: {e}")
    
    # Plot fault recovery
    try:
        print("   Creating fault recovery plot...")
        plot_fault_recovery(
            swarm.temp_history,
            swarm.energy_history,
            fault_step,
            output_dir / "fault_recovery.png"
        )
        print("   ✅ Fault recovery plot created")
    except Exception as e:
        print(f"   ⚠️  Error creating fault recovery plot: {e}")
    
    # Calculate temperature statistics
    # Flatten temp_history which is a list of arrays
    all_temps = []
    for temp_array in swarm.temp_history:
        if isinstance(temp_array, np.ndarray):
            all_temps.extend(temp_array.tolist())
        else:
            all_temps.append(temp_array)
    
    max_temp = max(all_temps)
    min_temp = min(all_temps)
    
    # Calculate average temperatures over time
    avg_temps_over_time = [np.mean(temps) if isinstance(temps, np.ndarray) else temps 
                           for temps in swarm.temp_history]
    
    # Save system metrics
    print("   Creating metrics file...")
    final_state = swarm.get_system_state()
    metrics_file = output_dir / "metrics.txt"
    
    try:
        with open(metrics_file, 'w') as f:
            f.write("="*60 + "\n")
            f.write("SIMULATION METRICS\n")
            f.write("="*60 + "\n\n")
            f.write(f"Configuration:\n")
            f.write(f"  - Number of agents: {config['system']['num_agents']}\n")
            f.write(f"  - Target temperature: {config['system']['target_temp']}°C\n")
            f.write(f"  - Simulation steps: {total_steps}\n")
            f.write(f"  - Fault injection step: {fault_step}\n")
            f.write(f"  - Faulty agent: {faulty_agent if faulty_agent is not None else 'None'}\n\n")
            
            f.write(f"Final State:\n")
            f.write(f"  - Average temperature: {final_state['avg_temperature']:.2f}°C\n")
            f.write(f"  - Temperature variance: {final_state['temp_variance']:.4f}\n")
            f.write(f"  - Average fan speed: {final_state['avg_fan_speed']:.2f}\n")
            f.write(f"  - Total power consumption: {final_state['total_power']:.2f} W\n\n")
            
            f.write(f"Temperature Statistics:\n")
            f.write(f"  - Maximum temperature: {max_temp:.2f}°C\n")
            f.write(f"  - Minimum temperature: {min_temp:.2f}°C\n")
            f.write(f"  - Temperature range: {max_temp - min_temp:.2f}°C\n")
            f.write(f"  - Final average: {avg_temps_over_time[-1]:.2f}°C\n\n")
            
            f.write(f"Energy Consumption:\n")
            f.write(f"  - Total energy: {sum(swarm.energy_history):.2f} J\n")
            f.write(f"  - Average power: {np.mean(swarm.energy_history):.2f} W\n")
            f.write(f"  - Peak power: {max(swarm.energy_history):.2f} W\n\n")
            
            # Fault recovery metrics
            if faulty_agent is not None:
                temps_before_fault = avg_temps_over_time[:fault_step]
                temps_after_fault = avg_temps_over_time[fault_step:]
                
                # Find recovery time (when temp returns to within 1°C of target)
                recovery_step = None
                target = config['system']['target_temp']
                for i, temp in enumerate(temps_after_fault):
                    if abs(temp - target) < 1.0:
                        recovery_step = i
                        break
                
                f.write(f"Fault Recovery:\n")
                f.write(f"  - Avg temp before fault: {np.mean(temps_before_fault):.2f}°C\n")
                f.write(f"  - Max temp during fault: {max(temps_after_fault[:20]):.2f}°C\n")
                if recovery_step is not None:
                    f.write(f"  - Recovery time: {recovery_step} steps\n")
                else:
                    f.write(f"  - Recovery time: Not recovered within simulation\n")
        
        print(f"   ✅ Metrics file created")
    except Exception as e:
        print(f"   ⚠️  Error creating metrics file: {e}")
    
    print(f"\n📊 Results saved to: {output_dir.absolute()}")
    print(f"📄 Metrics saved to: {metrics_file.absolute()}")
    
    # List all files created
    print(f"\n📋 Files created:")
    for file in output_dir.iterdir():
        print(f"   - {file.name}")


def main():
    """
    Main entry point for the simulation.
    """
    print("\n" + "="*60)
    print("SELF-HEALING SWARM AI COOLING SYSTEM")
    print("="*60)
    
    # Load configuration
    config = load_config()
    
    # Train models
    anomaly_detector, adaptive_controller = train_models(config)
    
    # Run simulation
    run_simulation(config, anomaly_detector, adaptive_controller)
    
    print("\n" + "="*60)
    print("SIMULATION COMPLETE")
    print("="*60)


if __name__ == "__main__":
    main()
