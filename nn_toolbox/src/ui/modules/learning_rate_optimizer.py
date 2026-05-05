"""
Learning Rate Analysis
Compare convergence curves for multiple learning rates.
"""

import streamlit as st
import numpy as np
import plotly.graph_objects as go
from typing import Dict, List


def plot_learning_rate_comparison(lr_histories: Dict[float, Dict[str, List[float]]]
                                 ) -> go.Figure:
    """
    Plot loss curves for multiple learning rates
    
    Args:
        lr_histories: {lr_value: {'train_loss': [...], 'epochs': [...]}}
    
    Returns:
        Plotly figure
    """
    fig = go.Figure()
    
    colors = ['#ef4444', '#f97316', '#eab308', '#84cc16', '#22c55e', '#10b981']
    
    for idx, (lr, history) in enumerate(sorted(lr_histories.items())):
        train_loss = history.get('train_loss', [])
        epochs = history.get('epochs', np.arange(len(train_loss)))
        
        color = colors[idx % len(colors)]
        
        fig.add_trace(go.Scatter(
            x=epochs,
            y=train_loss,
            mode='lines+markers',
            name=f"LR = {lr}",
            line=dict(color=color, width=2),
            marker=dict(size=4),
            hovertemplate='Epoch: %{x}<br>Loss: %{y:.4f}<extra></extra>'
        ))
    
    fig.update_layout(
        title="📈 Learning Rate Comparison - Convergence Analysis",
        xaxis_title="Epoch",
        yaxis_title="Training Loss",
        hovermode='x unified',
        height=500,
        template='plotly_white',
        yaxis_type='log'
    )
    
    return fig


def plot_learning_rate_stability(lr_histories: Dict[float, Dict[str, List[float]]]
                                ) -> go.Figure:
    """
    Analyze stability and oscillation for each learning rate
    """
    fig = go.Figure()
    
    summary_data = []
    
    for lr, history in sorted(lr_histories.items()):
        train_loss = np.array(history.get('train_loss', []))
        
        if len(train_loss) < 2:
            continue
        
        # Calculate loss variance (stability metric)
        loss_diff = np.diff(train_loss)
        oscillation = np.std(loss_diff)
        final_loss = train_loss[-1]
        min_loss = np.min(train_loss)
        convergence_speed = len(train_loss)  # Epochs to converge
        
        summary_data.append({
            'lr': lr,
            'oscillation': oscillation,
            'final_loss': final_loss,
            'min_loss': min_loss,
            'convergence': convergence_speed
        })
    
    # Create summary table
    lrs = [d['lr'] for d in summary_data]
    oscillations = [d['oscillation'] for d in summary_data]
    final_losses = [d['final_loss'] for d in summary_data]
    
    fig = go.Figure(data=[
        go.Bar(
            x=lrs,
            y=oscillations,
            marker=dict(color=oscillations, colorscale='Viridis', showscale=True),
            name='Oscillation',
            hovertemplate='LR: %{x}<br>Oscillation: %{y:.4f}<extra></extra>'
        )
    ])
    
    fig.update_layout(
        title="⚡ Learning Rate Stability - Loss Oscillation",
        xaxis_title="Learning Rate (log scale)",
        yaxis_title="Loss Oscillation (Std of Gradient)",
        xaxis_type='log',
        height=400,
        template='plotly_white'
    )
    
    return fig


def analyze_learning_rate_effects(lr_histories: Dict[float, Dict[str, List[float]]]
                                 ) -> Dict:
    """
    Comprehensive learning rate analysis
    """
    analysis = {
        'optimal_lr': None,
        'best_final_loss': float('inf'),
        'fastest_convergence': None,
        'most_stable': None,
        'summary': {}
    }
    
    min_oscillation = float('inf')
    
    for lr, history in lr_histories.items():
        train_loss = np.array(history.get('train_loss', []))
        
        if len(train_loss) == 0:
            continue
        
        final_loss = train_loss[-1]
        min_loss = np.min(train_loss)
        loss_diff = np.diff(train_loss)
        oscillation = np.std(loss_diff) if len(loss_diff) > 0 else 0
        
        # Find optimal (best final loss)
        if final_loss < analysis['best_final_loss']:
            analysis['best_final_loss'] = final_loss
            analysis['optimal_lr'] = lr
        
        # Find most stable (least oscillation)
        if oscillation < min_oscillation:
            min_oscillation = oscillation
            analysis['most_stable'] = lr
        
        # Find fastest convergence (earliest plateau)
        threshold = min_loss * 1.05
        for epoch, loss in enumerate(train_loss):
            if loss < threshold:
                if analysis['fastest_convergence'] is None or epoch < analysis['fastest_convergence']:
                    analysis['fastest_convergence'] = epoch
        
        analysis['summary'][str(lr)] = {
            'final_loss': float(final_loss),
            'min_loss': float(min_loss),
            'oscillation': float(oscillation)
        }
    
    return analysis


def plot_learning_curve_acceleration(lr_histories: Dict[float, Dict[str, List[float]]]
                                    ) -> go.Figure:
    """
    Plot epochs needed to reach target loss for each learning rate
    """
    fig = go.Figure()
    
    targets = [0.5, 0.3, 0.2, 0.1]  # Loss thresholds
    
    for target in targets:
        lrs = []
        epochs_needed = []
        
        for lr, history in sorted(lr_histories.items()):
            train_loss = np.array(history.get('train_loss', []))
            
            # Find epoch where loss drops below target
            reached = np.where(train_loss < target)[0]
            if len(reached) > 0:
                lrs.append(lr)
                epochs_needed.append(reached[0])
        
        if lrs:
            fig.add_trace(go.Scatter(
                x=lrs,
                y=epochs_needed,
                mode='lines+markers',
                name=f"Target Loss: {target}",
                marker=dict(size=8),
                hovertemplate='LR: %{x}<br>Epochs: %{y:.0f}<extra></extra>'
            ))
    
    fig.update_layout(
        title="🚀 Learning Rate Performance - Convergence Speed",
        xaxis_title="Learning Rate (log scale)",
        yaxis_title="Epochs to Target",
        xaxis_type='log',
        height=400,
        template='plotly_white',
        hovermode='x unified'
    )
    
    return fig
