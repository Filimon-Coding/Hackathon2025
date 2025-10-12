
"""
Main entry point for the Self-Healing Swarm AI Cooling System.
Provides CLI interface and simulation runner.
"""

import argparse
import json
import numpy as np
from pathlib import Path
from typing import Dict, Optional
import matplotlib.pyplot as plt
from datetime import datetime

from agents.swarm_controller import SwarmController
from utils.visualization import SwarmVisualizer
from utils.metrics import MetricsCollector
from utils.logger import setup_logger

logger = setup_logger(__name__)


class SimulationRunner:
    """Main simulation runner for the swarm cooling system."""
    
    def __init__(self, config: Dict):
        """
        Initialize simulation runner.
        
        Args:
            config: Configuration dictionary
        """
        self.config = config
        self.controller = SwarmController(
            num_agents=config['num_agents'],
            target_temp=config['target_temp'],
            communication_weight=config['communication_weight'],
            topology=config.get('topology', 'ring')
        )
        self.visualizer = SwarmVisualizer()
        self.metrics_collector = MetricsCollector()
        
    def run(self, steps: int, ambient_temp: float = 30.0, 
            inject_fault: Optional[Dict] = None):
        """
        Run the simulation.
        
        Args:
            steps: Number of simulation steps
            ambient_temp: Ambient temperature
            inject_fault: Fault injection config (agent_id, step, type)
        """
        logger.info(f"Starting simulation with {self.config['num_agents']} agents")
        logger.info(f"Target temperature: {self.config['target_temp']}°C")
        logger.info(f"Ambient temperature: {ambient_temp}°C")
        
        for step in range(steps):
            # Inject fault if configured
            if inject_fault and step == inject_fault.get('step', -1):
                agent_id = inject_fault['agent_id']
                fault_type = inject_fault.get('type', 'temperature_spike')
                self.controller.inject_fault(agent_id, fault_type)
                logger.warning(f"Fault injected at agent {agent_id}: {fault_type}")
            
            # Step simulation
            self.controller.step(ambient_temp)
            
            # Collect metrics
            metrics = self.controller.get_system_metrics()
            self.metrics_collector.record(step, metrics)
            
            # Log progress
            if step % 20 == 0:
                logger.info(f"Step {step}: Avg Temp={metrics['avg_temperature']:.2f}°C, "
                          f"Power={metrics['total_power']:.2f}W, "
                          f"Faults={metrics['num_faulty_agents']}")
        
        logger.info("Simulation completed")
        return self.controller.get_history()
    
    def visualize_results(self, save_path: Optional[str] = None):
        """
        Visualize simulation results.
        
        Args:
            save_path: Path to save visualization
        """
        history = self.controller.get_history()
        
        # Create visualization
        fig = self.visualizer.plot_comprehensive_results(
            history,
            self.config['target_temp'],
            self.metrics_collector.get_summary()
        )
        
        if save_path:
            fig.savefig(save_path, dpi=300, bbox_inches='tight')
            logger.info(f"Visualization saved to {save_path}")
        else:
            plt.show()
    
    def export_results(self, output_path: str):
        """
        Export simulation results to JSON.
        
        Args:
            output_path: Path to save results
        """
        results = {
            'config': self.config,
            'metrics': self.metrics_collector.get_summary(),
            'final_state': self.controller.export_state(),
            'timestamp': datetime.now().isoformat()
        }
        
        with open(output_path, 'w') as f:
            json.dump(results, f, indent=2)
        
        logger.info(f"Results exported to {output_path}")


def load_config(config_path: Optional[str] = None) -> Dict:
    """
    Load configuration from file or use defaults.
    
    Args:
        config_path: Path to config file
        
    Returns:
        Configuration dictionary
    """
    default_config = {
        'num_agents': 6,
        'target_temp': 25.0,
        'communication_weight': 0.3,
        'topology': 'ring',
        'learning_rate': 0.1
    }
    
    if config_path and Path(config_path).exists():
        with open(config_path, 'r') as f:
            user_config = json.load(f)
        default_config.update(user_config)
        logger.info(f"Loaded configuration from {config_path}")
    
    return default_config


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description='Self-Healing Swarm AI Cooling System Simulation'
    )
    
    parser.add_argument(
        '--config',
        type=str,
        help='Path to configuration file'
    )
    
    parser.add_argument(
        '--steps',
        type=int,
        default=200,
        help='Number of simulation steps (default: 200)'
    )
    
    parser.add_argument(
        '--agents',
        type=int,
        help='Number of cooling agents'
    )
    
    parser.add_argument(
        '--target-temp',
        type=float,
        help='Target temperature in Celsius'
    )
    
    parser.add_argument(
        '--ambient-temp',
        type=float,
        default=30.0,
        help='Ambient temperature in Celsius (default: 30.0)'
    )
    
    parser.add_argument(
        '--topology',
        type=str,
        choices=['ring', 'mesh', 'star'],
        help='Network topology'
    )
    
    parser.add_argument(
        '--inject-fault',
        type=int,
        help='Agent ID to inject fault into'
    )
    
    parser.add_argument(
        '--fault-step',
        type=int,
        default=50,
        help='Step at which to inject fault (default: 50)'
    )
    
    parser.add_argument(
        '--fault-type',
        type=str,
        default='temperature_spike',
        choices=['temperature_spike', 'sensor_failure', 'cooling_failure'],
        help='Type of fault to inject'
    )
    
    parser.add_argument(
        '--visualize',
        action='store_true',
        help='Show visualization after simulation'
    )
    
    parser.add_argument(
        '--save-plot',
        type=str,
        help='Path to save visualization plot'
    )
    
    parser.add_argument(
        '--export',
        type=str,
        help='Path to export results JSON'
    )
    
    parser.add_argument(
        '--verbose',
        action='store_true',
        help='Enable verbose logging'
    )
    
    args = parser.parse_args()
    
    # Load configuration
    config = load_config(args.config)
    
    # Override with command line arguments
    if args.agents:
        config['num_agents'] = args.agents
    if args.target_temp:
        config['target_temp'] = args.target_temp
    if args.topology:
        config['topology'] = args.topology
    
    # Setup fault injection
    fault_config = None
    if args.inject_fault is not None:
        fault_config = {
            'agent_id': args.inject_fault,
            'step': args.fault_step,
            'type': args.fault_type
        }
    
    # Run simulation
    runner = SimulationRunner(config)
    runner.run(
        steps=args.steps,
        ambient_temp=args.ambient_temp,
        inject_fault=fault_config
    )
    
    # Visualize results
    if args.visualize or args.save_plot:
        runner.visualize_results(save_path=args.save_plot)
    
    # Export results
    if args.export:
        runner.export_results(args.export)
    
    # Print summary
    metrics = runner.metrics_collector.get_summary()
    print("\n" + "="*60)
    print("SIMULATION SUMMARY")
    print("="*60)
    print(f"Total Steps: {args.steps}")
    print(f"Number of Agents: {config['num_agents']}")
    print(f"Target Temperature: {config['target_temp']}°C")
    print(f"Final Avg Temperature: {metrics['final_avg_temp']:.2f}°C")
    print(f"Total Energy Consumed: {metrics['total_energy']:.2f}W·s")
    print(f"Peak Temperature: {metrics['peak_temp']:.2f}°C")
    print(f"Temperature Stability: {metrics['stability_score']:.2%}")
    print(f"Faults Detected: {metrics['total_faults']}")
    print("="*60 + "\n")


if __name__ == '__main__':
    main()
