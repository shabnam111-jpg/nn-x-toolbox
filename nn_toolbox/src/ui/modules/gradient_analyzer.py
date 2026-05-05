"""
Gradient Flow Visualization
Detects and visualizes vanishing/exploding gradients across layers.
"""

import streamlit as st
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from src.ui.utils.gradient_tracker import GradientTracker


def plot_gradient_magnitudes(gradient_tracker: GradientTracker, 
                             current_epoch: int = None) -> go.Figure:
    """
    Plot gradient magnitudes for each layer as bar chart
    """
    magnitudes = gradient_tracker.get_all_layer_magnitudes()
    
    if not magnitudes:
        st.warning("⚠️ No gradient data available")
        return None
    
    layers = list(magnitudes.keys())
    values = list(magnitudes.values())
    
    # Color code by gradient health
    colors = []
    for layer, mag in magnitudes.items():
        if gradient_tracker.detect_vanishing_gradients(layer):
            colors.append('#ef4444')  # Red - vanishing
        elif gradient_tracker.detect_exploding_gradients(layer):
            colors.append('#f59e0b')  # Orange - exploding
        else:
            colors.append('#10b981')  # Green - healthy
    
    fig = go.Figure(data=[
        go.Bar(
            x=layers,
            y=values,
            marker=dict(color=colors),
            text=[f"{v:.2e}" for v in values],
            textposition="auto",
            hovertemplate='<b>%{x}</b><br>Magnitude: %{y:.2e}<extra></extra>'
        )
    ])
    
    fig.update_layout(
        title="🔍 Gradient Magnitudes per Layer",
        xaxis_title="Layer",
        yaxis_title="Gradient Magnitude",
        height=400,
        template='plotly_white',
        showlegend=False,
        yaxis_type='log'
    )
    
    return fig


def plot_gradient_flow_timeline(gradient_tracker: GradientTracker) -> go.Figure:
    """
    Plot gradient magnitude evolution over epochs for all layers
    """
    layer_names = list(gradient_tracker.layer_stats.keys())
    
    if not layer_names:
        st.warning("⚠️ No gradient history available")
        return None
    
    fig = go.Figure()
    
    for layer_name in layer_names:
        history = gradient_tracker.get_gradient_history(layer_name)
        if len(history) > 0:
            fig.add_trace(go.Scatter(
                x=np.arange(len(history)),
                y=history,
                mode='lines+markers',
                name=layer_name,
                hovertemplate='Epoch: %{x}<br>Gradient Mag: %{y:.2e}<extra></extra>'
            ))
    
    fig.update_layout(
        title="📈 Gradient Flow Timeline",
        xaxis_title="Epoch",
        yaxis_title="Gradient Magnitude",
        height=400,
        template='plotly_white',
        yaxis_type='log',
        hovermode='x unified'
    )
    
    return fig


def plot_gradient_health_heatmap(gradient_tracker: GradientTracker) -> go.Figure:
    """
    Heatmap showing gradient health over epochs and layers
    """
    layer_names = list(gradient_tracker.layer_stats.keys())
    
    if not layer_names:
        st.warning("⚠️ No gradient data available")
        return None
    
    # Build matrix: epochs x layers
    matrix = []
    max_epochs = 0
    
    for layer_name in layer_names:
        history = gradient_tracker.get_gradient_history(layer_name)
        matrix.append(history)
        max_epochs = max(max_epochs, len(history))
    
    # Pad shorter histories
    for i in range(len(matrix)):
        if len(matrix[i]) < max_epochs:
            matrix[i] = np.pad(matrix[i], (0, max_epochs - len(matrix[i])), 
                              mode='constant', constant_values=np.nan)
    
    matrix = np.array(matrix)
    
    fig = go.Figure(data=go.Heatmap(
        z=matrix,
        x=np.arange(matrix.shape[1]),
        y=layer_names,
        colorscale='Viridis',
        colorbar=dict(title="Gradient Mag"),
        hovertemplate='Layer: %{y}<br>Epoch: %{x}<br>Magnitude: %{z:.2e}<extra></extra>'
    ))
    
    fig.update_layout(
        title="🌡️ Gradient Health Heatmap",
        xaxis_title="Epoch",
        yaxis_title="Layer",
        height=400,
        template='plotly_white'
    )
    
    return fig


def gradient_health_summary(gradient_tracker: GradientTracker) -> dict:
    """
    Return gradient health metrics
    """
    layer_names = list(gradient_tracker.layer_stats.keys())
    
    summary = {
        'total_layers': len(layer_names),
        'vanishing': [],
        'exploding': [],
        'healthy': []
    }
    
    for layer_name in layer_names:
        if gradient_tracker.detect_vanishing_gradients(layer_name):
            summary['vanishing'].append(layer_name)
        elif gradient_tracker.detect_exploding_gradients(layer_name):
            summary['exploding'].append(layer_name)
        else:
            summary['healthy'].append(layer_name)
    
    return summary
