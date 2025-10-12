
"""Logging utilities for the swarm cooling system."""

import logging
import sys
from pathlib import Path
from datetime import datetime


def setup_logger(name: str, log_file: str = None, level=logging.INFO) -> logging.Logger:
    """
    Setup logger with console and file handlers.
    
    Args:
        name: Logger name
        log_file: Path to log file (optional)
        level: Logging level
        
    Returns:
        Configured logger
    """
    logger = logging.getLogger(name)
    logger.setLevel(level)
    
    # Remove existing handlers
    logger.handlers = []
    
    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(level)
    console_format = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    console_handler.setFormatter(console_format)
    logger.addHandler(console_handler)
    
    # File handler (if specified)
    if log_file:
        log_path = Path(log_file)
        log_path.parent.mkdir(parents=True, exist_ok=True)
        
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(level)
        file_format = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        file_handler.setFormatter(file_format)
        logger.addHandler(file_handler)
    
    return logger


import logging
import json
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, Optional

class SystemLogger:
    """
    Comprehensive logging system for the cooling simulation.
    Handles both file and console logging with structured output.
    """
    
    def __init__(self, log_dir: str = 'logs', log_level: str = 'INFO'):
        """
        Initialize the logger.
        
        Args:
            log_dir: Directory to store log files
            log_level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        """
        self.log_dir = Path(log_dir)
        self.log_dir.mkdir(exist_ok=True)
        
        # Create timestamp for this session
        self.session_id = datetime.now().strftime('%Y%m%d_%H%M%S')
        
        # Setup main logger
        self.logger = logging.getLogger('SwarmCoolingSystem')
        self.logger.setLevel(getattr(logging, log_level.upper()))
        
        # Clear existing handlers
        self.logger.handlers.clear()
        
        # Console handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        console_formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt='%H:%M:%S'
        )
        console_handler.setFormatter(console_formatter)
        self.logger.addHandler(console_handler)
        
        # File handler
        log_file = self.log_dir / f'simulation_{self.session_id}.log'
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(logging.DEBUG)
        file_formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        file_handler.setFormatter(file_formatter)
        self.logger.addHandler(file_handler)
        
        # JSON log for structured data
        self.json_log_file = self.log_dir / f'metrics_{self.session_id}.jsonl'
        
        self.logger.info(f"Logger initialized. Session ID: {self.session_id}")
        self.logger.info(f"Log directory: {self.log_dir.absolute()}")
    
    def log_system_start(self, config: Dict):
        """Log system initialization."""
        self.logger.info("=" * 80)
        self.logger.info("SELF-HEALING SWARM AI COOLING SYSTEM - STARTING")
        self.logger.info("=" * 80)
        self.logger.info(f"Configuration: {json.dumps(config, indent=2)}")
    
    def log_agent_creation(self, agent_id: int, neighbors: list):
        """Log agent creation."""
        self.logger.debug(f"Agent {agent_id} created with neighbors: {neighbors}")
    
    def log_fault_injection(self, agent_id: int, timestep: int, fault_type: str):
        """Log fault injection event."""
        self.logger.warning(f"💥 FAULT INJECTED - Agent {agent_id} at timestep {timestep} - Type: {fault_type}")
        self._log_json({
            'event': 'fault_injection',
            'timestep': timestep,
            'agent_id': agent_id,
            'fault_type': fault_type,
            'timestamp': datetime.now().isoformat()
        })
    
    def log_fault_detection(self, agent_id: int, timestep: int, anomaly_score: float):
        """Log fault detection."""
        self.logger.warning(f"🔍 FAULT DETECTED - Agent {agent_id} at timestep {timestep} - Score: {anomaly_score:.3f}")
        self._log_json({
            'event': 'fault_detection',
            'timestep': timestep,
            'agent_id': agent_id,
            'anomaly_score': anomaly_score,
            'timestamp': datetime.now().isoformat()
        })
    
    def log_healing_attempt(self, agent_id: int, timestep: int, success: bool):
        """Log self-healing attempt."""
        status = "SUCCESS ✅" if success else "FAILED ❌"
        self.logger.info(f"🔧 HEALING ATTEMPT - Agent {agent_id} at timestep {timestep} - {status}")
        self._log_json({
            'event': 'healing_attempt',
            'timestep': timestep,
            'agent_id': agent_id,
            'success': success,
            'timestamp': datetime.now().isoformat()
        })
    
    def log_load_redistribution(self, from_agent: int, to_agents: list, timestep: int):
        """Log load redistribution."""
        self.logger.info(f"🔄 LOAD REDISTRIBUTION - From Agent {from_agent} to Agents {to_agents} at timestep {timestep}")
        self._log_json({
            'event': 'load_redistribution',
            'timestep': timestep,
            'from_agent': from_agent,
            'to_agents': to_agents,
            'timestamp': datetime.now().isoformat()
        })
    
    def log_metrics(self, timestep: int, metrics: Dict[str, Any]):
        """Log system metrics."""
        self.logger.debug(f"Timestep {timestep} - Metrics: {metrics}")
        
        # Log to JSON file
        self._log_json({
            'event': 'metrics',
            'timestep': timestep,
            'metrics': metrics,
            'timestamp': datetime.now().isoformat()
        })
    
    def log_agent_state(self, timestep: int, agent_states: list):
        """Log all agent states."""
        self._log_json({
            'event': 'agent_states',
            'timestep': timestep,
            'states': agent_states,
            'timestamp': datetime.now().isoformat()
        })
    
    def log_control_action(self, agent_id: int, timestep: int, action: float, 
                          temperature: float, target: float):
        """Log control action."""
        self.logger.debug(
            f"Agent {agent_id} - Control: {action:.3f}, Temp: {temperature:.2f}°C, Target: {target:.2f}°C"
        )
    
    def log_coordination(self, timestep: int, coordination_signals: list):
        """Log swarm coordination signals."""
        self._log_json({
            'event': 'coordination',
            'timestep': timestep,
            'signals': coordination_signals,
            'timestamp': datetime.now().isoformat()
        })
    
    def log_error(self, error_msg: str, exception: Optional[Exception] = None):
        """Log error."""
        self.logger.error(f"❌ ERROR: {error_msg}")
        if exception:
            self.logger.exception(exception)
    
    def log_warning(self, warning_msg: str):
        """Log warning."""
        self.logger.warning(f"⚠️ WARNING: {warning_msg}")
    
    def log_info(self, info_msg: str):
        """Log info."""
        self.logger.info(info_msg)
    
    def log_system_summary(self, summary: Dict):
        """Log system summary."""
        self.logger.info("=" * 80)
        self.logger.info("SYSTEM SUMMARY")
        self.logger.info("=" * 80)
        for key, value in summary.items():
            self.logger.info(f"{key}: {value}")
        self.logger.info("=" * 80)
    
    def log_simulation_end(self, total_timesteps: int, duration: float):
        """Log simulation end."""
        self.logger.info("=" * 80)
        self.logger.info("SIMULATION COMPLETED")
        self.logger.info(f"Total timesteps: {total_timesteps}")
        self.logger.info(f"Duration: {duration:.2f} seconds")
        self.logger.info("=" * 80)
    
    def _log_json(self, data: Dict):
        """Write structured data to JSON log file."""
        try:
            with open(self.json_log_file, 'a') as f:
                f.write(json.dumps(data) + '\n')
        except Exception as e:
            self.logger.error(f"Failed to write JSON log: {e}")
    
    def get_log_files(self) -> Dict[str, Path]:
        """Get paths to all log files."""
        return {
            'text_log': self.log_dir / f'simulation_{self.session_id}.log',
            'json_log': self.json_log_file
        }
    
    def close(self):
        """Close all handlers."""
        for handler in self.logger.handlers:
            handler.close()
        self.logger.info("Logger closed")
