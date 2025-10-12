
"""
Data generation and loading utilities for Self-Healing Swarm AI Cooling System.

This module provides functions to generate synthetic datasets for:
- Baseline operational data
- Fault injection scenarios
- Runtime simulation logs
- Data normalization and preprocessing
"""

import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler
from datetime import datetime, timedelta
import os
from pathlib import Path

# Define base paths
BASE_DIR = Path(__file__).parent
RAW_DIR = BASE_DIR / 'raw'
PROCESSED_DIR = BASE_DIR / 'processed'
FAULT_DIR = BASE_DIR / 'fault_injection'
LOGS_DIR = BASE_DIR / 'logs'


def create_directories():
    """Create necessary directories if they don't exist."""
    for directory in [RAW_DIR, PROCESSED_DIR, FAULT_DIR, LOGS_DIR]:
        os.makedirs(directory, exist_ok=True)
        print(f"📁 Directory ready: {directory}")


def generate_baseline_data(num_samples=2000, num_racks=4):
    """
    Generate normal operational data for racks in a data center.
    
    Args:
        num_samples: Number of time samples to generate
        num_racks: Number of cooling racks/zones
        
    Returns:
        DataFrame with baseline operational data
    """
    print(f"🔄 Generating baseline data ({num_samples} samples, {num_racks} racks)...")
    
    np.random.seed(42)
    data = []
    
    start_time = datetime.now()
    
    for i in range(num_samples):
        timestamp = start_time + timedelta(minutes=i * 5)
        
        for rack_id in range(num_racks):
            # Simulate realistic values with slight variations per rack
            rack_offset = rack_id * 0.5  # Each rack slightly different
            
            data.append({
                'timestamp': timestamp,
                'rack_id': rack_id,
                'temp_C': np.random.normal(25.0 + rack_offset, 0.6),
                'humidity_%': np.random.normal(45.0, 2.0),
                'power_kW': np.random.normal(3.0 + rack_offset * 0.2, 0.3),
                'fan_speed_%': np.random.uniform(50, 70),
                'airflow_CFM': np.random.normal(450, 20)
            })
    
    df = pd.DataFrame(data)
    
    # Save to CSV
    output_path = RAW_DIR / 'baseline_operation.csv'
    df.to_csv(output_path, index=False)
    print(f"✅ Saved baseline data to: {output_path}")
    print(f"   Shape: {df.shape}, Columns: {list(df.columns)}")
    
    return df


def normalize_data(input_path, output_path):
    """
    Load raw data and normalize numerical columns using MinMaxScaler.
    
    Args:
        input_path: Path to input CSV file
        output_path: Path to save normalized CSV file
        
    Returns:
        Normalized DataFrame
    """
    print(f"🔄 Normalizing data from: {input_path}")
    
    try:
        # Load data
        df = pd.read_csv(input_path)
        
        # Identify numerical columns to normalize (exclude timestamp and IDs)
        numerical_cols = ['temp_C', 'humidity_%', 'power_kW', 'fan_speed_%', 'airflow_CFM']
        
        # Create a copy for normalized data
        df_normalized = df.copy()
        
        # Apply MinMaxScaler
        scaler = MinMaxScaler()
        df_normalized[numerical_cols] = scaler.fit_transform(df[numerical_cols])
        
        # Save normalized data
        df_normalized.to_csv(output_path, index=False)
        print(f"✅ Saved normalized data to: {output_path}")
        print(f"   Normalization range: [0, 1] for columns: {numerical_cols}")
        
        return df_normalized
        
    except FileNotFoundError:
        print(f"❌ Error: Input file not found at {input_path}")
        return None
    except Exception as e:
        print(f"❌ Error during normalization: {e}")
        return None


