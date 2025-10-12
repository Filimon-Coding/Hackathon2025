
"""
Utility functions for the cooling system.
"""

from .visualization import SystemVisualizer

# Create a global visualizer instance
_visualizer = SystemVisualizer()

# Wrapper functions for backward compatibility
def plot_temperature_evolution(temp_history, target_temp, fault_step, output_path, faulty_agent=None):
    """Plot temperature evolution."""
    fig = _visualizer.plot_temperature_evolution(
        temp_history=temp_history,
        target_temp=target_temp,
        faulty_agent_id=faulty_agent,
        fault_step=fault_step
    )
    fig.savefig(output_path, dpi=150, bbox_inches='tight')
    print(f"✅ Temperature plot saved to {output_path}")
    return fig

def plot_energy_consumption(energy_history, fault_step, output_path):
    """Plot energy consumption."""
    fig = _visualizer.plot_power_consumption(power_history=energy_history)
    
    # Add fault line
    import matplotlib.pyplot as plt
    ax = fig.axes[0]
    ax.axvline(x=fault_step, color='red', linestyle=':', linewidth=2, label='Fault Injection')
    ax.legend()
    
    fig.savefig(output_path, dpi=150, bbox_inches='tight')
    print(f"✅ Energy plot saved to {output_path}")
    return fig

def plot_fault_recovery(temp_history, energy_history, fault_step, output_path):
    """Plot fault recovery metrics."""
    import matplotlib.pyplot as plt
    import numpy as np
    
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 8))
    
    temp_array = np.array(temp_history)
    
    # Temperature variance over time
    temp_variance = np.var(temp_array, axis=1)
    ax1.plot(temp_variance, color='purple', linewidth=2)
    ax1.axvline(x=fault_step, color='red', linestyle=':', linewidth=2, label='Fault Injection')
    ax1.set_ylabel('Temperature Variance', fontsize=11)
    ax1.set_title('📊 System Stability Metrics', fontsize=13, fontweight='bold')
    ax1.legend()
    ax1.grid(True, alpha=0.3)
    
    # Energy efficiency
    if len(energy_history) > 0:
        efficiency = 1000 / (np.array(energy_history) + 1)
        ax2.plot(efficiency, color='green', linewidth=2)
        ax2.axvline(x=fault_step, color='red', linestyle=':', linewidth=2, label='Fault Injection')
        ax2.set_xlabel('Time Steps', fontsize=11)
        ax2.set_ylabel('Energy Efficiency', fontsize=11)
        ax2.legend()
        ax2.grid(True, alpha=0.3)
    
    plt.tight_layout()
    fig.savefig(output_path, dpi=150, bbox_inches='tight')
    print(f"✅ Fault recovery plot saved to {output_path}")
    return fig

__all__ = [
    'SystemVisualizer',
    'plot_temperature_evolution',
    'plot_energy_consumption',
    'plot_fault_recovery'
]
