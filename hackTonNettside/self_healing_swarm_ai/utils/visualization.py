
import matplotlib.pyplot as plt
import numpy as np
from typing import Dict, List, Optional
import seaborn as sns

class SystemVisualizer:
    """
    Visualization utilities for the cooling system.
    """
    
    def __init__(self, style: str = 'seaborn-v0_8-darkgrid'):
        try:
            plt.style.use(style)
        except:
            plt.style.use('default')
        
        sns.set_palette("husl")
        self.fig = None
        self.axes = None
    
    def plot_temperature_evolution(self, temp_history: List[List[float]], 
                                   target_temp: float,
                                   faulty_agent_id: Optional[int] = None,
                                   fault_step: Optional[int] = None) -> plt.Figure:
        """
        Plot temperature evolution for all agents.
        
        Args:
            temp_history: List of temperature arrays over time
            target_temp: Target temperature line
            faulty_agent_id: ID of faulty agent (if any)
            fault_step: Step when fault occurred
            
        Returns:
            Matplotlib figure
        """
        fig, ax = plt.subplots(figsize=(12, 6))
        
        num_agents = len(temp_history[0]) if temp_history else 0
        
        for agent_id in range(num_agents):
            temps = [step[agent_id] for step in temp_history]
            color = 'red' if agent_id == faulty_agent_id else None
            linewidth = 2.5 if agent_id == faulty_agent_id else 1.5
            label = f'Agent {agent_id}' + (' (FAULTY)' if agent_id == faulty_agent_id else '')
            
            ax.plot(temps, color=color, linewidth=linewidth, label=label, alpha=0.8)
        
        # Target temperature line
        ax.axhline(y=target_temp, color='blue', linestyle='--', linewidth=2, label='Target')
        
        # Mark fault injection
        if fault_step is not None:
            ax.axvline(x=fault_step, color='orange', linestyle=':', linewidth=2, label='Fault Injected')
        
        ax.set_xlabel('Time Steps', fontsize=12)
        ax.set_ylabel('Temperature (°C)', fontsize=12)
        ax.set_title('Temperature Evolution - Self-Healing Behavior', fontsize=14, fontweight='bold')
        ax.legend(loc='best', fontsize=9)
        ax.grid(True, alpha=0.3)
        
        plt.tight_layout()
        return fig
    
    def plot_power_consumption(self, power_history: List[float]) -> plt.Figure:
        """
        Plot total power consumption over time.
        
        Args:
            power_history: List of total power values
            
        Returns:
            Matplotlib figure
        """
        fig, ax = plt.subplots(figsize=(10, 5))
        
        ax.plot(power_history, color='orange', linewidth=2)
        ax.fill_between(range(len(power_history)), power_history, alpha=0.3, color='orange')
        
        ax.set_xlabel('Time Steps', fontsize=12)
        ax.set_ylabel('Total Power (W)', fontsize=12)
        ax.set_title('System Power Consumption', fontsize=14, fontweight='bold')
        ax.grid(True, alpha=0.3)
        
        # Add statistics
        avg_power = np.mean(power_history)
        ax.axhline(y=avg_power, color='red', linestyle='--', label=f'Average: {avg_power:.1f}W')
        ax.legend()
        
        plt.tight_layout()
        return fig
    
    def plot_system_metrics(self, metrics: Dict[str, List[float]]) -> plt.Figure:
        """
        Plot multiple system metrics in subplots.
        
        Args:
            metrics: Dict of metric names to value lists
            
        Returns:
            Matplotlib figure
        """
        num_metrics = len(metrics)
        fig, axes = plt.subplots(num_metrics, 1, figsize=(12, 3 * num_metrics))
        
        if num_metrics == 1:
            axes = [axes]
        
        for idx, (metric_name, values) in enumerate(metrics.items()):
            ax = axes[idx]
            ax.plot(values, linewidth=2)
            ax.set_ylabel(metric_name.replace('_', ' ').title())
            ax.grid(True, alpha=0.3)
            
            if idx == len(metrics) - 1:
                ax.set_xlabel('Time Steps')
        
        fig.suptitle('System Performance Metrics', fontsize=16, fontweight='bold')
        plt.tight_layout()
        return fig
    
    def plot_agent_heatmap(self, agent_states: List[Dict], 
                          metric: str = 'temperature') -> plt.Figure:
        """
        Plot heatmap of agent states.
        
        Args:
            agent_states: List of agent state dicts
            metric: Which metric to visualize
            
        Returns:
            Matplotlib figure
        """
        fig, ax = plt.subplots(figsize=(10, 6))
        
        # Extract metric values
        values = [state.get(metric, 0) for state in agent_states]
        agent_ids = [state['agent_id'] for state in agent_states]
        
        # Create bar plot with color coding
        colors = ['red' if state.get('is_faulty', False) else 'green' for state in agent_states]
        
        bars = ax.bar(agent_ids, values, color=colors, alpha=0.7, edgecolor='black')
        
        ax.set_xlabel('Agent ID', fontsize=12)
        ax.set_ylabel(metric.replace('_', ' ').title(), fontsize=12)
        ax.set_title(f'Agent {metric.title()} Status', fontsize=14, fontweight='bold')
        ax.grid(True, alpha=0.3, axis='y')
        
        # Add legend
        from matplotlib.patches import Patch
        legend_elements = [
            Patch(facecolor='green', alpha=0.7, label='Healthy'),
            Patch(facecolor='red', alpha=0.7, label='Faulty')
        ]
        ax.legend(handles=legend_elements)
        
        plt.tight_layout()
        return fig
    
    def plot_network_topology(self, num_agents: int, neighbors: Dict[int, List[int]],
                             agent_states: Optional[List[Dict]] = None) -> plt.Figure:
        """
        Visualize agent network topology.
        
        Args:
            num_agents: Total number of agents
            neighbors: Dict mapping agent ID to list of neighbor IDs
            agent_states: Optional agent states for color coding
            
        Returns:
            Matplotlib figure
        """
        import networkx as nx
        
        fig, ax = plt.subplots(figsize=(10, 10))
        
        # Create graph
        G = nx.Graph()
        G.add_nodes_from(range(num_agents))
        
        # Add edges
        for agent_id, neighbor_list in neighbors.items():
            for neighbor_id in neighbor_list:
                G.add_edge(agent_id, neighbor_id)
        
        # Position nodes in a circle
        pos = nx.circular_layout(G)
        
        # Color nodes based on state
        if agent_states:
            node_colors = []
            for i in range(num_agents):
                state = agent_states[i] if i < len(agent_states) else {}
                if state.get('is_faulty', False):
                    node_colors.append('red')
                elif not state.get('is_active', True):
                    node_colors.append('gray')
                else:
                    node_colors.append('lightgreen')
        else:
            node_colors = ['lightblue'] * num_agents
        
        # Draw network
        nx.draw_networkx_nodes(G, pos, node_color=node_colors, 
                              node_size=800, alpha=0.9, ax=ax)
        nx.draw_networkx_edges(G, pos, alpha=0.5, width=2, ax=ax)
        nx.draw_networkx_labels(G, pos, font_size=12, font_weight='bold', ax=ax)
        
        ax.set_title('Agent Network Topology', fontsize=14, fontweight='bold')
        ax.axis('off')
        
        # Add legend
        from matplotlib.patches import Patch
        legend_elements = [
            Patch(facecolor='lightgreen', label='Healthy'),
            Patch(facecolor='red', label='Faulty'),
            Patch(facecolor='gray', label='Inactive'),
            Patch(facecolor='lightblue', label='Uninitialized')
        ]
        ax.legend(handles=legend_elements, loc='upper right', bbox_to_anchor=(1.15, 1))
        
        plt.tight_layout()
        return fig
    
    def plot_fault_recovery_timeline(self, fault_events: List[Dict]) -> plt.Figure:
        """
        Plot timeline of fault injection and recovery events.
        
        Args:
            fault_events: List of fault event dicts with 'injection_time', 'detection_time', 'recovery_time'
            
        Returns:
            Matplotlib figure
        """
        fig, ax = plt.subplots(figsize=(12, 6))
        
        for idx, event in enumerate(fault_events):
            agent_id = event.get('agent_id', idx)
            injection = event.get('injection_time', 0)
            detection = event.get('detection_time', injection)
            recovery = event.get('recovery_time', detection)
            
            # Plot timeline
            ax.plot([injection, detection], [agent_id, agent_id], 'r-', linewidth=3, label='Fault Active' if idx == 0 else '')
            ax.plot([detection, recovery], [agent_id, agent_id], 'y-', linewidth=3, label='Healing' if idx == 0 else '')
            
            # Mark events
            ax.scatter([injection], [agent_id], color='red', s=100, marker='x', zorder=5)
            ax.scatter([detection], [agent_id], color='orange', s=100, marker='o', zorder=5)
            ax.scatter([recovery], [agent_id], color='green', s=100, marker='s', zorder=5)
        
        ax.set_xlabel('Time Steps', fontsize=12)
        ax.set_ylabel('Agent ID', fontsize=12)
        ax.set_title('Fault Injection and Recovery Timeline', fontsize=14, fontweight='bold')
        ax.legend(['Fault Active', 'Healing Process', 'Injection', 'Detection', 'Recovery'])
        ax.grid(True, alpha=0.3)
        
        plt.tight_layout()
        return fig
    
    def plot_comparative_analysis(self, baseline_metrics: Dict, swarm_metrics: Dict) -> plt.Figure:
        """
        Compare baseline vs swarm performance.
        
        Args:
            baseline_metrics: Metrics from baseline (no swarm) system
            swarm_metrics: Metrics from swarm-enabled system
            
        Returns:
            Matplotlib figure
        """
        fig, axes = plt.subplots(2, 2, figsize=(14, 10))
        
        metrics_to_compare = ['avg_temperature', 'total_power', 'temperature_variance', 'num_faults']
        titles = ['Average Temperature', 'Total Power Consumption', 'Temperature Variance', 'Number of Faults']
        
        for idx, (metric, title) in enumerate(zip(metrics_to_compare, titles)):
            ax = axes[idx // 2, idx % 2]
            
            if metric in baseline_metrics and metric in swarm_metrics:
                baseline_val = baseline_metrics[metric]
                swarm_val = swarm_metrics[metric]
                
                x = np.arange(len(baseline_val))
                width = 0.35
                
                ax.bar(x - width/2, baseline_val, width, label='Baseline', alpha=0.8)
                ax.bar(x + width/2, swarm_val, width, label='Swarm', alpha=0.8)
                
                ax.set_xlabel('Time Steps')
                ax.set_ylabel(title)
                ax.set_title(title)
                ax.legend()
                ax.grid(True, alpha=0.3)
        
        plt.suptitle('Comparative Analysis: Baseline vs Swarm Performance', fontsize=16, fontweight='bold')
        plt.tight_layout()
        return fig