def generate_fault_scenarios():
    """
    Create synthetic fault datasets for testing the self-healing system.
    
    Generates three fault scenarios:
    1. Fan Failure: fan speed = 0, temperature rises by +5°C
    2. Sensor Drift: temperature drifts upward by +2.5°C
    3. Cooling Drop: airflow drops by 200 CFM, temperature rises by +3°C
    """
    print("🔄 Generating fault injection scenarios...")
    
    np.random.seed(42)
    num_samples = 500
    start_time = datetime.now()
    
    # --- Scenario 1: Fan Failure ---
    print("  📌 Creating fan_failure.csv...")
    fan_failure_data = []
    
    for i in range(num_samples):
        timestamp = start_time + timedelta(minutes=i * 2)
        
        # Fan fails at step 100
        if i < 100:
            fan_speed = np.random.uniform(50, 70)
            temp = np.random.normal(25.0, 0.6)
        else:
            fan_speed = 0  # Fan failure
            temp = 25.0 + min((i - 100) * 0.1, 5.0)  # Gradual rise up to +5°C
        
        fan_failure_data.append({
            'timestamp': timestamp,
            'rack_id': 2,  # Fault in rack 2
            'temp_C': temp + np.random.normal(0, 0.3),
            'humidity_%': np.random.normal(45.0, 2.0),
            'power_kW': np.random.normal(3.0, 0.3),
            'fan_speed_%': fan_speed,
            'airflow_CFM': np.random.normal(450 if i < 100 else 200, 20),
            'fault_type': 'fan_failure' if i >= 100 else 'normal'
        })
    
    df_fan = pd.DataFrame(fan_failure_data)
    df_fan.to_csv(FAULT_DIR / 'fan_failure.csv', index=False)
    print(f"  ✅ Saved: {FAULT_DIR / 'fan_failure.csv'}")
    
    # --- Scenario 2: Sensor Drift ---
    print("  📌 Creating sensor_drift.csv...")
    sensor_drift_data = []
    
    for i in range(num_samples):
        timestamp = start_time + timedelta(minutes=i * 2)
        
        # Sensor starts drifting at step 150
        if i < 150:
            temp = np.random.normal(25.0, 0.6)
        else:
            drift = min((i - 150) * 0.02, 2.5)  # Slow drift up to +2.5°C
            temp = 25.0 + drift
        
        sensor_drift_data.append({
            'timestamp': timestamp,
            'rack_id': 1,  # Fault in rack 1
            'temp_C': temp + np.random.normal(0, 0.3),
            'humidity_%': np.random.normal(45.0, 2.0),
            'power_kW': np.random.normal(3.0, 0.3),
            'fan_speed_%': np.random.uniform(50, 70),
            'airflow_CFM': np.random.normal(450, 20),
            'fault_type': 'sensor_drift' if i >= 150 else 'normal'
        })
    
    df_drift = pd.DataFrame(sensor_drift_data)
    df_drift.to_csv(FAULT_DIR / 'sensor_drift.csv', index=False)
    print(f"  ✅ Saved: {FAULT_DIR / 'sensor_drift.csv'}")
    
    # --- Scenario 3: Cooling Drop ---
    print("  📌 Creating cooling_drop.csv...")
    cooling_drop_data = []
    
    for i in range(num_samples):
        timestamp = start_time + timedelta(minutes=i * 2)
        
        # Cooling system degrades at step 200
        if i < 200:
            airflow = np.random.normal(450, 20)
            temp = np.random.normal(25.0, 0.6)
        else:
            airflow = np.random.normal(250, 20)  # Drop by 200 CFM
            temp = 25.0 + min((i - 200) * 0.08, 3.0)  # Rise up to +3°C
        
        cooling_drop_data.append({
            'timestamp': timestamp,
            'rack_id': 3,  # Fault in rack 3
            'temp_C': temp + np.random.normal(0, 0.3),
            'humidity_%': np.random.normal(45.0, 2.0),
            'power_kW': np.random.normal(3.0, 0.3),
            'fan_speed_%': np.random.uniform(50, 70),
            'airflow_CFM': airflow,
            'fault_type': 'cooling_drop' if i >= 200 else 'normal'
        })
    
    df_cooling = pd.DataFrame(cooling_drop_data)
    df_cooling.to_csv(FAULT_DIR / 'cooling_drop.csv', index=False)
    print(f"  ✅ Saved: {FAULT_DIR / 'cooling_drop.csv'}")
    
    print("✅ All fault scenarios generated successfully!")


def generate_logs(num_steps=200):
    """
    Simulate runtime logs with agent behavior and anomaly detection.
    
    Args:
        num_steps: Number of simulation timesteps
        
    Returns:
        DataFrame with runtime logs
    """
    print(f"🔄 Generating runtime logs ({num_steps} steps)...")
    
    np.random.seed(42)
    data = []
    
    num_agents = 6
    
    for step in range(num_steps):
        for agent_id in range(num_agents):
            # 10% chance of anomaly
            is_anomaly = np.random.random() < 0.1
            
            if is_anomaly:
                temp = np.random.uniform(28, 32)  # High temperature
                fan_speed = np.random.uniform(80, 100)  # High fan speed
                energy = np.random.uniform(4.5, 6.0)  # High energy
            else:
                temp = np.random.normal(25.0, 0.8)
                fan_speed = np.random.uniform(50, 70)
                energy = np.random.normal(3.0, 0.4)
            
            # Neighbor adjustment (swarm cooperation)
            neighbor_adjustment = np.random.uniform(-0.5, 0.5) if not is_anomaly else np.random.uniform(-1.5, 1.5)
            
            data.append({
                'timestep': step,
                'agent_id': agent_id,
                'temp_C': temp,
                'fan_speed_%': fan_speed,
                'anomaly_flag': 1 if is_anomaly else 0,
                'energy_kW': energy,
                'neighbor_adjustment': neighbor_adjustment
            })
    
    df = pd.DataFrame(data)
    
    # Save to CSV
    output_path = LOGS_DIR / 'run_log.csv'
    df.to_csv(output_path, index=False)
    print(f"✅ Saved runtime logs to: {output_path}")
    print(f"   Total entries: {len(df)}")


def load_data(file_path):
    """
    Utility function to load any dataset into a Pandas DataFrame.
    
    Args:
        file_path: Path to the CSV file
        
    Returns:
        DataFrame with loaded data
    """
    try:
        df = pd.read_csv(file_path)
        print(f"✅ Loaded data from: {file_path}")
        return df
    except FileNotFoundError:
        print(f"❌ File not found: {file_path}")
        return None
    except Exception as e:
        print(f"❌ Error loading data: {e}")
        return None


if __name__ == "__main__":
    # Create directories
    create_directories()
    
    # Generate all datasets
    generate_baseline_data()
    normalize_data(RAW_DIR / 'baseline_operation.csv', PROCESSED_DIR / 'normalized_baseline.csv')
    generate_fault_scenarios()
    generate_logs()
    
    print("✅ Data generation complete.")
